import statistics as stats
def summarize(results):
    if not isinstance(results, list):
        raise ValueError("Results must be a list")
    if len(results) == 0:
        raise ValueError("Results list cannot be empty")
    summary = {
        'mean': stats.mean(results),
        'median': stats.median(results),
        'stdev': stats.stdev(results) if len(results) > 1 else 0.0,
        'min': min(results),
        'max': max(results)
    }
    return summary

def report(summary):
    if not isinstance(summary, dict):
        raise ValueError("Summary must be a dictionary")
    required_keys = {'mean', 'median', 'stdev', 'min', 'max'}
    if not required_keys.issubset(summary.keys()):
        raise ValueError(f"Summary must contain keys: {required_keys}")
    print("Summary of Results:")
    print(f"Mean: {summary['mean']:.4f}")
    print(f"Median: {summary['median']:.4f}")
    print(f"Standard Deviation: {summary['stdev']:.4f}")
    print(f"Minimum: {summary['min']:.4f}")
    print(f"Maximum: {summary['max']:.4f}")

def explain(summary):
    print(f"""
On average, results landed around {summary['mean']:.4f}.
Half of all trials fell below {summary['median']:.4f} (the median).
Results varied with a spread of {summary['stdev']:.4f} on average.
The lowest result was {summary['min']:.4f} and the highest was {summary['max']:.4f}.
""")