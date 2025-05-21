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
    def plot_mean_unloaded_planes(
        scenarios: dict[int, list[AirPlane]], simulation_duration: int, window_size: int
    ) -> None:
        """
        Plot the mean number of planes unloaded from the start of simulation up to each time point.
        - scenarios (dict[int, list]): Dictionary mapping scenario number to list of AirPlane objects
        - simulation_duration (int): Total duration of simulation in minutes
        - window_size (int): Size of time windows in minutes for calculating means
        """
        plt.figure(figsize=(20, 5))

        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            mean_planes = [
                AirPlane.calculate_mean_unloaded_rate(planes, window_end, window_size)
                for window_end in time_windows
            ]

            plt.plot(
                time_windows,
                mean_planes,
                label=f"{scenario_num} robots",
                marker=".",
                markersize=4,
            )

        plt.title("Mean Number of Planes Unloaded (Cumulative Average)")
        plt.xlabel("Time (minutes)")
        plt.ylabel(f"Mean planes unloaded per {window_size} minutes")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        plt.savefig("unloaded_mean_planes.png")
        plt.close()

    @staticmethod
    def plot_mean_queue_length(
        scenarios: dict[int, list], simulation_duration: int, window_size: int = 600
    ) -> None:
        """
        Plot the mean queue length from the start of simulation up to each time point.
        - scenarios (dict[int, list]): Dictionary mapping scenario number to list of AirPlane objects
        - simulation_duration (int): Total duration of simulation in minutes
        - window_size (int): Size of time windows in minutes for sampling
        """
        plt.figure(figsize=(20, 5))

        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            mean_queue_lengths = []
            total_queue_time = 0

            for window_end in time_windows:
                total_queue_time = sum(
                    min(window_end, plane.service_start_time or window_end)
                    - plane.queue_entry_time
                    for plane in planes
                    if plane.queue_entry_time is not None
                    and plane.queue_entry_time <= window_end
                )

                mean_queue = total_queue_time / window_end if window_end > 0 else 0
                mean_queue_lengths.append(mean_queue)

            plt.plot(
                time_windows,
                mean_queue_lengths,
                label=f"{scenario_num} robots",
                marker=".",
                markersize=4,
            )

        plt.title("Mean Queue Length Over Time (Cumulative Average)")
        plt.xlabel("Time (minutes)")
        plt.ylabel(f"Mean number of planes in queue per {window_size} minutes")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        plt.savefig("queue_mean_length.png")
        plt.close()

    @staticmethod
    def plot_mean_waiting_time(
        scenarios: dict[int, list], simulation_duration: int, window_size: int = 600
    ) -> None:
        """
        Plot the mean waiting time from the start of simulation up to each time point.
        - scenarios (dict[int, list]): Dictionary mapping scenario number to list of AirPlane objects
        - simulation_duration (int): Total duration of simulation in minutes
        - window_size (int): Size of time windows in minutes for sampling
        """
        plt.figure(figsize=(20, 5))

        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            mean_waiting_times = []

            for window_end in time_windows:
                completed_planes = [
                    plane.waiting_time
                    for plane in planes
                    if (
                        plane.service_end_time is not None
                        and plane.service_end_time <= window_end
                        and plane.waiting_time is not None
                    )
                ]

                mean_waiting = (
                    sum(completed_planes) / len(completed_planes)
                    if completed_planes
                    else 0
                )
                mean_waiting_times.append(mean_waiting)

            plt.plot(
                time_windows,
                mean_waiting_times,
                label=f"{scenario_num} robots",
                marker=".",
                markersize=4,
            )

        plt.title("Mean Waiting Time Over Time (Cumulative Average)")
        plt.xlabel("Time (minutes)")
        plt.ylabel("Mean waiting time (minutes)")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        plt.savefig("waiting_time_mean.png")
        plt.close()

    @staticmethod
    def plot_mean_robot_utilization(
        scenarios: dict[int, list], simulation_duration: int, window_size: int = 600
    ) -> None:
        """
        Plot the mean robot utilization rate from the start of simulation up to each time point.
        - scenarios (dict[int, list]): Dictionary mapping scenario number to list of AirPlane objects
        - simulation_duration (int): Total duration of simulation in minutes
        - window_size (int): Size of time windows in minutes for sampling
        """
        plt.figure(figsize=(20, 5))

        time_windows = range(0, simulation_duration, window_size)

        for scenario_num, planes in scenarios.items():
            mean_utilization_rates = []

            for window_end in time_windows:
                total_service_time = sum(
                    min(window_end, plane.service_end_time or window_end)
                    - plane.service_start_time
                    for plane in planes
                    if (
                        plane.service_start_time is not None
                        and plane.service_start_time <= window_end
                    )
                )

                total_robot_minutes = total_service_time * scenario_num
                elapsed_minutes = window_end * scenario_num
                mean_utilization = (
                    total_robot_minutes / elapsed_minutes if elapsed_minutes > 0 else 0
                )
                mean_utilization_rates.append(mean_utilization)

            plt.plot(
                time_windows,
                mean_utilization_rates,
                label=f"{scenario_num} robots",
                marker=".",
                markersize=4,
            )

        plt.title("Mean Robot Utilization Rate Over Time (Cumulative Average)")
        plt.xlabel("Time (minutes)")
        plt.ylabel("Mean utilization rate")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        plt.ylim(0, 1)  # Utilization rate is between 0 and 1
        plt.savefig("robot_utilization_mean.png")
        plt.close()
