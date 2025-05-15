from src.simulation.simulator import Simulator
from config.simulation import SimulationConfig
from src.visualization.plots import SimulationPlots
from src.statistics.metrics import PerformanceMetrics
from src.models.airport import Airport


def main():
    """Main entry point for the simulation."""
    
    config: SimulationConfig = SimulationConfig()
    airport: Airport = Airport(config)
    airport.launch_operation()

if __name__ == "__main__":
    main()
