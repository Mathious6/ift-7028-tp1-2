from typing import Dict, List, Tuple
import numpy as np
from scipy import stats
from src.models.airport import Airport
from src.models.airplane import AirPlane
from config.simulation import SimulationConfig
from config.logger import setup_logger

logger = setup_logger("analyzer")


class SimulationAnalyzer:
    def __init__(self, num_replications: int = 30, warmup_period: int = 10000):
        """Initialize the simulation analyzer."""
        self.num_replications = num_replications
        self.warmup_period = warmup_period
        self.scenarios = SimulationConfig.ROBOT_SCENARIOS.keys()

    def run_scenario_replications(self, num_robots: int, simulation_duration: int) -> List[Dict]:
        """Run multiple replications of a scenario and collect statistics."""
        replication_stats = []

        for rep in range(self.num_replications):
            SimulationConfig.RANDOM_SEED = 42 + rep

            airport = Airport(num_robots=num_robots)
            airport.run_simulation(simulation_duration)

            stats = self._calculate_scenario_statistics(airport)
            replication_stats.append(stats)

        return replication_stats

    def _calculate_scenario_statistics(self, airport: Airport) -> Dict:
        """Calculate statistics for a single replication after warmup period."""
        post_warmup_planes = [p for p in airport.planes if p.queue_entry_time >= self.warmup_period]
        simulation_duration = airport.simulator.get_current_time() - self.warmup_period

        return {
            "planes_per_hour": AirPlane.calculate_mean_unloaded_rate(post_warmup_planes, simulation_duration, 60),
            "mean_queue_length": AirPlane.calculate_mean_queue_length(post_warmup_planes, simulation_duration),
            "mean_waiting_time": AirPlane.calculate_mean_waiting_time(post_warmup_planes, simulation_duration),
            "robot_utilization": AirPlane.calculate_mean_robot_utilization(post_warmup_planes, simulation_duration),
        }

    def calculate_confidence_intervals(self, replication_stats: List[Dict]) -> Dict[str, Tuple[float, float, float]]:
        """Calculate 95% confidence intervals for each metric."""
        metrics = ["planes_per_hour", "mean_queue_length", "mean_waiting_time", "robot_utilization"]
        results = {}

        for metric in metrics:
            values = [stats[metric] for stats in replication_stats]
            mean = np.mean(values)
            std_err = stats.sem(values)
            ci = stats.t.interval(0.95, len(values)-1, loc=mean, scale=std_err)

            results[metric] = (mean, ci[0], ci[1])

        return results

    def analyze_all_scenarios(self, simulation_duration: int) -> Dict[int, Dict[str, Tuple[float, float, float]]]:
        """Run and analyze all scenarios."""
        results = {}

        for num_robots in self.scenarios:
            logger.info(f"Analyzing scenario with {num_robots} robots...")
            replication_stats = self.run_scenario_replications(num_robots, simulation_duration)
            confidence_intervals = self.calculate_confidence_intervals(replication_stats)
            results[num_robots] = confidence_intervals

        return results

    def print_results_table(self, results: Dict[int, Dict[str, Tuple[float, float, float]]]) -> None:
        """Print a formatted table of results with confidence intervals."""
        metrics = ["planes_per_hour", "mean_queue_length", "mean_waiting_time", "robot_utilization"]
        metric_names = {
            "planes_per_hour": "Planes per hour",
            "mean_queue_length": "Mean queue length",
            "mean_waiting_time": "Mean waiting time",
            "robot_utilization": "Robot utilization",
        }

        print("\nResults with 95% Confidence Intervals")
        print("=" * 100)
        print(f"{'Metric':<20}", end="")
        for num_robots in sorted(results.keys()):
            print(f"{num_robots:>15.0f}", end="")
        print("\n" + "-" * 100)

        for metric in metrics:
            print(f"{metric_names[metric]:<20}", end="")
            for num_robots in sorted(results.keys()):
                mean, lower, upper = results[num_robots][metric]
                print(f"{mean:>8.2f} ± {upper-mean:>5.2f}", end="")
            print()

        print("=" * 100)
        print("Note: Values shown as mean ± half-width of 95% confidence interval\n")
