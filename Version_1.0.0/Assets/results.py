from collections import Counter
from numbers import Number
import statistics as stats


def summarize(results):
    if not isinstance(results, list):
        raise ValueError("Results must be a list")
    if len(results) == 0:
        raise ValueError("Results list cannot be empty")

    if all(isinstance(result, Number) for result in results):
        return {
            "type": "numeric",
            "mean": stats.mean(results),
            "median": stats.median(results),
            "stdev": stats.stdev(results) if len(results) > 1 else 0.0,
            "min": min(results),
            "max": max(results),
        }

    counts = Counter(results)
    total = len(results)
    ordered_outcomes = sorted(counts.items(), key=lambda item: (-item[1], str(item[0])))
    return {
        "type": "categorical",
        "total": total,
        "mode": ordered_outcomes[0][0],
        "counts": ordered_outcomes,
    }


def report(summary):
    if not isinstance(summary, dict):
        raise ValueError("Summary must be a dictionary")

    print("Summary of Results:")

    if summary.get("type") == "numeric":
        required_keys = {"mean", "median", "stdev", "min", "max"}
        if not required_keys.issubset(summary.keys()):
            raise ValueError(f"Summary must contain keys: {required_keys}")
        print(f"Mean: {summary['mean']:.4f}")
        print(f"Median: {summary['median']:.4f}")
        print(f"Standard Deviation: {summary['stdev']:.4f}")
        print(f"Minimum: {summary['min']:.4f}")
        print(f"Maximum: {summary['max']:.4f}")
        return

    if summary.get("type") == "categorical":
        required_keys = {"total", "mode", "counts"}
        if not required_keys.issubset(summary.keys()):
            raise ValueError(f"Summary must contain keys: {required_keys}")
        print(f"Most common outcome: {summary['mode']}")
        for outcome, count in summary["counts"]:
            pct = (count / summary["total"]) * 100
            print(f"{outcome}: {count:,} ({pct:.2f}%)")
        return

    raise ValueError("Summary type must be 'numeric' or 'categorical'")


def explain(summary):
    if summary.get("type") == "numeric":
        print(f"""
On average, results landed around {summary['mean']:.4f}.
Half of all trials fell below {summary['median']:.4f} (the median).
Results varied with a spread of {summary['stdev']:.4f} on average.
The lowest result was {summary['min']:.4f} and the highest was {summary['max']:.4f}.
""")
        return

    if summary.get("type") == "categorical":
        total = summary["total"]
        most_common = summary["counts"][0]
        least_common = summary["counts"][-1]
        print(f"""
Across {total:,} trials, the most common outcome was {most_common[0]} with {most_common[1]:,} results.
The least common outcome was {least_common[0]} with {least_common[1]:,} results.
These percentages show how the random outcomes were distributed across the simulation.
""")
        return

    raise ValueError("Summary type must be 'numeric' or 'categorical'")
