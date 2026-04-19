import random
import threading
import time
import sys
import shutil

from Assets.distributions import sample_coin_flip, sample_die_roll, sample_uniform
from Assets.engine import SimulationCancelled, run
from Assets.results import add_financial_context, report, explain

print(rf"""
 .oooooo..o     .                       oooo                               .    o8o              
d8P'    `Y8   .o8                       `888                             .o8    `"'              
Y88bo.      .o888oo  .ooooo.   .ooooo.   888 .oo.    .oooo.    .oooo.o .o888oo oooo  oooo    ooo 
 `"Y8888o.    888   d88' `88b d88' `"Y8  888P"Y88b  `P  )88b  d88(  "8   888   `888   `88b..8P'  
     `"Y88b   888   888   888 888        888   888   .oP"888  `"Y88b.    888    888     Y888'    
oo     .d8P   888 . 888   888 888   .o8  888   888  d8(  888  o.  )88b   888 .  888   .o8"'88b   
8""88888P'    "888" `Y8bod8P' `Y8bod8P' o888o o888o `Y888""8o 8""888P'   "888" o888o o88'   888o  v1.0.1
""")

print("This is Stochastix, a Monte Carlo simulation engine for Python made by SS-YYC.")
print("Licensed under GPL-3.0. Feel free to use this code for any purpose.")


SCENARIOS = {
    "1": {
        "name": "Custom uniform range",
        "description": "Generate decimal values between two bounds.",
    },
    "2": {
        "name": "Coin flip",
        "description": "Simulate fair coin tosses with Heads/Tails outcomes.",
    },
    "3": {
        "name": "6-sided die",
        "description": "Roll a standard die with outcomes from 1 to 6.",
    },
    "4": {
        "name": "Financial return range",
        "description": "Simulate percentage returns and apply them to a starting amount.",
    },
}


def fit_text(text, max_width):
    if max_width <= 0:
        return ""
    if len(text) <= max_width:
        return text
    if max_width <= 3:
        return text[:max_width]
    return text[:max_width - 3] + "..."


def render_progress(progress, bar_width=None):
    terminal_width = shutil.get_terminal_size(fallback=(100, 20)).columns
    safe_width = max(20, terminal_width - 1)
    if bar_width is None:
        bar_width = max(5, min(28, safe_width // 4))

    pct = min(max(progress["percent"], 0.0), 1.0)
    filled = int(pct * bar_width)
    bar = '#' * filled + '-' * (bar_width - filled)
    prefix = f'[{bar}] {pct * 100:5.1f}% | {progress["status"]}'

    details = progress.get("details") or ""
    if details:
        available = safe_width - len(prefix) - 3
        if available > 0:
            details = fit_text(details, available)
            return f"{prefix} | {details}"

    return fit_text(prefix, safe_width)


def write_progress(progress, last_width, bar_width=None):
    line = render_progress(progress, bar_width)
    padding = max(0, last_width[0] - len(line))
    sys.stdout.write('\r' + line + (' ' * padding))
    sys.stdout.flush()
    last_width[0] = len(line)


def choose_scenario():
    print("\nChoose a scenario:")
    for key, scenario in SCENARIOS.items():
        print(f"{key}. {scenario['name']} - {scenario['description']}")

    while True:
        choice = input("Select scenario (1-4): ").strip()
        if choice in SCENARIOS:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


def get_trial_count():
    while True:
        try:
            n = int(input("Enter number of trials (n): "))
            if n <= 0:
                print("Number of trials must be a positive integer.")
                continue
            return n
        except ValueError:
            print("Invalid input. Please enter an integer for n.")


def get_initial_amount():
    while True:
        try:
            amount = float(input("Enter initial amount of money: "))
            if amount < 0:
                print("Initial amount cannot be negative.")
                continue
            return amount
        except ValueError:
            print("Invalid input. Please enter a numeric amount.")


def configure_model():
    choice = choose_scenario()

    if choice == "1":
        while True:
            try:
                a = float(input("Enter lower bound (a): "))
                b = float(input("Enter upper bound (b): "))
                if a >= b:
                    print("Lower bound must be less than upper bound.")
                    continue
                n = get_trial_count()

                def model():
                    return sample_uniform(a, b)

                details = f"Uniform distribution from {a:g} to {b:g}"
                return model, n, SCENARIOS[choice]["name"], details, None
            except ValueError:
                print("Invalid input. Please enter numeric values for a and b.")

    if choice == "2":
        n = get_trial_count()

        def model():
            return sample_coin_flip()

        details = "Fair coin with Heads/Tails outcomes"
        return model, n, SCENARIOS[choice]["name"], details, None

    if choice == "3":
        n = get_trial_count()

        def model():
            return sample_die_roll(6)

        details = "Standard die with outcomes from 1 to 6"
        return model, n, SCENARIOS[choice]["name"], details, None

    while True:
        try:
            lower_return = float(input("Enter lower return percentage: "))
            upper_return = float(input("Enter upper return percentage: "))
            if lower_return >= upper_return:
                print("Lower return percentage must be less than upper return percentage.")
                continue
            initial_amount = get_initial_amount()
            n = get_trial_count()

            def model():
                return sample_uniform(lower_return, upper_return)

            details = f"Returns from {lower_return:g}% to {upper_return:g}% on ${initial_amount:,.2f}"
            financial_config = {"initial_amount": initial_amount}
            return model, n, SCENARIOS[choice]["name"], details, financial_config
        except ValueError:
            print("Invalid input. Please enter numeric values for the return range.")


def main():
    model, n, scenario_name, scenario_details, scenario_config = configure_model()

    if n > 10_000_000:
        print("Warning: running over 10 million trials may take a while.")

    progress = {
        "percent": 0.05,
        "completed": 0,
        "status": "Preparing simulation inputs",
        "details": f"{scenario_name}: {scenario_details}",
    }
    worker_state = {
        "summary": None,
        "error": None,
        "cancelled": False,
    }
    cancel_event = threading.Event()

    def run_simulation():
        try:
            worker_state["summary"] = run(model, n, progress, cancel_event=cancel_event)
        except SimulationCancelled:
            worker_state["cancelled"] = True
        except Exception as exc:
            worker_state["error"] = exc

    progress["percent"] = 0.12
    progress["status"] = "Starting simulation worker"
    progress["details"] = f"Queued {n:,} trial{'s' if n != 1 else ''}"

    thread = threading.Thread(target=run_simulation, daemon=True)
    thread.start()

    bar_width = None
    last_width = [0]
    try:
        while thread.is_alive():
            done = progress["completed"]
            run_pct = done / n
            progress["percent"] = 0.12 + (run_pct * 0.76)
            progress["status"] = f"Running simulations ({done:,}/{n:,} trials)"
            progress["details"] = f"{n - done:,} remaining"
            write_progress(progress, last_width, bar_width)
            time.sleep(0.1)
    except KeyboardInterrupt:
        cancel_event.set()
        progress["status"] = "Cancelling simulation"
        progress["details"] = "Stopping after the current trial"
        write_progress(progress, last_width, bar_width)
        thread.join()
        sys.stdout.write("\nSimulation cancelled.\n")
        return

    thread.join()

    if worker_state["error"] is not None:
        sys.stdout.write("\n")
        raise worker_state["error"]

    if worker_state["cancelled"]:
        sys.stdout.write("\nSimulation cancelled.\n")
        return

    summary = worker_state["summary"]
    if scenario_config and "initial_amount" in scenario_config:
        summary = add_financial_context(summary, scenario_config["initial_amount"])

    progress["completed"] = n
    progress["percent"] = 0.88
    progress["status"] = "Simulation finished"
    progress["details"] = f"Processed {n:,} result{'s' if n != 1 else ''}"
    write_progress(progress, last_width, bar_width)

    progress["percent"] = 0.94
    progress["status"] = "Finalizing summary"
    progress["details"] = "Streaming statistics ready"
    write_progress(progress, last_width, bar_width)

    progress["percent"] = 0.98
    progress["status"] = "Preparing final report"
    progress["details"] = "Formatting summary and explanation"
    write_progress(progress, last_width, bar_width)

    progress["percent"] = 1.0
    progress["status"] = "Complete"
    progress["details"] = ""
    write_progress(progress, last_width, bar_width)
    sys.stdout.write("\n")
    report(summary)
    explain(summary)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("\nExiting Stochastix. Goodbye!")
