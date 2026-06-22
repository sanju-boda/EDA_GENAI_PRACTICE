"""Launch D-Tale for interactive EDA on the sales dataset."""

from __future__ import annotations

from pathlib import Path

import dtale
import pandas as pd


def load_sales_data(file_path: str = "sales_data.csv") -> pd.DataFrame:
    """Load the sales dataset with clear error handling."""
    csv_path = Path(file_path)
    print(f"Loading dataset from {csv_path}...")

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path.resolve()}")

    try:
        data = pd.read_csv(csv_path, parse_dates=["date"])
    except pd.errors.EmptyDataError as error:
        raise ValueError("The dataset file is empty.") from error
    except pd.errors.ParserError as error:
        raise ValueError("The dataset file could not be parsed as CSV.") from error

    print(f"Dataset loaded successfully: {len(data):,} rows, {len(data.columns)} columns.")
    return data


def launch_dtale(data: pd.DataFrame) -> None:
    """Start D-Tale and open the interactive GUI in a browser."""
    print("Launching D-Tale...")

    instance = dtale.show(data, open_browser=True)
    url = getattr(instance, "_main_url", None)

    print("D-Tale launched successfully.")
    print(f"Access the interface here: {url}")
    print("Keep this Python process running while using D-Tale.")

    try:
        input("Press Enter to stop the D-Tale session...")
    except EOFError:
        print("No interactive console was detected, so the D-Tale session has ended.")


def main() -> None:
    """Load the dataset and launch D-Tale."""
    try:
        sales_data = load_sales_data()
        launch_dtale(sales_data)
    except Exception as error:
        print("Failed to launch D-Tale.")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()
