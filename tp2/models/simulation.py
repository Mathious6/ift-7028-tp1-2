from logging import Logger
from config.simulation_config import SimulationConfig
from config.logger import setup_logger
from models.airport import Airport
from visualization.plots import SimulationPlots
from visualization.tables import SimulationTable


class Simulation:
    def __init__(self) -> None:

        self.config: SimulationConfig = SimulationConfig()
        self.logger: Logger = setup_logger()

    def run_scenarios(self, generate_plots: bool = True, generate_table: bool = True) -> None:
        scenarios_statistics: dict = {}
        for robots_count in self.config.ROBOTS_MEAN_UNLOADING_TIMES.keys():
            scenarios_statistics[robots_count] = self.run_scenario(
                robots_count, print_final_statistic=True, print_timely_statistics=False
            )
        if generate_table:
            print(SimulationTable.generate_table())
        if generate_plots:
            SimulationPlots.plot_all_metrics(scenarios=scenarios_statistics)

    def run_scenario(self, robots_count: int, print_final_statistic: bool = False, print_timely_statistics: bool = False) -> dict:
        airport: Airport = Airport(self.config, robots_count)
        airport.manage_operations()

        if print_final_statistic:
            simulation_results = airport.get_final_performance_statistics()
            self._log_simulation_results(simulation_results, robots_count)
        if print_timely_statistics:
            hourly_statistics = airport.get_time_performance_statistics()
            self._log_timely_statistics(hourly_statistics)

        return airport.get_time_performance_statistics()

    def _log_simulation_results(self, simulation_results: dict, robots_count: int) -> None:
        simulation_time: int = simulation_results["simulation_time"]
        total_planes: int = simulation_results["total_planes"]
        planes_unloaded: int = simulation_results["planes_unloaded_count"]
        current_queue_length: int = simulation_results["planes_queue_lenght"]
        robot_utilization: float = simulation_results["robot_activity_ratio"]
        planes_per_hour: float = simulation_results["planes_unloaded_hourly"]
        avg_queue_waiting_time: float = simulation_results["mean_queue_time"]
        scenario_execution_time: float = simulation_results["total_time_of_operations"]

        print("=" * 100)
        self.logger.info(f"🤖 Results for {robots_count} robots:")
        self.logger.info(f"Simulation time: {simulation_time:.1f} minutes")
        self.logger.info(f"Total planes: {total_planes}")
        self.logger.info(f"Planes unloaded: {planes_unloaded}")
        self.logger.info(f"Current queue length: {current_queue_length}")
        self.logger.info(f"Robot utilization: {robot_utilization:.2%}")
        self.logger.info(f"Planes per hour: {planes_per_hour:.1f}")
        self.logger.info(f"Average queue waiting time: {avg_queue_waiting_time:.1f} minutes")
        self.logger.info(f"Scenario execution time: {scenario_execution_time:.2f} minutes")

    def _log_timely_statistics(self, hourly_statistics: dict, hourly_only: bool = True) -> None:
        planes_unloaded_hourly: dict = hourly_statistics["planes_unloaded_hourly"]
        planes_queue_lenght_over_time: dict = hourly_statistics["planes_queue_lenght_over_time"]
        mean_queue_time_over_time: dict = hourly_statistics["mean_queue_time_over_time"]
        robots_activity_ratio_hourly: dict = hourly_statistics["cumulative_robots_activity_ratio"]

        self.logger.info("Timely statistics:")
        if hourly_only:
            for minute in planes_unloaded_hourly.keys():
                self.logger.info(f"Hour {minute // 60}:" + "-" * (100 - len(f"Hour {minute // 60}:")))
                self.logger.info(f"Minute {minute}:")
                self.logger.info(f"Planes unloaded: {planes_unloaded_hourly[minute]:.1f}")
                self.logger.info(f"Robot activity ratio: {robots_activity_ratio_hourly[minute]:.2%}")
                self.logger.info(f"Queue length: {planes_queue_lenght_over_time[minute]:.1f}")
                self.logger.info(f"Mean queue time: {mean_queue_time_over_time[minute]:.1f} minutes")
        else:
            for minute in planes_queue_lenght_over_time.keys():
                self.logger.info(f"Minute {minute}:")
                if minute % 60 == 0:
                    self.logger.info(f"Hour {minute // 60}:" + "-" * (100 - len(f"Hour {minute // 60}:")))
                    self.logger.info(f"Planes unloaded: {planes_unloaded_hourly[minute]:.1f}")
                    self.logger.info(f"Robot activity ratio: {robots_activity_ratio_hourly[minute]:.2%}")
                self.logger.info(f"Queue length: {planes_queue_lenght_over_time[minute]:.1f}")
                self.logger.info(f"Mean queue time: {mean_queue_time_over_time[minute]:.1f} minutes")
