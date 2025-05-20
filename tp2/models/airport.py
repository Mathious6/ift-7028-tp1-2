from simpy import Environment, Resource

from random import expovariate
from typing import Generator

from config.config import SimulationConfig


class Airport:

    def __init__(self, config: SimulationConfig, robots_count: int) -> None:
        self.config: SimulationConfig = config
        self.env: Environment = Environment()
        self.robots: Resource = Resource(self.env)

        self.total_planes: int = 0
        self.cumulative_queue_time: float = 0.0
        self.planes_unloaded_count: int = 0
        self.planes_queue_lenght: int = 0

        self.robots_count: int = robots_count
        self.robots_busy_time: float = 0.0

        self.total_time_of_operations: float = 0.0

    def manage_operations(self) -> None:
        operations_start_time = self.env.now
        self.env.process(self._handle_plane_arrival())
        self.env.run(until=self.config.SIMULATION_TIME)
        self.total_time_of_operations = self.env.now - operations_start_time

    def _handle_plane_arrival(self) -> Generator:
        while True:
            yield from self._wait_for_new_plane()
            self._create_new_plane()
            self.env.process(self._unload_plane())

    def _wait_for_new_plane(self) -> Generator:
        yield self.env.timeout(expovariate(1 / self.config.PLANES_MEAN_ARRIVAL_TIME))

    def _create_new_plane(self) -> None:
        self.total_planes += 1
        self.planes_queue_lenght += 1

    def _unload_plane(self) -> Generator:
        with self.robots.request() as request:
            yield from self._wait_for_robots(request)
            self.planes_queue_lenght -= 1
            yield from self._robots_unload_plane()

    def _wait_for_robots(self, robot_request) -> Generator:
        queue_start_waiting_time = self.env.now
        yield robot_request
        queue_end_waiting_time = self.env.now
        self.cumulative_queue_time += queue_end_waiting_time - queue_start_waiting_time

    def _robots_unload_plane(self) -> Generator:
        robots_busy_start_time = self.env.now

        yield self.env.timeout(
            expovariate(1 / self.config.ROBOTs_MEAN_UNLOADING_TIMES[self.robots_count])
        )
        self.planes_unloaded_count += 1

        robots_busy_end_time = self.env.now
        self.robots_busy_time += robots_busy_end_time - robots_busy_start_time

    def get_performance_statistics(self) -> dict:
        planes_unloaded_hourly: float = self.planes_unloaded_count / (
            self.config.SIMULATION_TIME / 60
        )
        mean_queue_time: float = (
            self.cumulative_queue_time / self.planes_unloaded_count
            if self.planes_unloaded_count > 0
            else 0
        )
        robot_activity_ratio: float = (
            (self.robots_busy_time / self.config.SIMULATION_TIME)
            if self.config.SIMULATION_TIME > 0
            else 0
        )

        return {
            "simulation_time": self.config.SIMULATION_TIME,
            "total_planes": self.total_planes,
            "planes_unloaded_count": self.planes_unloaded_count,
            "planes_queue_lenght": self.planes_queue_lenght,
            "robot_activity_ratio": robot_activity_ratio,
            "planes_unloaded_hourly": planes_unloaded_hourly,
            "mean_queue_time": mean_queue_time,
            "total_time_of_operations": self.total_time_of_operations,
        }
