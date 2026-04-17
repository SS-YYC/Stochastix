import random


def uniform(a, b, n):
    results = []
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    if n <= 0:
        raise ValueError("Number of samples must be a positive integer")
    for i in range(n):
        results.append(random.uniform(a, b))
    return results


def sample_uniform(a, b):
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    return random.uniform(a, b)


def sample_coin_flip():
    return random.choice(["Heads", "Tails"])


def sample_die_roll(sides=6):
    if sides <= 1:
        raise ValueError("A die must have at least 2 sides")
    return random.randint(1, sides)
