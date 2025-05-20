from logging import Logger
from config.simulation_config import SimulationConfig
from config.logger import setup_logger
from models.airport import Airport


class Simulation:

    def __init__(self) -> None:

        self.config: SimulationConfig = SimulationConfig()
        self.logger: Logger = setup_logger()

    def run_scenarios(self) -> None:
        for robots_count in self.config.ROBOTs_MEAN_UNLOADING_TIMES.keys():
            self._run_scenario(robots_count)

        airport: Airport = Airport(self.config, robots_count)
        airport.manage_operations()

        simulation_results = airport.get_performance_statistics()
        self._log_simulation_results(simulation_results, robots_count)

    def _log_simulation_results(
        self, simulation_results: dict, robots_count: int
    ) -> None:
        simulation_time: int = simulation_results["simulation_time"]
        total_planes: int = simulation_results["total_planes"]
        planes_unloaded: int = simulation_results["planes_unloaded_count"]
        current_queue_length: int = simulation_results["planes_queue_lenght"]
        robot_utilization: float = simulation_results["robot_activity_ratio"]
        planes_per_hour: float = simulation_results["planes_unloaded_hourly"]
        avg_queue_waiting_time: float = simulation_results["mean_queue_time"]
        scenario_execution_time: float = simulation_results["total_time_of_operations"]

        self.logger.info(f"🤖 Results for {robots_count} robots:")
        self.logger.info(f"Simulation time: {simulation_time:.1f} minutes")
        self.logger.info(f"Total planes: {total_planes}")
        self.logger.info(f"Planes unloaded: {planes_unloaded}")
        self.logger.info(f"Current queue length: {current_queue_length}")
        self.logger.info(f"Robot utilization: {robot_utilization:.2%}")
        self.logger.info(f"Planes per hour: {planes_per_hour:.1f}")
        self.logger.info(
            f"Average queue waiting time: {avg_queue_waiting_time:.1f} minutes"
        )
        self.logger.info(
            f"Scenario execution time: {scenario_execution_time:.2f} seconds"
        )
