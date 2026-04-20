from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

from csv_reader import load_csv, filter_by_bu
from metrics import build_report_data
from ppt_writer import write_ppt


mcp = FastMCP("bu-report")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "segmentation_usage.csv"
CINEMA_CSV_PATH = PROJECT_ROOT / "data" / "cinema_bu_campaigns_100_rows.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"

DATA_SOURCES = {
    "default": {
        "path": DEFAULT_CSV_PATH,
        "description": "General segmentation usage data (UTILITIES, TELCO, etc.)",
    },
    "cinema": {
        "path": CINEMA_CSV_PATH,
        "description": "Cinema BU campaign data (100 rows)",
    },
}


def resolve_csv_path(csv_path: Optional[str]) -> Path:
    """
    Resolve CSV path. Accepts a dataset alias (e.g. 'cinema', 'default')
    or a full file path. Falls back to DEFAULT_CSV_PATH if not provided.
    """
    if csv_path:
        alias = csv_path.strip().lower()
        if alias in DATA_SOURCES:
            return DATA_SOURCES[alias]["path"]
        return Path(csv_path).expanduser().resolve()
    return DEFAULT_CSV_PATH


def resolve_output_dir(output_dir: Optional[str]) -> Path:
    """
    Resolve output directory. Use default if not provided.
    """
    if output_dir:
        return Path(output_dir).expanduser().resolve()
    return DEFAULT_OUTPUT_DIR


@mcp.tool()
def list_data_sources() -> dict:
    """
    List all available raw data CSV files that can be used for report generation.
    Returns dataset names, file paths, and descriptions. Use the 'path' value
    as the csv_path argument in other tools (list_bu_names, preview_bu_report, generate_bu_report).
    """
    return {
        "status": "success",
        "sources": [
            {
                "name": name,
                "path": str(info["path"]),
                "exists": info["path"].exists(),
                "description": info["description"],
            }
            for name, info in DATA_SOURCES.items()
        ],
    }


@mcp.tool()
def list_bu_names(csv_path: Optional[str] = None) -> dict:
    """
    List all BU names available across all datasets (or a specific one).
    When csv_path is omitted, scans ALL data sources and returns every BU
    tagged with which dataset alias to use. Always pass that alias as csv_path
    when calling preview_bu_report or generate_bu_report.
    csv_path can be a dataset alias ('cinema', 'default') or a full file path.
    """
    if csv_path is not None:
        # Single dataset lookup
        try:
            final_csv_path = resolve_csv_path(csv_path)
            df = load_csv(str(final_csv_path))
            bu_names = (
                df["bu_name"].dropna().astype(str).str.strip().sort_values().unique().tolist()
            )
            return {
                "status": "success",
                "csv_path": str(final_csv_path),
                "count": len(bu_names),
                "bu_names": bu_names,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # No csv_path: scan all data sources
    all_bus = []
    errors = []
    for alias, info in DATA_SOURCES.items():
        try:
            df = load_csv(str(info["path"]))
            names = (
                df["bu_name"].dropna().astype(str).str.strip().sort_values().unique().tolist()
            )
            for name in names:
                all_bus.append({"bu_name": name, "dataset_alias": alias})
        except Exception as e:
            errors.append({"dataset_alias": alias, "error": str(e)})

    return {
        "status": "success",
        "note": "Pass dataset_alias as csv_path when calling preview_bu_report or generate_bu_report.",
        "count": len(all_bus),
        "bu_names": all_bus,
        "errors": errors,
    }


@mcp.tool()
def preview_bu_report(bu_name: str, csv_path: Optional[str] = None) -> dict:
    """
    Preview report data for one BU without generating the PowerPoint.
    Use this to inspect KPIs, top conditions, issues, and recommendations first.
    csv_path can be a dataset alias ('cinema', 'default') or a full file path.
    If the user mentions Cinema, use csv_path='cinema'.
    """
    try:
        final_csv_path = resolve_csv_path(csv_path)
        df = load_csv(str(final_csv_path))
        bu_df = filter_by_bu(df, bu_name)

        report_data = build_report_data(bu_df, bu_name)

        return {
            "status": "success",
            "bu_name": bu_name,
            "csv_path": str(final_csv_path),
            "period": report_data["period"],
            "kpis": report_data["team_overview"]["kpis"],
            "top_conditions": report_data["condition_analysis"]["top_conditions"],
            "issues": report_data["quality_issues"],
            "recommendations": report_data["recommendations"],
        }
    except Exception as e:
        return {
            "status": "error",
            "bu_name": bu_name,
            "message": str(e),
        }


@mcp.tool()
def generate_bu_report(
    bu_name: str,
    csv_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> dict:
    """
    Generate a PowerPoint segmentation report for one BU from the CSV.
    csv_path can be a dataset alias ('cinema', 'default') or a full file path.
    If the user mentions Cinema, use csv_path='cinema'.
    """
    try:
        final_csv_path = resolve_csv_path(csv_path)
        final_output_dir = resolve_output_dir(output_dir)

        df = load_csv(str(final_csv_path))
        bu_df = filter_by_bu(df, bu_name)

        report_data = build_report_data(bu_df, bu_name)

        output_path = final_output_dir / f"{bu_name.upper()}_report.pptx"
        saved_file = write_ppt(report_data, str(output_path))

        return {
            "status": "success",
            "bu_name": bu_name,
            "csv_path": str(final_csv_path),
            "output_file": saved_file,
            "period": report_data["period"],
            "kpis": report_data["team_overview"]["kpis"],
        }
    except Exception as e:
        return {
            "status": "error",
            "bu_name": bu_name,
            "message": str(e),
        }


@mcp.prompt()
def analyze_bu(bu_name: str, csv_path: Optional[str] = None) -> str:
    """
    Deep dive analysis for a single BU.
    Calls preview_bu_report and returns a structured analyst report.
    """
    csv_arg = f", csv_path='{csv_path}'" if csv_path else ""
    return f"""You are a data analyst specializing in marketing segmentation quality.

Call the tool: preview_bu_report(bu_name="{bu_name}"{csv_arg})

Then respond using exactly this structure (fill in values from the tool result):

## BU Deep Dive: {bu_name}
period=<period> | campaigns=<N> | segments=<N> | operators=<N> | avg_cond_per_seg=<X>

### Condition Analysis
top_conditions: [<name>(<count>), ...]
type_mix: CDP=<N>, BQ=<N>, OTHER=<N>

### Quality Issues
<one bullet per issue from the issues list>

### Recommendations
<one bullet per recommendation, prefix with R1, R2, ...>

### Operator Profiles
<one bullet per operator profile>

### Executive Summary
<2-3 sentences: overall segmentation health, biggest risk, top action item>

Rules:
- Use exact numbers from the tool result, never estimate
- Keep bullets concise (≤15 words each)
- Executive Summary must be data-backed, no filler phrases"""


@mcp.prompt()
def executive_summary(bu_name: str, csv_path: Optional[str] = None) -> str:
    """
    Concise 5-line executive summary card for a BU.
    """
    csv_arg = f", csv_path='{csv_path}'" if csv_path else ""
    return f"""You are a data analyst. Call: preview_bu_report(bu_name="{bu_name}"{csv_arg})

Then respond with exactly this 5-line card (no extra text):

BU: {bu_name} | period=<period> | campaigns=<N> | segments=<N> | operators=<N>
reuse_ratio=<campaigns/segments rounded to 2dp> | avg_cond_per_seg=<X> | top_condition=<NAME> (<N> uses)
issues_flagged=<count of issues>
top_recommendation=<first recommendation verbatim>
verdict=<one sentence: health rating and single most important action>

Rules:
- Compute reuse_ratio = total_campaigns / total_segments, round to 2 decimal places
- issues_flagged = length of the issues list
- No markdown headers, no extra lines, exactly 5 lines"""


@mcp.prompt()
def compare_bus(bu_name_1: str, bu_name_2: str, csv_path: Optional[str] = None) -> str:
    """
    Side-by-side comparison of two BUs.
    """
    csv_arg = f", csv_path='{csv_path}'" if csv_path else ""
    return f"""You are a data analyst. Call these two tools in sequence:
1. preview_bu_report(bu_name="{bu_name_1}"{csv_arg})
2. preview_bu_report(bu_name="{bu_name_2}"{csv_arg})

Then respond using exactly this structure:

## BU Comparison: {bu_name_1} vs {bu_name_2}

| metric | {bu_name_1} | {bu_name_2} |
|---|---|---|
| campaigns | <N> | <N> |
| segments | <N> | <N> |
| operators | <N> | <N> |
| avg_cond_per_seg | <X> | <X> |
| reuse_ratio | <X> | <X> |
| top_condition | <NAME> | <NAME> |
| issues_flagged | <N> | <N> |

### Key Differences
<2-4 bullets: metrics where the two BUs diverge most>

### Recommendation Focus
- {bu_name_1}: <top recommendation for this BU>
- {bu_name_2}: <top recommendation for this BU>

Rules:
- reuse_ratio = total_campaigns / total_segments, round to 2dp
- Only highlight differences that are meaningful (>20% gap or different top condition)
- No speculation beyond what the tool data shows"""


@mcp.prompt()
def analyze_all_bus(csv_path: Optional[str] = None) -> str:
    """
    Fleet-wide health analysis across all BUs.
    """
    csv_arg = f"csv_path='{csv_path}'" if csv_path else ""
    return f"""You are a data analyst. Execute this workflow:

Step 1 — Call: list_bu_names({csv_arg})
Step 2 — For each BU in the result, call: preview_bu_report(bu_name=<BU>{", " + csv_arg if csv_arg else ""})
Step 3 — Respond using exactly this structure:

## All-BU Segmentation Health Report

| bu | campaigns | segments | avg_cond_per_seg | reuse_ratio | issues_flagged |
|---|---|---|---|---|---|
<one row per BU, sorted by issues_flagged descending>

### Common Issues Across BUs
<bullets: issues that appear in 2+ BUs>

### Top Performers
<bullets: BUs with 0 issues and reuse_ratio > 1.5>

### BUs Needing Attention
<bullets: BUs with the most issues, include their top recommendation>

Rules:
- reuse_ratio = total_campaigns / total_segments, round to 2dp
- issues_flagged = length of each BU's issues list
- Process every BU returned by list_bu_names, skip none"""


@mcp.prompt()
def generate_all_reports(
    csv_path: Optional[str] = None, output_dir: Optional[str] = None
) -> str:
    """
    Batch generate PowerPoint reports for all BUs and report status.
    """
    csv_arg = f"csv_path='{csv_path}'" if csv_path else ""
    out_arg = f"output_dir='{output_dir}'" if output_dir else ""
    tool_args = ", ".join(filter(None, [csv_arg, out_arg]))
    list_args = csv_arg
    return f"""You are a data analyst running batch report generation.

Step 1 — Call: list_bu_names({list_args})
Step 2 — For each BU, call: generate_bu_report(bu_name=<BU>{", " + tool_args if tool_args else ""})
Step 3 — Respond using exactly this structure:

## Batch Report Generation

| bu | status | output_file | period |
|---|---|---|---|
<one row per BU: status=success or error, output_file=path, period=period or error message>

summary: <N> succeeded, <N> failed

Rules:
- Process every BU from list_bu_names, skip none
- If a BU fails, record status=error and put the error message in the output_file column
- Call generate_bu_report sequentially (one at a time), not in parallel"""


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()