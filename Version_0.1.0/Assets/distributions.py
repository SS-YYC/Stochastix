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