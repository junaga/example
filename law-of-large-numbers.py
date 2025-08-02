"""
Estimate the sample size needed so that, by Chebyshev’s inequality,

    Pr(|X̄ - μ| ≥ margin) ≤ risk

for a discrete distribution on {0, 1, ..., k-1}
with outcome probabilities given by `probs`.

python law-of-large-numbers.py \
  --probs 0.5 0.5 \
  --risk 0.05 \
  --margin 0.1
"""

import argparse
import math
import sys

def estimate_sample_size(probs, risk, margin):
    # Compute the mean μ
    mean = sum(p * i for i, p in enumerate(probs))
    # Compute the variance σ²
    variance = sum(p * (i - mean) ** 2 for i, p in enumerate(probs))
    # Chebyshev bound: n ≥ σ² / (risk * margin²)
    return math.ceil(variance / (risk * margin ** 2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute required sample size via Chebyshev’s inequality"
    )
    parser.add_argument(
        "--probs", "-p", type=float, nargs="+", required=True,
        help="List of outcome probabilities (must sum to 1)."
    )
    parser.add_argument(
        "--risk", "-r", type=float, required=True,
        help="Allowed probability δ of exceeding the margin (e.g. 0.05)."
    )
    parser.add_argument(
        "--margin", "-m", type=float, required=True,
        help="Desired margin ε around the mean (same units as outcomes)."
    )
    args = parser.parse_args()

    if abs(sum(args.probs) - 1.0) > 1e-6:
        sys.exit("Error: --probs must sum to 1.")

    n_required = estimate_sample_size(args.probs, args.risk, args.margin)
    print(f"Required sample size: {n_required}")
