from typing import Generator
from simpy import *
from random import expovariate
from uuid import uuid4, UUID

from config.config import SimulationConfig


class Airport:

    def __init__(self, config: SimulationConfig, robots_count: int) -> None:
        self.config: SimulationConfig = config
        self.env: Environment = Environment()
        self.robots: Resource = Resource(self.env)

        self.cumulative_queue_time: float = 0.0
        self.planes_unloaded_count: int = 0
        self.number_of_plane_in_queue: int = 0

        self.robots_count: int = robots_count
        self.robots_busy_time: float = 0.0

    def manage_airport_operations(self) -> None:
        self.env.process(self._handle_airplane_arrival())
        self.env.run(until=self.config.SIMULATION_TIME)

    def _handle_airplane_arrival(self) -> Generator:
        while True:
            yield from self._wait_for_new_airplane()
            airplane_id: UUID = self._create_new_aiplane()
            self.env.process(self._unload_airplane(airplane_id))

    def _wait_for_new_airplane(self) -> Generator:
        yield self.env.timeout(expovariate(1 / self.config.AIRPLANES_MEAN_ARRIVAL_TIME))

    def _create_new_aiplane(self) -> UUID:
        airplane_id: UUID = uuid4()
        self.number_of_plane_in_queue += 1
        return airplane_id

    def _unload_airplane(self, airplane_id: UUID) -> Generator:
        with self.robots.request() as request:
            yield from self._wait_for_robots(request)
            self.number_of_plane_in_queue -= 1
            yield from self._robots_unload_airplane()

    def _wait_for_robots(self, robot_request) -> Generator:
        queue_start_waiting_time = self.env.now
        yield robot_request
        queue_end_waiting_time = self.env.now
        self.cumulative_queue_time += queue_end_waiting_time - queue_start_waiting_time

    def _robots_unload_airplane(self) -> Generator:
        robots_busy_start_time = self.env.now

        yield self.env.timeout(
            expovariate(1 / self.config.ROBOTs_MEAN_UNLOADING_TIMES[self.robots_count])
        )
        self.planes_unloaded_count += 1

        robots_busy_end_time = self.env.now
        self.robots_busy_time += robots_busy_end_time - robots_busy_start_time

    def get_performance_statistics(self) -> dict:
        planes_unloaded_hourly = self.planes_unloaded_count / (
            self.config.SIMULATION_TIME / 60
        )
        mean_queue_time = (
            self.cumulative_queue_time / self.planes_unloaded_count
            if self.planes_unloaded_count > 0
            else 0
        )
        robot_activity_ratio = (
            (self.robots_busy_time / self.config.SIMULATION_TIME)
            if self.config.SIMULATION_TIME > 0
            else 0
        )

        return {
            "planes_unloaded_count": self.planes_unloaded_count,
            "planes_unloaded_hourly": planes_unloaded_hourly,
            "number_of_plane_in_queue": self.number_of_plane_in_queue,
            "mean_queue_time": mean_queue_time,
            "robot_activity_ratio": robot_activity_ratio,
        }
