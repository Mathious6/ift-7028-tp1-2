from tp1.src.models.airport import Airport
from tp1.config.simulation import SimulationConfig
from tp1.src.visualization.plots import SimulationPlots
from tp1.config.logger import setup_logger
import time

SIMULATION_DURATION = 40000


def main():
    """Main entry point for the simulation."""
    root_logger = setup_logger()

    root_logger.info(f"Starting simulation with {SIMULATION_DURATION}m per scenario")

    scenarios = {}

    for num_robots in list(SimulationConfig.ROBOT_SCENARIOS.keys()):
        start_time = time.time()  # only for analytics

        airport = Airport(num_robots=num_robots)
        airport.run_simulation(SIMULATION_DURATION)

        current_time = airport.simulator.get_current_time()
        unloaded_planes = sum(1 for plane in airport.planes if plane.status == airport.planes[0].status.UNLOADED)
        queue_waiting_times = [plane.waiting_time for plane in airport.planes if plane.service_start_time is not None]
        avg_queue_waiting_time = sum(queue_waiting_times) / len(queue_waiting_times)

        root_logger.info(f"🤖 Results for {num_robots} robots:")
        root_logger.info(f"Simulation time: {current_time:.1f} minutes")
        root_logger.info(f"Total planes: {len(airport.planes)}")
        root_logger.info(f"Planes unloaded: {unloaded_planes}")
        root_logger.info(f"Current queue length: {airport.get_queue_length()}")
        root_logger.info(f"Robot utilization: {airport.get_robot_utilization(current_time):.2%}")
        root_logger.info(f"Planes per hour: {airport.get_planes_per_hour(current_time):.1f}")
        root_logger.info(f"Average queue waiting time: {avg_queue_waiting_time:.1f} minutes")
        root_logger.info(f"Scenario execution time: {time.time() - start_time:.2f} seconds")

        scenarios[num_robots] = airport.planes

    SimulationPlots.plot_unloaded_planes_per_hour(scenarios, SIMULATION_DURATION)



if __name__ == "__main__":
    main()
