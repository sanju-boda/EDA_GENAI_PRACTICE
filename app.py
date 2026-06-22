#Streamlit dashboard for EDA_GENAI_PRACTICE.

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional

import pandas as pd
import streamlit as st
import altair as alt
from streamlit.components.v1 import html

try:
    import dtale
except Exception:
    dtale = None

# Paths
DATA_PATH = Path("sales_data.csv")
SWEETVIZ_REPORT = Path("sweetviz_report.html")
YDATA_REPORT = Path("ydata_report.html")


@st.cache_data
def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            "sales_data.csv was not found. Run `python generate_sales_data.py` before deploying."
        )
    df = pd.read_csv(path, parse_dates=["date"], low_memory=False)
    return df.convert_dtypes()


def option_index(options: List[str], preferred_names: List[str]) -> int:
    lowered = [o.lower() for o in options]
    for name in preferred_names:
        if name.lower() in lowered:
            return lowered.index(name.lower())
    return 0


def select_optional_column(label: str, columns: List[str], preferred_names: Optional[List[str]] = None, key: Optional[str] = None) -> Optional[str]:
    preferred_names = preferred_names or []
    options = ["None"] + columns
    idx = 0
    for name in preferred_names:
        if name in columns:
            idx = options.index(name)
            break
    selected = st.sidebar.selectbox(label, options, index=idx, key=key)
    return None if selected == "None" else selected


def parse_date_series(values: pd.Series) -> pd.Series:
    return pd.to_datetime(values, errors="coerce")


def numeric_columns(data: pd.DataFrame) -> List[str]:
    cols: List[str] = []
    for col in data.columns:
        converted = pd.to_numeric(data[col], errors="coerce")
        if converted.notna().any():
            cols.append(col)
    return cols


def categorical_columns(data: pd.DataFrame) -> List[str]:
    cols: List[str] = []
    for col in data.columns:
        unique_count = data[col].nunique(dropna=True)
        if 1 < unique_count <= 200:
            cols.append(col)
    return cols


def metric_value(v: Any) -> str:
    if pd.isna(v):
        return "—"
    if isinstance(v, (float, int)):
        return f"{v:,.2f}" if isinstance(v, float) else f"{v:,}"
    return str(v)


def format_metric(label: str, value: Any) -> tuple[str, str]:
    return label, metric_value(value)


def render_report_link(report_path: Path, title: str) -> None:
    st.subheader(title)
    if report_path.exists():
        try:
            report_html = report_path.read_text(encoding="utf-8")
            st.info(f"Embedded {title} below.")
            html(report_html, height=900, scrolling=True)
        except Exception as exc:
            st.error(f"Unable to embed the report: {exc}")
    else:
        st.warning(f"{title} is not available. Run `python automated_eda.py` first.")


def get_d_tale_url(data: pd.DataFrame) -> Optional[str]:
    if dtale is None:
        return None
    data_hash = int(pd.util.hash_pandas_object(data, index=True).sum())
    if "dtale_url" not in st.session_state or st.session_state.get("dtale_data_id") != data_hash:
        inst = dtale.show(data, open_browser=False)
        st.session_state["dtale_url"] = getattr(inst, "_main_url", None)
        st.session_state["dtale_data_id"] = data_hash
    return st.session_state.get("dtale_url")


def render_overview(data: pd.DataFrame) -> None:
    st.title("EDA Overview")
    # Sidebar controls
    all_columns = list(data.columns)
    numeric_opts = numeric_columns(data)
    category_opts = categorical_columns(data)

    st.sidebar.header("Dataset Mapping")
    value_col = select_optional_column("Value column", numeric_opts, preferred_names=["revenue", "sales", "amount", "price", "total"], key="value_col")
    date_col = select_optional_column("Date column", all_columns, preferred_names=["date", "order_date", "transaction_date", "created_at"], key="date_col")
    group_col = select_optional_column("Group column", category_opts, preferred_names=["category", "product", "region", "country", "segment"], key="group_col")
    filter_col = select_optional_column("Filter column", category_opts, preferred_names=["region", "country", "category", "segment"], key="filter_col")

    # Region filter if available
    selected_regions: List[str] = []
    if "region" in data.columns:
        regions = sorted([str(x) for x in data["region"].dropna().unique()])
        selected_regions = st.sidebar.multiselect("Regions", regions, default=regions)

    # Date range
    if date_col and data[date_col].notna().any():
        parsed = parse_date_series(data[date_col])
        valid = parsed.dropna()
        if not valid.empty:
            min_d = valid.min().date()
            max_d = valid.max().date()
            selected_range = st.sidebar.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
        else:
            selected_range = None
    else:
        selected_range = None

    # Apply filters
    filtered = data.copy()
    if selected_range and len(selected_range) == 2 and date_col:
        start_d, end_d = selected_range
        parsed = parse_date_series(filtered[date_col])
        filtered = filtered[(parsed.dt.date >= start_d) & (parsed.dt.date <= end_d)]
    if selected_regions and "region" in filtered.columns:
        filtered = filtered[filtered["region"].astype(str).isin(selected_regions)]

    if filter_col:
        vals = sorted([str(x) for x in filtered[filter_col].dropna().unique()])
        sel = st.sidebar.multiselect(f"{filter_col} filter", vals, default=vals)
        if sel:
            filtered = filtered[filtered[filter_col].astype(str).isin(sel)]

    # Metrics
    orders = len(filtered)
    revenue = float(filtered["revenue"].sum(skipna=True)) if "revenue" in filtered.columns else 0.0
    avg_order = float(filtered["revenue"].mean(skipna=True)) if "revenue" in filtered.columns else 0.0
    missing_price = int(filtered["price"].isna().sum()) if "price" in filtered.columns else 0
    missing_cells = int(filtered.isna().sum().sum())
    duplicate_rows = int(filtered.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue", f"${metric_value(revenue)}")
    col2.metric("Transactions", metric_value(orders))
    col3.metric("Avg. Revenue", f"${metric_value(avg_order)}")
    col4.metric("Missing Prices", metric_value(missing_price))

    st.markdown("---")

    # Layout columns for charts
    left, right = st.columns(2)
    with left:
        st.subheader("Revenue by Category")
        if "category" in filtered.columns:
            cat_rev = filtered.groupby("category", dropna=False)["revenue"].sum().sort_values(ascending=False)
            st.bar_chart(cat_rev)
        else:
            st.info("No 'category' column available.")

        st.subheader("Grouped Values")
        if value_col and group_col:
            grp = (
                filtered.assign(**{value_col: pd.to_numeric(filtered[value_col], errors="coerce")})
                .groupby(group_col, dropna=False)[value_col]
                .sum()
                .sort_values(ascending=False)
                .head(30)
            )
            st.bar_chart(grp)
        else:
            st.info("Choose a value column and group column to show this chart.")

    with right:
        st.subheader("Revenue by Region")
        if "region" in filtered.columns:
            reg_rev = filtered.groupby("region", dropna=False)["revenue"].sum().sort_values(ascending=False)
            st.bar_chart(reg_rev)
        else:
            st.info("No 'region' column available.")

        st.subheader("Missing Values")
        st.bar_chart(filtered.isna().sum().sort_values(ascending=False).head(30))

    st.markdown("---")
    st.subheader("Monthly Revenue")
    if date_col and value_col:
        tmp = filtered.copy()
        tmp[date_col] = parse_date_series(tmp[date_col])
        series = tmp.dropna(subset=[date_col]).set_index(date_col).resample("M")[value_col].sum()
        st.line_chart(series)
    else:
        st.info("Choose a date column and value column to show monthly trends.")


def main() -> None:
    st.set_page_config(page_title="EDA_GENAI_PRACTICE Dashboard", layout="wide")
    # Load data
    try:
        data = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        return

    tabs = st.tabs(["Overview", "Sweetviz Report", "YData Report", "D-Tale"])

    with tabs[0]:
        render_overview(data)

    with tabs[1]:
        render_report_link(SWEETVIZ_REPORT, "Sweetviz Report")

    with tabs[2]:
        render_report_link(YDATA_REPORT, "YData Profiling Report")

    with tabs[3]:
        st.subheader("D-Tale")
        url = get_d_tale_url(data)
        if url:
            st.markdown(f"[Open D-Tale in a new tab]({url})")
        else:
            st.info("D-Tale is not available or not installed. Install with `pip install dtale`.")


if __name__ == "__main__":
    main()
