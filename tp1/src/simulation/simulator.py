import os
import time
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
        time_waited_by_robots : int = 0

        for index_of_time in range(1, self.config.SIMULATION_TIME * 10 + 1):
            
            if (index_of_time) % (self.config.MEAN_ARRIVAL_TIME * 10) == 0:
                airplane = Airplane()
                airplaines_waiting_queue.put(airplane)
                number_of_airplane_arrivals += 1
                print(f"Airplane {airplane.id} added to airport waiting queue at {index_of_time} time.")
            

            if remaining_robots_work_time <= 0:
                if not airplaines_waiting_queue.empty():
                    remaining_robots_work_time = self.config.ROBOT_SCENARIOS[self.config.NUMBER_OF_ROBOTS] * 10

                    airplane: Airplane = airplaines_waiting_queue.get()
                    
                    print(f"Airplane {airplane.id} begin discharging at {index_of_time} time.")
                    
                else:
                    # print("Robots are waiting for airplanes to discharge.")
                    time_waited_by_robots += 1
            
            if remaining_robots_work_time > 0:
                # print("Robots are working on discharging airplanes.")
                remaining_robots_work_time -= 1
                if remaining_robots_work_time <= 0:
                    number_of_airplane_discharged += 1
                    remaining_robots_work_time = 0
                    print(f"Airplane discharged at {index_of_time} time.")

        print(f"Simulation completed. {airplaines_waiting_queue.qsize()} airplanes left in the queue.")
        print(f"Number of airplanes arrived: {number_of_airplane_arrivals}")
        print(f"Number of airplanes discharged: {number_of_airplane_discharged}")
        print(f"Time waited by robots: {time_waited_by_robots / 10}")
        print(f"Work time remaining for robots: {remaining_robots_work_time / 10}")
        


