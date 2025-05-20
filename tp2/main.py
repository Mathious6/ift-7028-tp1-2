from models.simulation import Simulation


def main():
    simulation: Simulation = Simulation()
    simulation.run_scenarios()


if __name__ == "__main__":
    main()
