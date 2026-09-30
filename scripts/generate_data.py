"""Write a synthetic Churn_Modelling.csv to data/raw/.

Usage: uv run python scripts/generate_data.py [--rows 10000] [--seed 42]
"""

import argparse
from pathlib import Path

from tulip_churn.data import TARGET
from tulip_churn.synthetic import generate

OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "Churn_Modelling.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    df = generate(args.rows, args.seed)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} rows to {OUT} (churn rate {df[TARGET].mean():.1%})")


if __name__ == "__main__":
    main()
