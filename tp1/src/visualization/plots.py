from src.models.airplane import AirPlane
import matplotlib.pyplot as plt


class SimulationPlots:
    @staticmethod
    def plot_mean_unloaded_planes(
        scenarios: dict[int, list[AirPlane]], simulation_duration: int, window_size: int
    ) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the mean number of planes unloaded from the start of simulation up to each time point.
        Returns the figure and axes for further customization or combination with other plots.
        """
        fig, ax = plt.subplots(figsize=(20, 5))
        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            mean_planes = [AirPlane.calculate_mean_unloaded_rate(planes, window_end, window_size) for window_end in time_windows]
            ax.plot(time_windows, mean_planes, label=f"{scenario_num} robots", marker=".", markersize=4)

        ax.set_title("Mean Number of Planes Unloaded (Cumulative Average)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel(f"Mean planes unloaded per {window_size} minutes")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_queue_length(
        scenarios: dict[int, list], simulation_duration: int, window_size: int = 600
    ) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the mean queue length from the start of simulation up to each time point.
        Returns the figure and axes for further customization or combination with other plots.
        """
        fig, ax = plt.subplots(figsize=(20, 5))
        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            mean_queue_lengths = AirPlane.calculate_cumulative_mean_queue_length(planes, simulation_duration, window_size)
            ax.plot(time_windows, mean_queue_lengths, label=f"{scenario_num} robots", marker=".", markersize=4)

        ax.set_title("Mean Queue Length Over Time (Cumulative Average)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel(f"Mean number of planes in queue per {window_size} minutes")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_waiting_time(
        scenarios: dict[int, list], simulation_duration: int, window_size: int = 600
    ) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the mean waiting time from the start of simulation up to each time point.
        Returns the figure and axes for further customization or combination with other plots.
        """
        fig, ax = plt.subplots(figsize=(20, 5))
        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            mean_waiting_times = [AirPlane.calculate_mean_waiting_time(planes, window_end) for window_end in time_windows]
            ax.plot(time_windows, mean_waiting_times, label=f"{scenario_num} robots", marker=".", markersize=4)

        ax.set_title("Mean Waiting Time Over Time (Cumulative Average)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Mean waiting time (minutes)")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_robot_utilization(
        scenarios: dict[int, list], simulation_duration: int, window_size: int = 600
    ) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the mean robot utilization rate from the start of simulation up to each time point.
        Returns the figure and axes for further customization or combination with other plots.
        """
        fig, ax = plt.subplots(figsize=(20, 5))
        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            mean_utilization_rates = [
                AirPlane.calculate_mean_robot_utilization(planes, window_end) for window_end in time_windows
            ]
            ax.plot(time_windows, mean_utilization_rates, label=f"{scenario_num} robots", marker=".", markersize=4)

        ax.set_title("Mean Robot Utilization Rate Over Time (Cumulative Average)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Mean utilization rate")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()
        ax.set_ylim(0, 1)
        return fig, ax

    @staticmethod
    def plot_all_metrics(
        scenarios: dict[int, list[AirPlane]],
        simulation_duration: int,
        window_size: int = 600,
    ) -> None:
        """
        Create a single figure with all four metrics plots arranged vertically.
        - scenarios (dict[int, list]): Dictionary mapping scenario number to list of AirPlane objects
        - simulation_duration (int): Total duration of simulation in minutes
        - window_size (int): Size of time windows in minutes for sampling
        """
        _, ax_unloaded = SimulationPlots.plot_mean_unloaded_planes(scenarios, simulation_duration, window_size)
        _, ax_queue = SimulationPlots.plot_mean_queue_length(scenarios, simulation_duration, window_size)
        _, ax_waiting = SimulationPlots.plot_mean_waiting_time(scenarios, simulation_duration, window_size)
        _, ax_utilization = SimulationPlots.plot_mean_robot_utilization(scenarios, simulation_duration, window_size)

        _, axes = plt.subplots(4, 1, figsize=(15, 20))

        # Copy data from individual plots to subplots
        for ax_src, ax_dst in [(ax_unloaded, axes[0]), (ax_queue, axes[1]), (ax_waiting, axes[2]), (ax_utilization, axes[3])]:
            for line in ax_src.get_lines():
                ax_dst.plot(line.get_xdata(), line.get_ydata(), label=line.get_label(), marker=".", markersize=4)

            ax_dst.set_title(ax_src.get_title())
            ax_dst.set_xlabel(ax_src.get_xlabel())
            ax_dst.set_ylabel(ax_src.get_ylabel())

            ax_dst.grid(True, linestyle="--", alpha=0.7)
            ax_dst.legend()

            if ax_src == ax_utilization:
                ax_dst.set_ylim(0, 1)

        plt.tight_layout()
        plt.savefig("all_metrics_tp1.png", dpi=300, bbox_inches="tight")
        plt.close()

        plt.close(ax_unloaded.figure)
        plt.close(ax_queue.figure)
        plt.close(ax_waiting.figure)
        plt.close(ax_utilization.figure)
