from typing import Generator
from simpy import *
from random import expovariate
from uuid import uuid4, UUID

from config.config import SimulationConfig


class Simulation:

    def __init__(self, config: SimulationConfig) -> None:
        self.config: SimulationConfig = config
        self.env: Environment = Environment()
        self.robots: Resource = Resource(self.env)

        self.total_time_in_queue: float = 0.0
        self.total_number_of_planes_unloaded: int = 0
        self.number_of_plane_in_queue: int = 0

        self.robots_busy_time: float = 0.0

    def run(self) -> None:
        self.env.process(self._simulate_airplane_arrival())
        self.env.run(until=self.config.SIMULATION_TIME)

    def _simulate_airplane_arrival(self) -> Generator:
        while True:
            yield from self._wait_for_new_airplane()
            airplane_id: UUID = self._create_new_aiplane()
            self.env.process(self._simulate_airplane_unloading(airplane_id))

    def _wait_for_new_airplane(self) -> Generator:
        yield self.env.timeout(expovariate(1 / self.config.MEAN_ARRIVAL_TIME))

    def _create_new_aiplane(self) -> UUID:
        arrival_time = self.env.now
        airplane_id: UUID = uuid4()
        self.number_of_plane_in_queue += 1
        print(f"Airplane {airplane_id} arrived at {arrival_time}")
        return airplane_id

    def _simulate_airplane_unloading(self, airplane_id: UUID) -> Generator:
        with self.robots.request() as request:
            yield from self._wait_for_robots(request)
            print(f"Airplane {airplane_id} started unloading at {self.env.now}")
            self.number_of_plane_in_queue -= 1
            yield from self._robots_unload_airplane()
            print(f"Airplane {airplane_id} finished unloading at {self.env.now}")

    def _wait_for_robots(self, robot_request) -> Generator:
        queue_start_waiting_time = self.env.now
        yield robot_request
        queue_end_waiting_time = self.env.now
        self.total_time_in_queue += queue_end_waiting_time - queue_start_waiting_time

    def _robots_unload_airplane(self) -> Generator:
        robots_busy_start_time = self.env.now

        yield self.env.timeout(
            expovariate(1 / self.config.ROBOT_SCENARIOS[self.config.NUMBER_OF_ROBOTS])
        )
        self.total_number_of_planes_unloaded += 1

        robots_busy_end_time = self.env.now
        self.robots_busy_time += robots_busy_end_time - robots_busy_start_time

    def get_performance_metrics(self) -> dict:
        number_of_planes_unloaded_per_hour = self.total_number_of_planes_unloaded / (
            self.config.SIMULATION_TIME / 60
        )
        average_time_in_queue = (
            self.total_time_in_queue / self.total_number_of_planes_unloaded
            if self.total_number_of_planes_unloaded > 0
            else 0
        )
        percentage_of_time_robots_busy = (
            (self.robots_busy_time / self.config.SIMULATION_TIME) * 100
            if self.config.SIMULATION_TIME > 0
            else 0
        )

        return {
            "total_number_of_planes_unloaded": self.total_number_of_planes_unloaded,
            "number_of_planes_unloaded_per_hour": number_of_planes_unloaded_per_hour,
            "number_of_plane_in_queue": self.number_of_plane_in_queue,
            "average_time_in_queue": average_time_in_queue,
            "percentage_of_time_robots_busy": percentage_of_time_robots_busy,
        }
