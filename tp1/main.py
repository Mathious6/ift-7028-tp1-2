from tp1.src.models.airport import Airport
from tp1.config.simulation import SimulationConfig
import time

SIMULATION_DURATION = 40000


def main():
    """Main entry point for the simulation."""

    print(f"Starting simulation with {SIMULATION_DURATION} m per scenario")

    for num_robots in list(SimulationConfig.ROBOT_SCENARIOS.keys()):
        print(f"SCENARIO: {num_robots} ROBOTS")

        start_time = time.time()

        airport = Airport(num_robots=num_robots)
        airport.run_simulation(SIMULATION_DURATION)

        current_time = airport.simulator.get_current_time()
        unloaded_planes = sum(1 for p in airport.planes if p.status == airport.planes[0].status.UNLOADED)

        print(f"\nResults for {num_robots} robots:")
        print(f"> Simulation time: {current_time:.1f} minutes")
        print(f"> Total planes: {len(airport.planes)}")
        print(f"> Planes unloaded: {unloaded_planes}")
        print(f"> Current queue length: {airport.get_queue_length()}")
        print(f"> Robot utilization: {airport.get_robot_utilization(current_time):.2%}")
        print(f"> Planes per hour: {airport.get_planes_per_hour(current_time):.1f}")

        waiting_times = [p.waiting_time for p in airport.planes if p.service_start_time is not None]
        if waiting_times:
            avg_waiting_time = sum(waiting_times) / len(waiting_times)
            print(f"> Average waiting time: {avg_waiting_time:.1f} minutes")

        print(f"> Scenario execution time: {time.time() - start_time:.2f} seconds")

    print("\nAll scenarios completed!")


if __name__ == "__main__":
    main()
