# Stochastix

```
 .oooooo..o     .                       oooo                               .    o8o              
d8P'    `Y8   .o8                       `888                             .o8    `"'              
Y88bo.      .o888oo  .ooooo.   .ooooo.   888 .oo.    .oooo.    .oooo.o .o888oo oooo  oooo    ooo 
 `"Y8888o.    888   d88' `88b d88' `"Y8  888P"Y88b  `P  )88b  d88(  "8   888   `888   `88b..8P'  
     `"Y88b   888   888   888 888        888   888   .oP"888  `"Y88b.    888    888     Y888'    
oo     .d8P   888 . 888   888 888   .o8  888   888  d8(  888  o.  )88b   888 .  888   .o8"'88b   
8""88888P'    "888" `Y8bod8P' `Y8bod8P' o888o o888o `Y888""8o 8""888P'   "888" o888o o88'   888o  v1.0.1
```

A lightweight Monte Carlo simulation engine for Python. Run thousands - or millions - of random trials from your terminal and get clear, plain-English statistical summaries without storing every result in memory.

Built by [SS-YYC](https://github.com/SS-YYC) · Licensed under [GPL-3.0](LICENSE)

---

## What is Monte Carlo Simulation?

Monte Carlo simulation is a technique where you repeat a random experiment thousands of times to understand what outcomes are likely. Instead of calculating a single answer, you let randomness play out at scale and observe the pattern.

For example: if you flip a coin 10 times, you might get 7 heads by luck. But if you flip it 1,000,000 times, you'll get very close to 50/50. Stochastix applies this idea to any range of values you choose.

---

## Features

- **Built-in scenarios** - run a custom uniform range, coin flip, 6-sided die, or financial return simulation
- **Real-time progress bar** - terminal-safe staged progress updates during long simulations
- **Readable results screen** - keeps familiar stats like mean and median while explaining them in plain language
- **Finance-friendly reporting** - can apply simulated returns to a starting amount of money
- **Input validation** - clear error messages for invalid inputs
- **Large trial warnings** - heads-up when running over 10 million trials
- **Streaming summaries** - large runs avoid building a giant in-memory results list
- **Clean exit handling** - `Ctrl+C` now cancels the running simulation instead of leaving a worker behind

---

## Project Structure

```
Stochastix/
├── main.py                  # Entry point and CLI
├── README.md
└── Assets/
    ├── distributions.py     # Random sampling functions
    ├── engine.py            # Core simulation runner
    └── results.py           # Aggregation, statistics, and reporting
```

---

## Requirements

- Python 3.10 or higher
- No external dependencies - uses only the Python standard library

---

## Installation

Clone the repository:

```bash
git clone https://github.com/SS-YYC/stochastix.git
cd stochastix
```

No install step required. Run directly with Python.

---

## Usage

```bash
python main.py
```

You'll be prompted to choose a scenario and then enter the values that scenario needs:

```
Choose a scenario:
1. Custom uniform range - Generate decimal values between two bounds.
2. Coin flip - Simulate fair coin tosses with Heads/Tails outcomes.
3. 6-sided die - Roll a standard die with outcomes from 1 to 6.
4. Financial return range - Simulate percentage returns and apply them to a starting amount.
Select scenario (1-4): 1
Enter lower bound (a): 10
Enter upper bound (b): 50
Enter number of trials (n): 100000
```

Stochastix will run the simulation with a live progress bar, then print a more human-readable summary:

```
[########################] 100.0% | Complete
Here is the simulation summary:
Mean: 30.0124
Median: 30.0351
Usual amount of variation: 11.5478
Lowest result seen: 10.0003
Highest result seen: 49.9991

Across these trials, a typical result landed around 30.0124.
The middle result was 30.0351, which gives you a sense of where half the outcomes fell below and half rose above.
Most runs tended to move around by about 11.5478.
The full range went from 10.0003 up to 49.9991.
```

If you choose the financial scenario, Stochastix also asks for your starting amount and then shows the ending values those simulated returns would produce.

---

## How It Works

Stochastix is built around three modular layers:

**`distributions.py`** generates random outcomes for each scenario. It now supports custom uniform sampling, fair coin flips, standard 6-sided die rolls, and financial return sampling.

**`engine.py`** accepts a model function and a trial count, runs each trial, updates the progress tracker in real time, and supports safe cancellation.

**`results.py`** computes numeric and categorical summaries, using streaming statistics for numeric simulations so large runs do not need to keep every result in memory. Financial simulations also display the ending value that each return profile would imply for the user's starting amount.

---

## License

Stochastix is open source under the [GNU General Public License v3.0](LICENSE). Feel free to use, modify, and distribute.
