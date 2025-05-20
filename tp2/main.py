from airport import Airport
from config.config import SimulationConfig


def main():
    config: SimulationConfig = SimulationConfig()
    simulation = Airport(config, 12)
    simulation.manage_airport_operations()

    simulation_results = simulation.get_performance_statistics()
    print(f"planes unloaded count: {simulation_results['planes_unloaded_count']}")
    print(f"planes unloaded hourly: {simulation_results['planes_unloaded_hourly']}")
    print(f"number of plane in queue: {simulation_results['number_of_plane_in_queue']}")
    print(f"mean queue time: {simulation_results['mean_queue_time']}")
    print(f"robot_activity_ratio: {simulation_results['robot_activity_ratio']}")
          
    
if __name__ == "__main__":
    main()
