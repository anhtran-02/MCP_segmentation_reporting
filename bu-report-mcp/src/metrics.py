import pandas as pd


def compute_basic_kpis(df: pd.DataFrame) -> dict:
    total_campaigns = df["campaign_id"].nunique()
    total_segments = df["segment_name"].nunique()
    total_operators = df["operator_name"].nunique()

    temp = df.copy()
    temp["condition_name_clean"] = temp["condition_name"].fillna("").astype(str).str.strip()

    cond_per_segment = (
        temp[temp["condition_name_clean"] != ""]
        .groupby("segment_name")["condition_name_clean"]
        .nunique()
    )

    avg_cond_per_seg = cond_per_segment.mean() if not cond_per_segment.empty else 0.0

    return {
        "total_campaigns": int(total_campaigns),
        "total_segments": int(total_segments),
        "total_operators": int(total_operators),
        "avg_cond_per_seg": round(float(avg_cond_per_seg), 2),
    }


def compute_period(df: pd.DataFrame) -> str:
    temp = df.copy()
    temp["month_dt"] = pd.to_datetime(temp["month"], errors="coerce")
    valid_dates = temp["month_dt"].dropna()

    if valid_dates.empty:
        return "Unknown period"

    return f"{valid_dates.min().date()} to {valid_dates.max().date()}"


def compute_top_conditions(df: pd.DataFrame, top_n: int = 5) -> list[dict]:
    temp = df.copy()
    temp["condition_name_clean"] = temp["condition_name"].fillna("").astype(str).str.strip()
    temp = temp[temp["condition_name_clean"] != ""]

    if temp.empty:
        return []

    result = (
        temp.groupby("condition_name_clean")
        .size()
        .reset_index(name="usage_count")
        .sort_values("usage_count", ascending=False)
        .head(top_n)
    )

    return [
        {
            "condition_name": row["condition_name_clean"],
            "usage_count": int(row["usage_count"]),
        }
        for _, row in result.iterrows()
    ]


def compute_condition_type_mix(df: pd.DataFrame) -> dict:
    temp = df.copy()
    temp["condition_type_clean"] = temp["condition_type"].fillna("UNKNOWN").astype(str).str.strip()

    counts = temp["condition_type_clean"].value_counts().to_dict()

    return {
        "CDP": int(counts.get("CDP", 0)),
        "BQ": int(counts.get("BQ", 0)),
        "OTHER": int(
            sum(v for k, v in counts.items() if k not in {"CDP", "BQ"})
        ),
    }


def compute_channel_breakdown(df: pd.DataFrame) -> list[dict]:
    result = (
        df["channel"]
        .fillna("UNKNOWN")
        .astype(str)
        .value_counts()
        .reset_index()
    )
    result.columns = ["channel", "count"]

    return result.to_dict(orient="records")


def compute_goal_breakdown(df: pd.DataFrame, top_n: int = 5) -> list[dict]:
    result = (
        df["goal"]
        .fillna("UNKNOWN")
        .astype(str)
        .value_counts()
        .reset_index()
        .head(top_n)
    )
    result.columns = ["goal", "count"]

    return result.to_dict(orient="records")


def compute_zero_condition_segments(df: pd.DataFrame) -> int:
    temp = df.copy()
    temp["condition_name_clean"] = temp["condition_name"].fillna("").astype(str).str.strip()

    seg_condition_counts = (
        temp.groupby("segment_name")["condition_name_clean"]
        .apply(lambda x: (x != "").sum())
        .reset_index(name="non_empty_condition_count")
    )

    zero_cond_segments = seg_condition_counts[
        seg_condition_counts["non_empty_condition_count"] == 0
    ]

    return int(len(zero_cond_segments))


def compute_reuse_ratio(df: pd.DataFrame) -> float:
    total_campaigns = df["campaign_id"].nunique()
    total_segments = df["segment_name"].nunique()

    if total_segments == 0:
        return 0.0

    return round(total_campaigns / total_segments, 2)


def generate_methodology_text() -> dict:
    return {
        "data_sources": "Local CSV export for BU segmentation usage analysis.",
        "join_logic": "V1 uses a single prepared CSV; no multi-table join is applied yet.",
        "dedup_logic": "Distinct campaigns, segments, operators, and conditions are computed from the CSV input.",
        "condition_label_formula": "condition_name is used directly after trimming blanks.",
        "key_metrics": "campaigns, segments, operators, avg conditions per segment, top conditions, zero-condition segments, reuse ratio.",
        "terminology": [
            "Segment: a target user group used in one or more campaigns.",
            "Condition: a filtering rule used to build a segment.",
            "CDP Condition: a behavioral or profile-based condition.",
            "BQ Condition: a static list or table-based audience condition.",
            "Avg Cond/Seg: average number of distinct conditions per segment.",
            "Camp/Seg Ratio: campaigns divided by segments; higher means more reuse.",
        ],
    }


def generate_team_overview(df: pd.DataFrame, kpis: dict) -> dict:
    return {
        "kpis": kpis,
        "channel_breakdown": compute_channel_breakdown(df),
        "goal_breakdown": compute_goal_breakdown(df),
    }


def generate_condition_analysis(df: pd.DataFrame) -> dict:
    return {
        "top_conditions": compute_top_conditions(df, top_n=5),
        "condition_type_mix": compute_condition_type_mix(df),
    }


def generate_quality_issues(df: pd.DataFrame, kpis: dict) -> list[str]:
    issues = []

    zero_condition_segments = compute_zero_condition_segments(df)
    if zero_condition_segments > 0:
        issues.append(f"Found {zero_condition_segments} zero-condition segments.")

    reuse_ratio = compute_reuse_ratio(df)
    if reuse_ratio < 1.2:
        issues.append(f"Segment reuse is low (campaigns/segments = {reuse_ratio}).")

    if kpis["avg_cond_per_seg"] < 2:
        issues.append(
            f"Average conditions per segment is low ({kpis['avg_cond_per_seg']}); targeting may be too broad."
        )

    if not issues:
        issues.append("No major issues detected by the current V1 quality checks.")

    return issues


def generate_recommendations(df: pd.DataFrame, kpis: dict) -> list[str]:
    recommendations = []

    zero_condition_segments = compute_zero_condition_segments(df)
    if zero_condition_segments > 0:
        recommendations.append(
            "Fix zero-condition segments by requiring at least one inclusion condition."
        )

    reuse_ratio = compute_reuse_ratio(df)
    if reuse_ratio < 1.2:
        recommendations.append(
            "Improve segment reuse by checking existing segments before creating new ones."
        )

    if kpis["avg_cond_per_seg"] < 2:
        recommendations.append(
            "Increase targeting depth by adding more behavioral conditions."
        )

    recommendations.append("Standardize segment naming to improve discoverability.")
    recommendations.append("Document core audience logic for team consistency.")

    return recommendations[:5]


def generate_key_takeaways(df: pd.DataFrame, kpis: dict) -> list[str]:
    takeaways = []

    takeaways.append(
        f"This BU ran {kpis['total_campaigns']} campaigns using {kpis['total_segments']} segments."
    )

    takeaways.append(
        f"The team has {kpis['total_operators']} operators and an average of {kpis['avg_cond_per_seg']} conditions per segment."
    )

    top_conditions = compute_top_conditions(df, top_n=1)
    if top_conditions:
        top = top_conditions[0]
        takeaways.append(
            f"The most used condition is {top['condition_name']} with {top['usage_count']} uses."
        )

    reuse_ratio = compute_reuse_ratio(df)
    takeaways.append(
        f"The campaign-to-segment reuse ratio is {reuse_ratio}."
    )

    zero_condition_segments = compute_zero_condition_segments(df)
    takeaways.append(
        f"There are {zero_condition_segments} zero-condition segments flagged in the current checks."
    )

    return takeaways[:5]


def build_report_data(df: pd.DataFrame, bu_name: str) -> dict:
    kpis = compute_basic_kpis(df)

    return {
        "bu_name": bu_name,
        "period": compute_period(df),
        "methodology": generate_methodology_text(),
        "team_overview": generate_team_overview(df, kpis),
        "condition_analysis": generate_condition_analysis(df),
        "quality_issues": generate_quality_issues(df, kpis),
        "recommendations": generate_recommendations(df, kpis),
        "key_takeaways": generate_key_takeaways(df, kpis),
        "size_pool": compute_size_pool_distribution(df),
        "operator_profiles": compute_operator_profiles(df),
    }
    
def compute_size_pool_distribution(df: pd.DataFrame) -> list[str]:
    temp = df.copy()
    temp["size_pool"] = pd.to_numeric(temp["size_pool"], errors="coerce")

    lines = []

    grouped = temp.groupby(["channel", "goal"])["size_pool"]

    summary = grouped.median().reset_index().sort_values("size_pool", ascending=False)

    for _, row in summary.head(4).iterrows():
        lines.append(
            f"{row['channel']} / {row['goal']} median = {int(row['size_pool'])} users"
        )

    if not lines:
        lines.append("No size pool data available.")

    return lines

def compute_operator_profiles(df: pd.DataFrame) -> list[str]:
    temp = df.copy()
    temp["condition_name_clean"] = temp["condition_name"].fillna("").astype(str)

    profiles = []

    grouped = temp.groupby("operator_name")

    for operator, g in grouped:
        campaigns = g["campaign_id"].nunique()
        segments = g["segment_name"].nunique()

        cond_per_seg = (
            g[g["condition_name_clean"] != ""]
            .groupby("segment_name")["condition_name_clean"]
            .nunique()
            .mean()
        )

        cond_per_seg = round(cond_per_seg, 2) if cond_per_seg else 0

        reuse_ratio = round(campaigns / segments, 2) if segments else 0

        if cond_per_seg >= 3:
            label = "Full-Funnel (High Complexity)"
        elif reuse_ratio >= 2:
            label = "High Reuse Specialist"
        else:
            label = "Low Complexity"

        profiles.append(
            f"{operator}: {label} | campaigns={campaigns}, cond/seg={cond_per_seg}, reuse={reuse_ratio}"
        )

    return profiles[:5]