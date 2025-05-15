from src.models.airplane import Airplane
from .events import Event
from queue import Queue

class Simulator:
    def __init__(self, config: dict):
        """Initialize the simulator with configuration parameters."""
        self.config = config

    def run_simulation(self):
        """Run a single simulation replication for a given scenario."""
        airplaines_waiting_queue = Queue()
        remaining_robots_work_time: int = 0

        number_of_airplane_arrivals : int = 0
        number_of_airplane_discharged : int = 0

        for index_of_time in range(self.config.SIMULATION_TIME):
            
            if (index_of_time * 10) % (self.config.MEAN_ARRIVAL_TIME * 10) == 0:
                airplane = Airplane()
                airplaines_waiting_queue.put(airplane)
                number_of_airplane_arrivals += 1
                print(f"Airplane {airplane.id} added to airport waiting queue.")
            
            if remaining_robots_work_time > 0:
                remaining_robots_work_time -= 1
                if remaining_robots_work_time == 0:
                    number_of_airplane_discharged += 1

            else:
                if not airplaines_waiting_queue.empty():
                    remaining_robots_work_time = self.config.ROBOT_SCENARIOS[self.config.NUMBER_OF_ROBOTS]

                    airplane: Airplane = airplaines_waiting_queue.get()
                    
                    print(f"Airplane {airplane.id} discharging.")

        print(f"Simulation completed. {airplaines_waiting_queue.qsize()} airplanes left in the queue.")
        print(f"Number of airplanes arrived: {number_of_airplane_arrivals}")
        print(f"Number of airplanes discharged: {number_of_airplane_discharged}")
        


