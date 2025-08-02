"""
Monte Carlo test of the Chebyshev-based sample size estimator.

1. Computes n_required via Chebyshev’s inequality for given
   outcome probabilities, risk δ, and margin ε.
2. Runs num_trials simulations, each drawing n_required samples
   from the discrete distribution.
3. Estimates the empirical probability that |X̄ - μ| ≥ ε, and
   compares it to the allowed risk δ.

python law-of-numbers-theory.py \
  --probs 0.5 0.5 \
  --risk 0.05 \
  --margin 0.1 \
  --trials 20000
"""

import argparse
import math
import sys
import random

def estimate_sample_size(probs, risk, margin):
    mean = sum(p * i for i, p in enumerate(probs))
    variance = sum(p * (i - mean) ** 2 for i, p in enumerate(probs))
    return math.ceil(variance / (risk * margin ** 2)), mean

def run_simulation(probs, n_samples, true_mean, margin, num_trials):
    failures = 0
    outcomes = list(range(len(probs)))
    for _ in range(num_trials):
        # draw n_samples with replacement
        sample = random.choices(outcomes, weights=probs, k=n_samples)
        sample_mean = sum(sample) / n_samples
        if abs(sample_mean - true_mean) >= margin:
            failures += 1
    return failures / num_trials

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-p", "--probs", type=float, nargs="+", required=True,
                        help="Outcome probabilities summing to 1 (e.g. 0.5 0.5)")
    parser.add_argument("-r", "--risk", type=float, required=True,
                        help="Allowed risk δ (e.g. 0.05 for 5%)")
    parser.add_argument("-m", "--margin", type=float, required=True,
                        help="Desired margin ε around the mean")
    parser.add_argument("-t", "--trials", type=int, default=10000,
                        help="Number of Monte Carlo trials (default: 10000)")
    return parser.parse_args()

def main():
    args = parse_args()
    if abs(sum(args.probs) - 1.0) > 1e-6:
        sys.exit("Error: --probs must sum to 1.")
    n_required, true_mean = estimate_sample_size(args.probs, args.risk, args.margin)
    print(f"Computed sample size (n_required): {n_required}")
    print(f"True mean of distribution: {true_mean:.4f}")
    print(f"Running {args.trials} Monte Carlo trials...")
    emp_risk = run_simulation(
        probs=args.probs,
        n_samples=n_required,
        true_mean=true_mean,
        margin=args.margin,
        num_trials=args.trials
    )
    print(f"Empirical risk (P(|X̄ - μ| ≥ ε)): {emp_risk:.4f}")
    print(f"Allowed risk δ: {args.risk:.4f}")
    if emp_risk <= args.risk:
        print("→ Empirical risk is within the allowed bound.")
    else:
        print("→ Empirical risk exceeds the allowed bound.")

if __name__ == "__main__":
    main()
