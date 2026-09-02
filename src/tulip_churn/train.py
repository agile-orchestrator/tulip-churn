"""Training entrypoint.

TODO: training currently lives in notebooks/01_exploration.ipynb. Run the notebook to produce
models/model.joblib until this is ported.
"""

import sys


def main() -> None:
    print(
        "Training is not wired up yet. Run:\n"
        "  uv run jupyter nbconvert --to notebook --execute --inplace "
        "notebooks/01_exploration.ipynb",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
