import matplotlib.pyplot as plt


class SimulationPlots:
    @staticmethod
    def plot_planes_unloaded_hourly(
        scenarios: dict[int, dict]
    ) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(20, 5))

        for robots_count, planes_unloaded_hourly_per_hour in scenarios.items():
            time_frames = planes_unloaded_hourly_per_hour.keys()
            planes_unloaded_hourly = planes_unloaded_hourly_per_hour.values()     
            ax.plot(time_frames, planes_unloaded_hourly, label=f"{robots_count} robots", marker=".", markersize=4)

        ax.set_title("Mean Number of Planes Unloaded (Cumulative Average)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel(f"Mean planes unloaded per 60 minutes")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_queue_length(
        scenarios: dict[int, dict]
    ) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(20, 5))

        for robots_count, mean_queue_lengths_per_minutes in scenarios.items():
            time_frames = mean_queue_lengths_per_minutes.keys()
            mean_queue_lengths = mean_queue_lengths_per_minutes.values()
            ax.plot(time_frames, mean_queue_lengths, label=f"{robots_count} robots", marker=".", markersize=4)

        ax.set_title("Mean Queue Length Over Time (Cumulative Average)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel(f"Mean number of planes in queue per minute")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_waiting_time(
        scenarios: dict[int, dict]
    ) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(20, 5))

        for robots_count, mean_queue_time_per_minutes in scenarios.items():
            time_frames = mean_queue_time_per_minutes.keys()
            mean_queue_times = mean_queue_time_per_minutes.values()
            ax.plot(time_frames, mean_queue_times, label=f"{robots_count} robots", marker=".", markersize=4)

        ax.set_title("Mean Waiting Time Over Time (Cumulative Average)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Mean waiting time (minutes)")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_robot_utilization_hourly(
        scenarios: dict[int, dict]
    ) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(20, 5))

        for robots_count, robots_utilization_hourly in scenarios.items():
            time_frames = robots_utilization_hourly.keys()
            robots_utilization = robots_utilization_hourly.values()
            ax.plot(time_frames, robots_utilization, label=f"{robots_count} robots", marker=".", markersize=4)

        ax.set_title("Mean Robot Utilization Rate Over Time (Cumulative Average)")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Mean utilization rate")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.legend()
        ax.set_ylim(0, 1)
        return fig, ax

    @staticmethod
    def plot_all_metrics(
        scenarios: dict[int, dict],
    ) -> None:
        
        planes_unloaded_hourly_scenarios = {}
        mean_queue_length_scenarios = {}
        mean_waiting_time_scenarios = {}
        mean_robot_utilization_hourly_scenarios = {}
        for robots_count, hourly_statistics in scenarios.items():
            planes_unloaded_hourly_scenarios[robots_count] = hourly_statistics["planes_unloaded_hourly"]
            mean_queue_length_scenarios[robots_count] = hourly_statistics["planes_queue_lenght_over_time"]
            mean_waiting_time_scenarios[robots_count] = hourly_statistics["mean_queue_time_over_time"]
            mean_robot_utilization_hourly_scenarios[robots_count] = hourly_statistics["cumulative_robots_activity_ratio"]


        _, ax_unloaded = SimulationPlots.plot_planes_unloaded_hourly(planes_unloaded_hourly_scenarios)
        _, ax_queue = SimulationPlots.plot_mean_queue_length(mean_queue_length_scenarios)
        _, ax_waiting = SimulationPlots.plot_mean_waiting_time(mean_waiting_time_scenarios)
        _, ax_utilization = SimulationPlots.plot_mean_robot_utilization_hourly(mean_robot_utilization_hourly_scenarios)

        _, axes = plt.subplots(4, 1, figsize=(15, 20))

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
        plt.savefig("all_metrics_tp2.png", dpi=300, bbox_inches="tight")
        plt.close()

        plt.close(ax_unloaded.figure)
        plt.close(ax_queue.figure)
        plt.close(ax_waiting.figure)
        plt.close(ax_utilization.figure)
