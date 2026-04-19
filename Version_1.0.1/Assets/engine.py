from Assets.results import StreamingSummary


class SimulationCancelled(Exception):
    pass


def run(model, n_trials, progress=None, cancel_event=None):
    if not callable(model):
        raise ValueError("Model must be a callable function")
    if n_trials <= 0:
        raise ValueError("Number of trials must be a positive integer")

    summary = StreamingSummary()
    for i in range(n_trials):
        if cancel_event is not None and cancel_event.is_set():
            raise SimulationCancelled("Simulation cancelled by user")

        result = model()
        summary.add(result)

        if progress is not None:
            progress["completed"] = i + 1
            progress["status"] = f"Running simulations ({i + 1:,}/{n_trials:,} trials)"
    return summary.finalize()
