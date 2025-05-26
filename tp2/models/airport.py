from simpy import Environment, Resource

from random import expovariate, seed
from typing import Generator

from config.simulation_config import SimulationConfig


class Airport:

    def __init__(self, config: SimulationConfig, robots_count: int) -> None:
        self._config: SimulationConfig = config
        seed(self._config.RANDOM_SEED)
        self._env: Environment = Environment()
        self._robots: Resource = Resource(self._env)

        self._total_planes: int = 0
        self._planes_unloaded_count: int = 0
        self._cumulative_queue_time: float = 0.0
        self._planes_queue_lenght: int = 0
        self._cumulative_queue_length_sum: float = 0.0
        self._queue_length_sample_count: int = 0

        self._robots_count: int = robots_count
        self._robots_busy_time: float = 0.0

        self._total_time_of_operations: float = 0.0  # Total time of operations in minutes

        self._planes_unloaded_hourly: dict = {}
        self._mean_queue_lenght_over_time: dict = {}
        self._mean_queue_time_over_time: dict = {}
        self._cumulative_robots_activity_ratio: dict = {}

    def manage_operations(self) -> None:
        operations_start_time = self._env.now
        self._env.process(self._handle_plane_arrival())
        self._env.process(self._manage_timely_statistics())
        self._env.run(until=self._config.SIMULATION_TIME)  # Run the simulation for the specified number of minutes
        self._total_time_of_operations = self._env.now - operations_start_time

    def _handle_plane_arrival(self) -> Generator:
        while True:
            yield from self._wait_for_new_plane()
            self._create_new_plane()
            self._env.process(self._unload_plane())

    def _wait_for_new_plane(self) -> Generator:
        yield self._env.timeout(expovariate(1 / self._config.PLANES_MEAN_ARRIVAL_TIME))

    def _create_new_plane(self) -> None:
        self._total_planes += 1
        self._planes_queue_lenght += 1

    def _unload_plane(self) -> Generator:
        with self._robots.request() as request:
            yield from self._wait_for_robots(request)
            self._planes_queue_lenght -= 1
            yield from self._robots_unload_plane()

    def _wait_for_robots(self, robot_request) -> Generator:
        queue_start_waiting_time = self._env.now
        yield robot_request
        queue_end_waiting_time = self._env.now
        self._cumulative_queue_time += queue_end_waiting_time - queue_start_waiting_time

    def _robots_unload_plane(self) -> Generator:
        robots_busy_start_time = self._env.now

        yield self._env.timeout(expovariate(1 / self._config.ROBOTs_MEAN_UNLOADING_TIMES[self._robots_count]))
        self._planes_unloaded_count += 1

        robots_busy_end_time = self._env.now
        self._robots_busy_time += robots_busy_end_time - robots_busy_start_time

    def _manage_timely_statistics(self) -> Generator:
        """Track timely statistics for planes unloaded per hour, queue length, mean queue time and robot activity ratio. The statistics are collected every time frame in minutes"""

        while True:
            yield self._env.timeout(1)
            current_time = self._env.now

            if (current_time + 1) % 60 == 0:  # Every hour
                self._planes_unloaded_hourly[current_time] = (
                    self._planes_unloaded_count / (current_time / 60) if current_time > 0 else 0
                )

            self._cumulative_robots_activity_ratio[current_time] = (
                self._robots_busy_time / current_time if current_time > 0 else 0
            )

            self._cumulative_queue_length_sum += self._planes_queue_lenght
            self._queue_length_sample_count += 1
            self._mean_queue_lenght_over_time[current_time] = (
                self._cumulative_queue_length_sum / self._queue_length_sample_count if self._queue_length_sample_count > 0 else 0
            )

            self._mean_queue_time_over_time[current_time] = (
                self._cumulative_queue_time / self._planes_unloaded_count if self._planes_unloaded_count > 0 else 0
            )

    def get_final_performance_statistics(self) -> dict:
        planes_unloaded_hourly: float = self._planes_unloaded_count / (self._config.SIMULATION_TIME / 60)
        mean_queue_time: float = (
            self._cumulative_queue_time / self._planes_unloaded_count if self._planes_unloaded_count > 0 else 0
        )

        return {
            "simulation_time": self._config.SIMULATION_TIME,
            "total_planes": self._total_planes,
            "planes_unloaded_count": self._planes_unloaded_count,
            "planes_queue_lenght": self._planes_queue_lenght,
            "robot_activity_ratio": self._cumulative_robots_activity_ratio.get(self._config.SIMULATION_TIME, 0),
            "planes_unloaded_hourly": planes_unloaded_hourly,
            "mean_queue_time": mean_queue_time,
            "total_time_of_operations": self._total_time_of_operations,
        }

    def get_time_performance_statistics(self) -> dict:
        return {
            "planes_unloaded_hourly": self._planes_unloaded_hourly,
            "planes_queue_lenght_over_time": self._mean_queue_lenght_over_time,
            "mean_queue_time_over_time": self._mean_queue_time_over_time,
            "cumulative_robots_activity_ratio": self._cumulative_robots_activity_ratio,
        }
