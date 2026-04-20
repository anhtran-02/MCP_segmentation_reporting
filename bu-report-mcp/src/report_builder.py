import argparse
from pathlib import Path

from csv_reader import load_csv, filter_by_bu
from metrics import build_report_data
from ppt_writer import write_ppt


DEFAULT_CSV_PATH = Path("data/segmentation_usage.csv")
DEFAULT_OUTPUT_DIR = Path("outputs")


def print_report_data(report_data: dict) -> None:
    print("\nBU REPORT SUMMARY")
    print("-" * 60)
    print(f"BU Name: {report_data['bu_name']}")
    print(f"Period: {report_data['period']}")

    kpis = report_data["team_overview"]["kpis"]

    print("\nKPIs")
    print("-" * 60)
    for key, value in kpis.items():
        print(f"{key}: {value}")

    print("\nTop Conditions")
    print("-" * 60)
    for item in report_data["condition_analysis"]["top_conditions"]:
        print(f"- {item['condition_name']}: {item['usage_count']}")

    print("\nQuality Issues")
    print("-" * 60)
    for item in report_data["quality_issues"]:
        print(f"- {item}")

    print("\nRecommendations")
    print("-" * 60)
    for item in report_data["recommendations"]:
        print(f"- {item}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a simple BU PowerPoint report from a local CSV."
    )
    parser.add_argument(
        "--bu",
        required=True,
        help="Business unit name, for example UTILITIES or TELCO",
    )
    parser.add_argument(
        "--csv",
        default=str(DEFAULT_CSV_PATH),
        help="Path to the CSV file",
    )

    args = parser.parse_args()

    print("=" * 60)
    print(f"Loading CSV: {args.csv}")
    print(f"Filtering BU: {args.bu}")
    print("=" * 60)

    df = load_csv(args.csv)
    bu_df = filter_by_bu(df, args.bu)

    report_data = build_report_data(bu_df, args.bu)
    print_report_data(report_data)

    output_path = DEFAULT_OUTPUT_DIR / f"{args.bu.upper()}_report.pptx"
    saved_file = write_ppt(report_data, str(output_path))

    print("\nPowerPoint created successfully.")
    print(f"Output file: {saved_file}")
    print("\nDone.")


if __name__ == "__main__":
    main()