from collections import Counter
import heapq
from numbers import Number


class StreamingSummary:
    def __init__(self):
        self.count = 0
        self.data_type = None
        self.all_integral = True
        self.mean = 0.0
        self.sum_squares = 0.0
        self.minimum = None
        self.maximum = None
        self.lower_half = []
        self.upper_half = []
        self.counts = Counter()

    def add(self, result):
        if self.count == 0:
            self.data_type = "numeric" if isinstance(result, Number) else "categorical"
        elif self.data_type == "numeric" and not isinstance(result, Number):
            raise ValueError("Simulation results must all be numeric or all be categorical")
        elif self.data_type == "categorical" and isinstance(result, Number):
            raise ValueError("Simulation results must all be numeric or all be categorical")

        self.count += 1

        if self.data_type == "numeric":
            self._add_numeric(result)
            return

        self.counts[result] += 1

    def _add_numeric(self, value):
        value = float(value)
        self.all_integral = self.all_integral and value.is_integer()

        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self.sum_squares += delta * delta2

        self.minimum = value if self.minimum is None else min(self.minimum, value)
        self.maximum = value if self.maximum is None else max(self.maximum, value)

        if not self.lower_half or value <= -self.lower_half[0]:
            heapq.heappush(self.lower_half, -value)
        else:
            heapq.heappush(self.upper_half, value)

        if len(self.lower_half) > len(self.upper_half) + 1:
            heapq.heappush(self.upper_half, -heapq.heappop(self.lower_half))
        elif len(self.upper_half) > len(self.lower_half):
            heapq.heappush(self.lower_half, -heapq.heappop(self.upper_half))

    def finalize(self):
        if self.count == 0:
            raise ValueError("Results list cannot be empty")

        if self.data_type == "numeric":
            if len(self.lower_half) > len(self.upper_half):
                median = -self.lower_half[0]
            else:
                median = (-self.lower_half[0] + self.upper_half[0]) / 2

            variance = self.sum_squares / (self.count - 1) if self.count > 1 else 0.0
            return {
                "type": "numeric",
                "count": self.count,
                "display_style": "integer" if self.all_integral else "decimal",
                "mean": self.mean,
                "median": median,
                "stdev": variance ** 0.5,
                "min": self.minimum,
                "max": self.maximum,
            }

        ordered_outcomes = sorted(self.counts.items(), key=lambda item: (-item[1], str(item[0])))
        return {
            "type": "categorical",
            "total": self.count,
            "mode": ordered_outcomes[0][0],
            "counts": ordered_outcomes,
        }


def summarize(results):
    if not isinstance(results, list):
        raise ValueError("Results must be a list")
    summary = StreamingSummary()
    for result in results:
        summary.add(result)
    return summary.finalize()


def add_financial_context(summary, initial_amount):
    if not isinstance(summary, dict):
        raise ValueError("Summary must be a dictionary")
    if summary.get("type") != "numeric":
        raise ValueError("Financial context can only be applied to numeric summaries")
    if initial_amount < 0:
        raise ValueError("Initial amount cannot be negative")

    summary = dict(summary)
    summary["display_style"] = "percentage"
    summary["financial"] = {
        "initial_amount": initial_amount,
        "mean": initial_amount * (1 + (summary["mean"] / 100)),
        "median": initial_amount * (1 + (summary["median"] / 100)),
        "stdev": initial_amount * (summary["stdev"] / 100),
        "min": initial_amount * (1 + (summary["min"] / 100)),
        "max": initial_amount * (1 + (summary["max"] / 100)),
    }
    return summary


def format_numeric(value, display_style):
    if display_style == "integer":
        return str(round(value))
    if display_style == "percentage":
        return f"{value:.2f}%"
    return f"{value:.4f}"


def format_currency(value):
    return f"${value:,.2f}"


def report(summary):
    if not isinstance(summary, dict):
        raise ValueError("Summary must be a dictionary")

    print("Here is the simulation summary:")

    if summary.get("type") == "numeric":
        required_keys = {"mean", "median", "stdev", "min", "max"}
        if not required_keys.issubset(summary.keys()):
            raise ValueError(f"Summary must contain keys: {required_keys}")
        display_style = summary.get("display_style", "decimal")
        print(f"Mean: {format_numeric(summary['mean'], display_style)}")
        print(f"Median: {format_numeric(summary['median'], display_style)}")
        print(f"Usual amount of variation: {format_numeric(summary['stdev'], display_style)}")
        print(f"Lowest result seen: {format_numeric(summary['min'], display_style)}")
        print(f"Highest result seen: {format_numeric(summary['max'], display_style)}")
        if "financial" in summary:
            financial = summary["financial"]
            print("")
            print("If you apply those returns to your money:")
            print(f"Starting amount: {format_currency(financial['initial_amount'])}")
            print(f"Mean ending value: {format_currency(financial['mean'])}")
            print(f"Median ending value: {format_currency(financial['median'])}")
            print(f"Typical swing in ending value: {format_currency(financial['stdev'])}")
            print(f"Lowest ending value seen: {format_currency(financial['min'])}")
            print(f"Highest ending value seen: {format_currency(financial['max'])}")
        return

    if summary.get("type") == "categorical":
        required_keys = {"total", "mode", "counts"}
        if not required_keys.issubset(summary.keys()):
            raise ValueError(f"Summary must contain keys: {required_keys}")
        print(f"Most common outcome: {summary['mode']}")
        print("Outcome breakdown:")
        for outcome, count in summary["counts"]:
            pct = (count / summary["total"]) * 100
            print(f"{outcome} came up {count:,} times ({pct:.2f}%)")
        return

    raise ValueError("Summary type must be 'numeric' or 'categorical'")


def explain(summary):
    if summary.get("type") == "numeric":
        display_style = summary.get("display_style", "decimal")
        if "financial" in summary:
            financial = summary["financial"]
            print(f"""
Across these trials, the typical return was {format_numeric(summary['mean'], display_style)}.
Starting from {format_currency(financial['initial_amount'])}, that works out to a typical ending value of about {format_currency(financial['mean'])}.
About half of the runs finished below {format_currency(financial['median'])}, and half finished above it.
The weakest run ended at {format_currency(financial['min'])}, while the strongest reached {format_currency(financial['max'])}.
""")
            return
        print(f"""
Across these trials, a typical result landed around {format_numeric(summary['mean'], display_style)}.
The middle result was {format_numeric(summary['median'], display_style)}, which gives you a sense of where half the outcomes fell below and half rose above.
Most runs tended to move around by about {format_numeric(summary['stdev'], display_style)}.
The full range went from {format_numeric(summary['min'], display_style)} up to {format_numeric(summary['max'], display_style)}.
""")
        return

    if summary.get("type") == "categorical":
        total = summary["total"]
        most_common = summary["counts"][0]
        least_common = summary["counts"][-1]
        print(f"""
Across {total:,} trials, {most_common[0]} showed up the most with {most_common[1]:,} results.
The rarest outcome was {least_common[0]}, which appeared {least_common[1]:,} times.
The breakdown above gives you a quick feel for how the outcomes were distributed overall.
""")
        return

    raise ValueError("Summary type must be 'numeric' or 'categorical'")
