# This fill will 
# - read the CSV
# - check required columns
# - filter data by BU


from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "bu_name",
    "campaign_id",
    "segment_name",
    "operator_name",
    "condition_name",
    "condition_type",
    "channel",
    "goal",
    "size_pool",
    "month",
]


def load_csv(csv_path: str) -> pd.DataFrame:
    """
    Load CSV file into a pandas DataFrame.
    """
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(path)

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Missing required columns: {missing_cols}\n"
            f"Found columns: {list(df.columns)}"
        )

    return df


def filter_by_bu(df: pd.DataFrame, bu_name: str) -> pd.DataFrame:
    """
    Filter rows for one BU only.
    """
    filtered = df[df["bu_name"].astype(str).str.upper() == bu_name.upper()].copy()

    if filtered.empty:
        raise ValueError(f"No data found for BU: {bu_name}")

    return filtered


def list_bu_names(df: pd.DataFrame) -> list[str]:
    """
    Return sorted distinct BU names.
    """
    values = df["bu_name"].dropna().astype(str).str.strip().unique().tolist()
    return sorted(values)