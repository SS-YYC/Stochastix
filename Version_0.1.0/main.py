import random
import threading
import time
import sys

from Assets.distributions import uniform
from Assets.engine import run
from Assets.results import summarize, report, explain

print(rf"""
 .oooooo..o     .                       oooo                               .    o8o              
d8P'    `Y8   .o8                       `888                             .o8    `"'              
Y88bo.      .o888oo  .ooooo.   .ooooo.   888 .oo.    .oooo.    .oooo.o .o888oo oooo  oooo    ooo 
 `"Y8888o.    888   d88' `88b d88' `"Y8  888P"Y88b  `P  )88b  d88(  "8   888   `888   `88b..8P'  
     `"Y88b   888   888   888 888        888   888   .oP"888  `"Y88b.    888    888     Y888'    
oo     .d8P   888 . 888   888 888   .o8  888   888  d8(  888  o.  )88b   888 .  888   .o8"'88b   
8""88888P'    "888" `Y8bod8P' `Y8bod8P' o888o o888o `Y888""8o 8""888P'   "888" o888o o88'   888o  v0.1.0
""")

print("This is Stochastix, a Monte Carlo simulation engine for Python made by SS-YYC.")
print("Licensed under GPL-3.0. Feel free to use this code for any purpose.")


def main():
    try:
        while True:
            try:
                a = float(input("Enter lower bound (a): "))
                b = float(input("Enter upper bound (b): "))
                n = int(input("Enter number of trials (n): "))
                break
            except ValueError:
                print("Invalid input. Please enter numeric values for a, b and an integer for n.")

        def model():
            return random.uniform(a, b)

        if n > 10_000_000:
            print("Warning: running over 10 million trials may take a while.")

        progress = [0]
        simulation_results = []

        def run_simulation():
            simulation_results.extend(run(model, n, progress))

        thread = threading.Thread(target=run_simulation)
        thread.start()

        bar_width = 40
        while thread.is_alive():
            done = progress[0]
            pct = done / n
            filled = int(pct * bar_width)
            bar = '█' * filled + '░' * (bar_width - filled)
            sys.stdout.write(f'\r[{bar}] {pct*100:.1f}%')
            sys.stdout.flush()
            time.sleep(0.1)

        sys.stdout.write(f'\r[{"█" * bar_width}] 100.0%\n')
        results = simulation_results
        summary = summarize(results)
        report(summary)
        explain(summary)

    except (KeyboardInterrupt, EOFError):
        print("\nExiting Stochastix. Goodbye!")


if __name__ == "__main__":
    main()