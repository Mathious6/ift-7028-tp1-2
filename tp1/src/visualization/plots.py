from tp1.src.models.airplane import AirPlane
import matplotlib.pyplot as plt


class SimulationPlots:
    @staticmethod
    def plot_warmup_period(metrics: dict, scenario: int) -> None:
        """Plot metrics to determine warmup period."""
        pass

    @staticmethod
    def plot_confidence_intervals(results: dict) -> None:
        """Plot confidence intervals for all scenarios."""
        pass

    @staticmethod
    def plot_comparison_scenarios(results: dict) -> None:
        """Plot comparison between different scenarios."""
        pass

    @staticmethod
    def plot_unloaded_planes(scenarios: dict[int, list], simulation_duration: int, window_size: int = 600) -> None:
        """
        Plot the number of planes unloaded over time for all scenarios.
        - scenarios (dict[int, list]): Dictionary mapping scenario number to list of AirPlane objects
        - simulation_duration (int): Total duration of simulation in minutes
        """
        plt.figure(figsize=(20, 5))

        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            planes_per_hour = []

            for window_start in time_windows:
                window_end = window_start + window_size
                planes_in_window = sum(
                    1 for plane in planes
                    if plane.service_end_time is not None
                    and window_start <= plane.service_end_time < window_end
                )
                planes_per_hour.append(planes_in_window)

            plt.plot(time_windows, planes_per_hour, label=f'{scenario_num} robots')

        plt.title('Number of Planes Unloaded per Hour by Scenario')
        plt.xlabel('Time (minutes)')
        plt.ylabel('Number of planes unloaded per hour')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.savefig('unloaded_planes_per_hour.png')
        plt.close()
