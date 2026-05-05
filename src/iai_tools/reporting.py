import pandas as pd


def build_iai_report(
    original_df: pd.DataFrame,
    classified_iai: pd.DataFrame,
    summary: dict,
) -> pd.DataFrame:
    """
    Builds final IAI report with score, category, coverage and reliability.
    """

    report_df = original_df.copy()

    report_df["IAI"] = classified_iai["IAI"]
    report_df["IAI_category"] = classified_iai["IAI_category"]

    report_df["score_type"] = summary["score_type"]
    report_df["reliability"] = summary["reliability"]
    report_df["coverage"] = summary["coverage"]
    report_df["core_coverage"] = summary["core_coverage"]

    return report_df