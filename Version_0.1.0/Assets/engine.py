def run(model, n_trials, progress=None):
    if not callable(model):
        raise ValueError("Model must be a callable function")
    if n_trials <= 0:
        raise ValueError("Number of trials must be a positive integer")
    results = []
    for i in range(n_trials):
        results.append(model())
        if progress is not None:
            progress[0] = i + 1
    return results