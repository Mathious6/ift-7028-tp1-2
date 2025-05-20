from typing import Generator
from simpy import *
from random import randint, expovariate

from config.config import SimulationConfig


class Simulation():

    def __init__(self) -> None:
        """
        Initialize the simulation.
        """
        self.config: SimulationConfig = SimulationConfig()
        self.env: Environment = Environment()
        self.robots: Resource = Resource(self.env)

        self.total_time_in_queue: float = 0.0
        self.total_number_of_planes_unloaded: int = 0
        self.number_of_plane_in_queue: int = 0
        
        # self.are_robots_busy: bool = False
        self.robots_busy_time: float = 0.0

        
    def run(self) -> None:
        """
        Run the simulation.
        """
        self.env.process(self._airplane_arrival())
        self.env.run(until=self.config.SIMULATION_TIME)
        print("Simulation finished.")
    
    def _airplane_arrival(self) -> Generator:
        while True:
            # Simule l'arrivée d'un avion
            yield self.env.timeout(expovariate(1 / self.config.MEAN_ARRIVAL_TIME))

            # Crée un nouvel avion
            self.env.process(self._airplane())

    def _airplane(self) -> Generator:
        arrival_time = self.env.now
        id: int = randint(111111111, 999999999)
        print(f"Airplane {id} arrived at {arrival_time}")
        # Incrémente le nombre d'avions dans la file d'attente
        self.number_of_plane_in_queue += 1

        # Simule l'attente de l'avion pour le déchargement
        with self.robots.request() as request:
            queue_start_waiting_time = self.env.now
            yield request # Attendre que les robots soit disponible
            queue_end_waiting_time = self.env.now
            self.total_time_in_queue += (queue_end_waiting_time - queue_start_waiting_time)

            print(f"Airplane {id} started unloading at {self.env.now}")
            # Simule le déchargement de l'avion
            self.number_of_plane_in_queue -= 1
            # self.are_robots_busy = True
            robots_busy_start_time = self.env.now

            # Le temps de déchargement correspond à une distribution exponentielle dont la moyenne est établie dans SimulationConfig
            yield self.env.timeout(expovariate(1 / self.config.ROBOT_SCENARIOS[self.config.NUMBER_OF_ROBOTS])) # Simule le temps de déchargement
            # Fin du déchargement
            self.total_number_of_planes_unloaded += 1

            robots_busy_end_time = self.env.now
            # self.are_robots_busy = False
            self.robots_busy_time += (robots_busy_end_time - robots_busy_start_time)
            print(f"Airplane {id} finished unloading at {self.env.now}")
            

    
    def get_performance_metrics(self) -> dict:
        """
        Get the performance metrics of the simulation.
        """
        number_of_planes_unloaded_per_hour = self.total_number_of_planes_unloaded / (self.config.SIMULATION_TIME / 60)
        average_time_in_queue = self.total_time_in_queue / self.total_number_of_planes_unloaded if self.total_number_of_planes_unloaded > 0 else 0
        percentage_of_time_robots_busy = (self.robots_busy_time / self.config.SIMULATION_TIME) * 100 if self.config.SIMULATION_TIME > 0 else 0
    
        return {
            "total_number_of_planes_unloaded": self.total_number_of_planes_unloaded,
            "number_of_planes_unloaded_per_hour": number_of_planes_unloaded_per_hour,
            "number_of_plane_in_queue": self.number_of_plane_in_queue,
            "average_time_in_queue": average_time_in_queue,
            "percentage_of_time_robots_busy": percentage_of_time_robots_busy
        }