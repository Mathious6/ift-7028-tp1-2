from src.simulation.simulator import Simulator
from config.simulation import SimulationConfig
from src.visualization.plots import SimulationPlots
from src.statistics.metrics import PerformanceMetrics


def main():
    """Main entry point for the simulation."""
    config = SimulationConfig()

    # Run simulations for each scenario
    for scenario_id, service_time in config.ROBOT_SCENARIOS.items():
        for replication in range(config.NUM_REPLICATIONS):
            simulator = Simulator(config)
            results = simulator.run_simulation(scenario_id, replication)
            # Process and store results

    # Generate plots and reports ...
    # Calculate confidence intervals ...
    # Output final results ...


if __name__ == "__main__":
    main()
