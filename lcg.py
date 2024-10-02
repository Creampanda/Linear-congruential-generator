class LCG:
    def __init__(
        self, multiplier: int, increment: int, modulus: int, seed: int = 1
    ) -> None:
        if not (0 <= seed < modulus):
            raise ValueError("Seed should satisfy 0 ≤ seed < modulus")
        if not (0 <= multiplier < modulus):
            raise ValueError("Multiplier should satisfy 0 ≤ multiplier < modulus")
        if not (0 <= increment < modulus):
            raise ValueError("Increment should satisfy 0 ≤ increment < modulus")
        self.a = multiplier
        self.c = increment
        self.m = modulus
        self.current = seed

    def __iter__(self):
        return self

    def __next__(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current

    def generate_numbers(self, count: int):
        return [next(self) for _ in range(count)]

    def generate_numbers_normalized(self, count: int):
        return [next(self) / self.m for _ in range(count)]
