def run(model, n_trials, progress=None):
    if not callable(model):
        raise ValueError("Model must be a callable function")
    if n_trials <= 0:
        raise ValueError("Number of trials must be a positive integer")
    results = []
    for i in range(n_trials):
        results.append(model())
        if progress is not None:
            progress["completed"] = i + 1
            progress["status"] = f"Running simulations ({i + 1:,}/{n_trials:,} trials)"
    return results
