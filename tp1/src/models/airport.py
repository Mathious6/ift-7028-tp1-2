from queue import Queue
import random
import threading
import time

from config.simulation import SimulationConfig
from src.models.airplane import Airplane


class Airport:

    def __init__(self, config: SimulationConfig):
        self.config: SimulationConfig = config

        self.robots_number = self.config.NUMBER_OF_ROBOTS
        self.airplanes_waiting_queue = Queue()

    def _add_airplane(self):
        """Adds an airplane to the waiting queue."""
        start_time: float = time.time()
        while time.time() - start_time < self.config.SIMULATION_TIME:
            airplane = Airplane()
            self.airplanes_waiting_queue.put(airplane)
            print(f"Airplane {airplane.id} added to airport waiting queue.")
            time.sleep(self.config.MEAN_ARRIVAL_TIME)

    def _discharge_airplanes(self):
        """Discharges an airplane from the waiting queue."""
        while True:
            if not self.airplanes_waiting_queue.empty():
                discharged_airplane: Airplane = self.airplanes_waiting_queue.get()
                discharged_airplane.discharge(self.config.ROBOT_SCENARIOS[self.robots_number])
                print(f"Airplane {discharged_airplane.id} discharged.")
                self.airplanes_waiting_queue.task_done()

    
    def launch_operation(self):
        """Launches the operation of the airport for a given time."""
        thread_airplane = threading.Thread(target=self._add_airplane, daemon=True)
        thread_discharge = threading.Thread(target=self._discharge_airplanes, daemon=True)

        thread_airplane.start()
        thread_discharge.start()

        self.airplanes_waiting_queue.join()
        print(f"Airport operation completed.")
        