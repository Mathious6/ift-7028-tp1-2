from src.models.airport import Airport
from src.models.airplane import AirPlane
from config.simulation import SimulationConfig
from src.visualization.plots import SimulationPlots
from src.simulation.analyzer import SimulationAnalyzer
from config.logger import setup_logger
import time

RUN_VISUALIZATION = False
SIMULATION_DURATION = 40000
WINDOW_SIZE = 60
NUM_REPLICATIONS = 50
WARMUP_PERIOD = 0


def main():
    """Main entry point for the simulation."""
    root_logger = setup_logger()

    root_logger.info(f"Starting simulation analysis with {NUM_REPLICATIONS} replications per scenario")
    root_logger.info(f"Simulation duration: {SIMULATION_DURATION} minutes")
    root_logger.info(f"Warmup period: {WARMUP_PERIOD} minutes")

    analyzer = SimulationAnalyzer(num_replications=NUM_REPLICATIONS, warmup_period=WARMUP_PERIOD)
    results = analyzer.analyze_all_scenarios(SIMULATION_DURATION)
    analyzer.print_results_table(results)

    if RUN_VISUALIZATION:
        root_logger.info("Running single simulation for visualization...")
        scenarios = {}
        for num_robots in SimulationConfig.ROBOT_SCENARIOS.keys():
            start_time = time.time()

            airport = Airport(num_robots=num_robots)
            airport.run_simulation(SIMULATION_DURATION)

            current_time = airport.simulator.get_current_time()
            unloaded_planes = AirPlane.count_unloaded_by_time(airport.planes, current_time)
            queue_waiting_time = AirPlane.calculate_mean_waiting_time(airport.planes, current_time)

            root_logger.info(f"🤖 Results for {num_robots} robots (single run):")
            root_logger.info(f"Simulation time: {current_time:.1f} minutes")
            root_logger.info(f"Total planes: {len(airport.planes)}")
            root_logger.info(f"Planes unloaded: {unloaded_planes}")
            root_logger.info(f"Planes per hour: {airport.get_planes_per_hour(current_time):.1f}")
            root_logger.info(f"Current queue length: {airport.get_queue_length()}")
            root_logger.info(f"Average queue waiting time: {queue_waiting_time:.1f} minutes")
            root_logger.info(f"Robot utilization: {airport.get_robot_utilization(current_time):.2%}")
            root_logger.info(f"Scenario execution time: {time.time() - start_time:.2f} seconds")

            scenarios[num_robots] = airport.planes

        # SimulationPlots.plot_all_metrics(scenarios, SIMULATION_DURATION, WINDOW_SIZE)


if __name__ == "__main__":
    main()
