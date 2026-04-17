# Stochastix

```
 .oooooo..o     .                       oooo                               .    o8o              
d8P'    `Y8   .o8                       `888                             .o8    `"'              
Y88bo.      .o888oo  .ooooo.   .ooooo.   888 .oo.    .oooo.    .oooo.o .o888oo oooo  oooo    ooo 
 `"Y8888o.    888   d88' `88b d88' `"Y8  888P"Y88b  `P  )88b  d88(  "8   888   `888   `88b..8P'  
     `"Y88b   888   888   888 888        888   888   .oP"888  `"Y88b.    888    888     Y888'    
oo     .d8P   888 . 888   888 888   .o8  888   888  d8(  888  o.  )88b   888 .  888   .o8"'88b   
8""88888P'    "888" `Y8bod8P' `Y8bod8P' o888o o888o `Y888""8o 8""888P'   "888" o888o o88'   888o  v1.0.0
```

A lightweight Monte Carlo simulation engine for Python. Run thousands - or millions - of random trials from your terminal and get clear, plain-English statistical summaries.

Built by [SS-YYC](https://github.com/SS-YYC) · Licensed under [GPL-3.0](LICENSE)

---

## What is Monte Carlo Simulation?

Monte Carlo simulation is a technique where you repeat a random experiment thousands of times to understand what outcomes are likely. Instead of calculating a single answer, you let randomness play out at scale and observe the pattern.

For example: if you flip a coin 10 times, you might get 7 heads by luck. But if you flip it 1,000,000 times, you'll get very close to 50/50. Stochastix applies this idea to any range of values you choose.

---

## Features

- **Built-in scenarios** - run a custom uniform range, coin flip, or 6-sided die
- **Real-time progress bar** - visual feedback during long simulations
- **Statistical summary** - mean, median, standard deviation, min, and max
- **Plain-English explanation** - results explained in simple terms for non-statisticians
- **Input validation** - clear error messages for invalid inputs
- **Large trial warnings** - heads-up when running over 10 million trials
- **Clean exit handling** - graceful `Ctrl+C` support

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

You'll be prompted to choose a scenario and enter the number of trials:

```
Choose a scenario:
1. Custom uniform range - Generate decimal values between two bounds.
2. Coin flip - Simulate fair coin tosses with Heads/Tails outcomes.
3. 6-sided die - Roll a standard die with outcomes from 1 to 6.
Select scenario (1-3): 1
Enter lower bound (a): 10
Enter upper bound (b): 50
Enter number of trials (n): 100000
```

Stochastix will run the simulation with a live progress bar, then print a summary:

```
[████████████████████████████████████████] 100.0%
Summary of Results:
Mean: 30.0124
Median: 30.0351
Standard Deviation: 11.5478
Minimum: 10.0003
Maximum: 49.9991

On average, results landed around 30.0124.
Half of all trials fell below 30.0351 (the median).
Results varied with a spread of 11.5478 on average.
The lowest result was 10.0003 and the highest was 49.9991.
```

---

## How It Works

Stochastix is built around three modular layers:

**`distributions.py`** generates random outcomes for each scenario. It now supports custom uniform sampling, fair coin flips, and standard 6-sided die rolls.

**`engine.py`** accepts a model function and a trial count, calls the model repeatedly, and collects all results. The progress tracker updates in real time so the CLI can display a progress bar.

**`results.py`** takes the raw list of outputs and computes summary statistics, formats them for the terminal, and provides a plain-English explanation of what the numbers mean.

---

## License

Stochastix is open source under the [GNU General Public License v3.0](LICENSE). Feel free to use, modify, and distribute.
