"""Create automated EDA reports for the sales dataset."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import pandas as pd
import sweetviz as sv
from packaging.version import Version
from ydata_profiling import ProfileReport


REQUIRED_PACKAGES = {
    "pandas": "2.0.0",
    "ydata-profiling": "4.6.0",
    "sweetviz": "2.3.0",
}


def verify_library_versions() -> None:
    """Confirm that required libraries are installed at compatible versions."""
    print("Verifying library versions...")

    for package_name, minimum_version in REQUIRED_PACKAGES.items():
        try:
            installed_version = version(package_name)
        except PackageNotFoundError as error:
            raise RuntimeError(f"{package_name} is not installed.") from error

        if Version(installed_version) < Version(minimum_version):
            raise RuntimeError(
                f"{package_name}>={minimum_version} is required, "
                f"but {installed_version} is installed."
            )

        print(f"OK: {package_name} {installed_version}")

    print("Library version verification completed successfully.")


def load_sales_data(file_path: str = "sales_data.csv") -> pd.DataFrame:
    """Load the sales CSV file into a pandas DataFrame with clear error messages."""
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

    print(f"Dataset loaded successfully with {len(data):,} rows and {len(data.columns)} columns.")
    return data


def create_ydata_report(data: pd.DataFrame, output_file: str = "ydata_report.html") -> None:
    """Create and save a fast YData Profiling report."""
    print("Creating YData Profiling report...")

    profile = ProfileReport(
        data,
        title="Sales Data Profiling Report",
        minimal=True,
    )
    profile.to_file(output_file)

    print(f"YData Profiling report saved successfully: {Path(output_file).resolve()}")


def create_sweetviz_report(data: pd.DataFrame, output_file: str = "sweetviz_report.html") -> None:
    """Create and save a Sweetviz report using revenue as the target variable."""
    print("Creating Sweetviz report...")

    if "revenue" not in data.columns:
        raise ValueError("The dataset must include a 'revenue' column for the Sweetviz target.")

    # Sweetviz does not allow missing values in the target feature. The original
    # dataset is left unchanged; only the Sweetviz input is filtered.
    sweetviz_data = data.dropna(subset=["revenue"]).copy()
    dropped_rows = len(data) - len(sweetviz_data)

    if sweetviz_data.empty:
        raise ValueError("No rows with non-missing revenue are available for Sweetviz.")

    if dropped_rows:
        print(f"Dropped {dropped_rows:,} rows with missing revenue for the Sweetviz target.")

    report = sv.analyze(sweetviz_data, target_feat="revenue")
    report.show_html(filepath=output_file, open_browser=False)

    print(f"Sweetviz report saved successfully: {Path(output_file).resolve()}")


def main() -> None:
    """Run automated EDA report generation."""
    try:
        verify_library_versions()
        sales_data = load_sales_data()
        create_ydata_report(sales_data)
        create_sweetviz_report(sales_data)
        print("Automated EDA completed successfully.")
    except Exception as error:
        print("Automated EDA failed.")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()
