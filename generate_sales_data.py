"""Generate a sample sales dataset for Python EDA practice."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_sales_data(output_file: str = "sales_data.csv", row_count: int = 100_000) -> None:
    """Create a reproducible sales transaction dataset and save it as a CSV file."""
    if row_count <= 0:
        raise ValueError("row_count must be a positive integer.")

    print("Starting sales data generation...")

    np.random.seed(42)

    products = np.array(["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse", "Printer"])
    product_to_category = {
        "Laptop": "Electronics",
        "Phone": "Electronics",
        "Tablet": "Electronics",
        "Monitor": "Accessories",
        "Keyboard": "Accessories",
        "Mouse": "Accessories",
        "Printer": "Office Equipment",
    }
    regions = np.array(["North", "South", "East", "West", "Central"], dtype=object)

    selected_products = np.random.choice(products, size=row_count)
    prices = np.round(np.random.uniform(10.0, 2_000.0, size=row_count), 2)
    selected_regions = np.random.choice(regions, size=row_count)

    data = pd.DataFrame(
        {
            "transaction_id": np.arange(1, row_count + 1),
            "customer_id": np.random.randint(1_000, 10_000, size=row_count),
            "product": selected_products,
            "category": [product_to_category[product] for product in selected_products],
            "quantity": np.random.randint(1, 11, size=row_count),
            "price": prices,
            "date": np.random.choice(pd.date_range("2023-01-01", "2024-12-31"), size=row_count),
            "region": selected_regions,
        }
    )

    price_missing_indices = np.random.choice(data.index, size=int(row_count * 0.05), replace=False)
    region_missing_indices = np.random.choice(data.index, size=int(row_count * 0.02), replace=False)

    data.loc[price_missing_indices, "price"] = np.nan
    data.loc[region_missing_indices, "region"] = np.nan
    data["revenue"] = data["quantity"] * data["price"]

    data = data[
        [
            "transaction_id",
            "customer_id",
            "product",
            "category",
            "quantity",
            "price",
            "revenue",
            "date",
            "region",
        ]
    ]

    output_path = Path(output_file)
    data.to_csv(output_path, index=False)

    print(f"Dataset created successfully: {output_path.resolve()}")
    print(f"Rows generated: {len(data):,}")
    print(f"Missing price values: {data['price'].isna().sum():,}")
    print(f"Missing region values: {data['region'].isna().sum():,}")


def main() -> None:
    """Run the dataset generator with simple error handling."""
    try:
        generate_sales_data()
    except Exception as error:
        print("Failed to generate the sales dataset.")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()
