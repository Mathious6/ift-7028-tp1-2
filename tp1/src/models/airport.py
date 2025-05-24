from typing import List, Optional
from tp1.src.random.distributions import ExponentialDistribution
from tp1.src.models.airplane import AirPlane, PlaneStatus
from tp1.config.simulation import SimulationConfig
from tp1.config.logger import setup_logger
from tp1.src.simulation.events import Event, EventType
from tp1.src.simulation.simulator import Simulator

logger = setup_logger("airport")


class Airport:
    """Represents the airport system with its planes, robots, and queue."""

    def __init__(self, num_robots: int):
        self.config = SimulationConfig(num_robots)

        self.planes: List[AirPlane] = []  # planes in the system
        self.queue: List[AirPlane] = []  # planes waiting to be served
        self.current_plane: Optional[AirPlane] = None  # plane being served

        # We use a fixed seed for the random number generator to ensure reproducibility
        self.inter_arrival_time = ExponentialDistribution(
            mean=self.config.MEAN_ARRIVAL_TIME, seed=self.config.RANDOM_SEED
        )
        self.processing_time = ExponentialDistribution(
            mean=self.config.ROBOT_SCENARIOS[num_robots], seed=self.config.RANDOM_SEED
        )

        self.simulator = Simulator()
        self.simulator.register_handler(
            EventType.PLANE_ARRIVAL, self.handle_plane_arrival
        )
        self.simulator.register_handler(EventType.END_LOADING, self.handle_end_loading)

    def handle_plane_arrival(self, event: Event) -> None:
        """Handle a plane arrival event."""
        current_time = event.time

        plane = self.add_plane(current_time)
        self.schedule_next_arrival(current_time)
        logger.debug(
            f"Time {current_time:.1f}: Plane {plane.id:04d} arrived\t[queue: {self.get_queue_length()}]"
        )

        if self.can_start_service():
            self.start_serving_plane(current_time)

    def handle_end_loading(self, event: Event) -> None:
        """Handle an end of loading event."""
        current_time = event.time

        logger.debug(
            f"Time {current_time:.1f}: Plane {event.data.id:04d} finished\t[queue: {self.get_queue_length()}]"
        )
        self.finish_serving_plane(current_time)

    def add_plane(self, arrival_time: float) -> AirPlane:
        """Add a new plane to the system."""
        plane = AirPlane(id=len(self.planes), queue_entry_time=arrival_time)
        self.planes.append(plane)
        self.queue.append(plane)
        return plane

    def schedule_next_arrival(self, current_time: float) -> None:
        """Schedule the next plane arrival."""
        next_arrival_time = current_time + self.inter_arrival_time.generate()
        self.simulator.schedule(
            Event(time=next_arrival_time, type=EventType.PLANE_ARRIVAL)
        )

    def start_serving_plane(self, current_time: float) -> None:
        """Start serving the next plane in queue."""
        if not self.can_start_service():
            return

        self.current_plane = self.queue.pop(0)
        self.current_plane.status = PlaneStatus.BEING_SERVED
        self.current_plane.service_start_time = current_time

        service_time = self.processing_time.generate()
        service_end_time = current_time + service_time

        self.simulator.schedule(
            Event(
                time=service_end_time,
                type=EventType.END_LOADING,
                data=self.current_plane,
            )
        )
        logger.debug(
            f"Time {current_time:.1f}: Plane {self.current_plane.id:04d} served \t[delay: {service_time: .1f}m]"
        )

    def finish_serving_plane(self, current_time: float) -> None:
        """Finish serving the current plane."""
        if self.current_plane is None:
            return

        self.current_plane.status = PlaneStatus.UNLOADED
        self.current_plane.service_end_time = current_time
        self.current_plane = None

        if self.can_start_service():
            self.start_serving_plane(current_time)

    def run_simulation(self, simulation_time: float) -> None:
        """Run the simulation for the specified duration."""
        self.schedule_next_arrival(0.0)
        self.simulator.run(simulation_time)

    def get_queue_length(self) -> int:
        """Get the current length of the queue."""
        return len(self.queue)

    def get_robot_utilization(self, current_time: float) -> float:
        """Calculate the current robot utilization rate."""
        if not self.planes:
            return 0.0

        total_busy_time = sum(
            (p.service_end_time or current_time) - (p.service_start_time or current_time)
            for p in self.planes
            if p.service_start_time is not None
        )

        return total_busy_time / current_time if current_time > 0 else 0.0

    def get_planes_per_hour(self, current_time: float) -> float:
        """Calculate the number of planes served per hour."""
        if not self.planes or current_time == 0:
            return 0.0

        unloaded_planes = sum(
            1 for p in self.planes if p.status == PlaneStatus.UNLOADED
        )
        hours = current_time / 60.0
        return unloaded_planes / hours if hours > 0 else 0.0

    def can_start_service(self) -> bool:
        """Check if we can start serving a new plane."""
        return self.current_plane is None and self.get_queue_length() > 0


# python -m tp1.src.models.airport
if __name__ == "__main__":
    root_logger = setup_logger()

    NUM_ROBOTS = 2
    SIMULATION_TIME = 100

    root_logger.info("Starting airport simulation...")
    airport = Airport(num_robots=NUM_ROBOTS)
    airport.run_simulation(SIMULATION_TIME)

    current_time = airport.simulator.get_current_time()
    root_logger.info(f"Simulation results w {NUM_ROBOTS} robots:")
    root_logger.info(f"> Simulation time: {current_time:.1f} minutes")
    root_logger.info(f"> Total planes: {len(airport.planes)}")
    root_logger.info(
        f"> Planes unloaded: {sum(1 for p in airport.planes if p.status == PlaneStatus.UNLOADED)}"
    )
    root_logger.info(f"> Current queue length: {airport.get_queue_length()}")
    root_logger.info(
        f"> Robot utilization: {airport.get_robot_utilization(current_time):.2%}"
    )
    root_logger.info(
        f"> Planes per hour: {airport.get_planes_per_hour(current_time):.1f}"
    )
