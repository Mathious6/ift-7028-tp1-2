from simulation import Simulation

def main():
    """
    Main function to run the simulation.
    """
    simulation = Simulation()
    simulation.run()
    print("Simulation finished.")
    # Print the results
    results = simulation.get_performance_metrics()
    print(f"Total number of planes unloaded: {results['total_number_of_planes_unloaded']}")
    print(f"number of planes unloaded per hour: {results['number_of_planes_unloaded_per_hour']}")
    print(f"number of planes in queue: {results['number_of_plane_in_queue']}")
    print(f"average time in queue: {results['average_time_in_queue']}")
    print(f"percentage of time robots busy: {results['percentage_of_time_robots_busy']}")

if __name__ == "__main__":
    main()
