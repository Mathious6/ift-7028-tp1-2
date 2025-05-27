from config.simulation_config import SimulationConfig
from models.airport import Airport
from prettytable import PrettyTable
from scipy import stats
import numpy as np


class SimulationTable:
    @staticmethod
    def run_scenario_replications(num_robots: int, warmup_period: int = 12500, num_replications: int = 30) -> list[dict]:
        replication_stats: list = []

        for i in range(num_replications):
            config: SimulationConfig = SimulationConfig()
            config.RANDOM_SEED = 42 + i
            airport: Airport = Airport(config=config, robots_count=num_robots)
            airport.manage_operations()
            stats: dict = airport.get_time_performance_statistics()
            warmed_up_stats = {}
            for metric in stats.keys():
                warmed_up_stats[metric] = {}
                for time_frame, value in stats[metric].items():
                    if time_frame >= warmup_period:
                        warmed_up_stats[metric][time_frame] = value
            replication_stats.append(warmed_up_stats)
        return replication_stats

    @staticmethod
    def calculate_confidence_intervals(replication_stats: list[dict]) -> dict:
        """Calculate 95% confidence intervals for each metric."""
        metrics = [
            "planes_unloaded_hourly",
            "planes_queue_lenght_over_time",
            "mean_queue_time_over_time",
            "cumulative_robots_activity_ratio",
        ]
        results = {}

        for metric in metrics:
            values = [stats[metric].values() for stats in replication_stats]
            values = [item for sublist in values for item in sublist]
            mean = np.mean(values)
            std_err = stats.sem(values)
            ci = stats.t.interval(0.95, len(values) - 1, loc=mean, scale=std_err)

            results[metric] = (mean, ci[0], ci[1])

        return results

    @staticmethod
    def analyze_all_scenarios() -> dict:
        results = {}
        for num_robots in SimulationConfig.ROBOTS_MEAN_UNLOADING_TIMES.keys():
            replication_stats = SimulationTable.run_scenario_replications(num_robots)
            results[num_robots] = SimulationTable.calculate_confidence_intervals(replication_stats)
        return results

    @staticmethod
    def generate_table() -> PrettyTable:
        metrics = [
            "planes_unloaded_hourly",
            "planes_queue_lenght_over_time",
            "mean_queue_time_over_time",
            "cumulative_robots_activity_ratio",
        ]
        table = PrettyTable()
        table.field_names = ["Robots"] + list(SimulationConfig.ROBOTS_MEAN_UNLOADING_TIMES.keys())
        results = SimulationTable.analyze_all_scenarios()

        for metric in metrics:
            row = []
            for num_robots, stats in results.items():
                mean, ci_lower, ci_upper = stats[metric]
                row.append(f"{mean:>8.2f} ± {ci_upper-mean:>5.2f}")
            table.add_row([metric] + row)

        return table
