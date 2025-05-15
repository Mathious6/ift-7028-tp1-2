import random
import math


class RandomDistributions:
    """Class for generating random numbers from various distributions."""

    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)


# DOC: https://fr.wikipedia.org/wiki/Loi_exponentielle
class ExponentialDistribution(RandomDistributions):
    """Class for generating random numbers from an exponential distribution."""

    def __init__(self, mean: float, seed: int = None):
        super().__init__(seed)
        self.mean = mean
        self.lambda_ = 1 / self.mean  # Rate parameter (λ)

    def generate(self) -> float:
        """Generate a random number from an exponential distribution."""
        u = random.random()  # Uniform random number in [0,1)
        return - (1 / self.lambda_) * math.log(1 - u)


if __name__ == "__main__":
    inter_arrival_time = ExponentialDistribution(mean=12.3, seed=42)
    print("Temps entre arrivées d'avions (minutes):")
    for i in range(5):
        time = inter_arrival_time.generate()
        print(f"  Avion {i+1}: {time:.2f} minutes")
