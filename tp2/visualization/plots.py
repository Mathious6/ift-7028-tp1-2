import matplotlib.pyplot as plt


class SimulationPlots:
    @staticmethod
    def plot_planes_unloaded_hourly(
        robots_count: int, planes_unloaded_hourly_per_hour: dict[int, float]
    ) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(20, 5))

        time_frames = planes_unloaded_hourly_per_hour.keys()
        planes_unloaded_hourly = planes_unloaded_hourly_per_hour.values()
        ax.plot(time_frames, planes_unloaded_hourly, marker=".", markersize=4)

        ax.set_title(f"Mean Number of Planes Unloaded (Cumulative Average) with {robots_count} Robots")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel(f"Mean planes unloaded per 60 minutes")
        ax.grid(True, linestyle="--", alpha=0.7)
        # ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_queue_length(
        robots_count: int, mean_queue_lengths_per_minutes: dict[int, float]
    ) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(20, 5))

        time_frames = mean_queue_lengths_per_minutes.keys()
        mean_queue_lengths = mean_queue_lengths_per_minutes.values()
        ax.plot(time_frames, mean_queue_lengths, marker=".", markersize=4)

        ax.set_title(f"Mean Queue Length Over Time (Cumulative Average) with {robots_count} Robots")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel(f"Mean number of planes in queue per minute")
        ax.grid(True, linestyle="--", alpha=0.7)
        # ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_waiting_time(robots_count: int, mean_queue_time_per_minutes: dict[int, float]) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(20, 5))

        time_frames = mean_queue_time_per_minutes.keys()
        mean_queue_times = mean_queue_time_per_minutes.values()
        ax.plot(time_frames, mean_queue_times, marker=".", markersize=4)

        ax.set_title(f"Mean Waiting Time Over Time (Cumulative Average) with {robots_count} Robots")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Mean waiting time (minutes)")
        ax.grid(True, linestyle="--", alpha=0.7)
        # ax.legend()
        return fig, ax

    @staticmethod
    def plot_mean_robot_utilization_hourly(
        robots_counts: int, robots_utilization_hourly: dict[int, float]
    ) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=(20, 5))

        time_frames = robots_utilization_hourly.keys()
        robots_utilization = robots_utilization_hourly.values()
        ax.plot(time_frames, robots_utilization, marker=".", markersize=4)

        ax.set_title(f"Mean Robot Utilization Rate Over Time (Cumulative Average) with {robots_counts} Robots")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Mean utilization rate")
        ax.grid(True, linestyle="--", alpha=0.7)
        # ax.legend()
        ax.set_ylim(0, 1)
        return fig, ax

    @staticmethod
    def plot_all_metrics(
        scenarios: dict[int, dict],
    ) -> None:

        # planes_unloaded_hourly_scenarios = {}
        # mean_queue_length_scenarios = {}
        # mean_waiting_time_scenarios = {}
        # mean_robot_utilization_hourly_scenarios = {}
        # for robots_count, hourly_statistics in scenarios.items():
        #     planes_unloaded_hourly_scenarios[robots_count] = hourly_statistics["planes_unloaded_hourly"]
        #     mean_queue_length_scenarios[robots_count] = hourly_statistics["planes_queue_lenght_over_time"]
        #     mean_waiting_time_scenarios[robots_count] = hourly_statistics["mean_queue_time_over_time"]
        #     mean_robot_utilization_hourly_scenarios[robots_count] = hourly_statistics["cumulative_robots_activity_ratio"]

        for robots_count in scenarios.keys():

            _, ax_unloaded = SimulationPlots.plot_planes_unloaded_hourly(
                robots_count, scenarios[robots_count]["planes_unloaded_hourly"]
            )
            _, ax_queue = SimulationPlots.plot_mean_queue_length(
                robots_count, scenarios[robots_count]["planes_queue_lenght_over_time"]
            )
            _, ax_waiting = SimulationPlots.plot_mean_waiting_time(
                robots_count, scenarios[robots_count]["mean_queue_time_over_time"]
            )
            _, ax_utilization = SimulationPlots.plot_mean_robot_utilization_hourly(
                robots_count, scenarios[robots_count]["cumulative_robots_activity_ratio"]
            )

            _, axes = plt.subplots(4, 1, figsize=(15, 20))

            for ax_src, ax_dst in [(ax_unloaded, axes[0]), (ax_queue, axes[1]), (ax_waiting, axes[2]), (ax_utilization, axes[3])]:
                for line in ax_src.get_lines():
                    ax_dst.plot(line.get_xdata(), line.get_ydata(), label=line.get_label(), marker=".", markersize=4)

                ax_dst.set_title(ax_src.get_title())
                ax_dst.set_xlabel(ax_src.get_xlabel())
                ax_dst.set_ylabel(ax_src.get_ylabel())

                ax_dst.grid(True, linestyle="--", alpha=0.7)
                # ax_dst.legend()

                if ax_src == ax_utilization:
                    ax_dst.set_ylim(0, 1)

            plt.tight_layout()
            plt.savefig(f"metrics_with_{robots_count}_robots_tp2.png", dpi=300, bbox_inches="tight")
            plt.close()

            plt.close(ax_unloaded.figure)
            plt.close(ax_queue.figure)
            plt.close(ax_waiting.figure)
            plt.close(ax_utilization.figure)
