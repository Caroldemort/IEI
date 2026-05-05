import numpy as np
import pandas as pd


def assign_initial_weights(
    validation_report: pd.DataFrame,
    domain_weights: dict,
) -> pd.DataFrame:
    """
    Assigns provisional marker weights based on biological domains.
    """

    available = validation_report[
        validation_report["available"] == True
    ].copy()

    weights = []

    for domain, domain_weight in domain_weights.items():
        domain_features = available[available["domain"] == domain]

        if domain_features.empty:
            continue

        per_marker_weight = domain_weight / len(domain_features)

        for _, row in domain_features.iterrows():
            weights.append({
                "marker_id": row["marker_id"],
                "selected_column": row["selected_column"],
                "domain": row["domain"],
                "modality": row["modality"],
                "core": row["core"],
                "weight": per_marker_weight,
            })

    weights_df = pd.DataFrame(weights)

    if not weights_df.empty:
        weights_df["weight"] = weights_df["weight"] / weights_df["weight"].sum()

    return weights_df


def compute_iai(
    normalized_df: pd.DataFrame,
    weights_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes the Immune Exhaustion Index (IAI).
    """

    if normalized_df.empty:
        raise ValueError("normalized_df is empty.")

    if weights_df.empty:
        raise ValueError("weights_df is empty.")

    required_columns = {"marker_id", "weight"}
    missing_columns = required_columns - set(weights_df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns in weights_df: {missing_columns}")

    markers_in_weights = weights_df["marker_id"].tolist()
    available_markers = [m for m in markers_in_weights if m in normalized_df.columns]

    if not available_markers:
        raise ValueError("No available markers to compute IAI.")

    weights_used = weights_df[weights_df["marker_id"].isin(available_markers)].copy()
    weights_used["weight"] = weights_used["weight"] / weights_used["weight"].sum()

    normalized_subset = normalized_df[weights_used["marker_id"]]
    iai_values = normalized_subset.dot(weights_used["weight"].values)

    iai_scores = pd.DataFrame({"IAI": iai_values}, index=normalized_df.index)

    return iai_scores, weights_used


def classify_iai(
    iai_scores: pd.DataFrame,
    low_cutoff: float = 0.33,
    high_cutoff: float = 0.66,
) -> pd.DataFrame:
    """
    Classifies IAI values as low, intermediate or high.
    """

    if "IAI" not in iai_scores.columns:
        raise ValueError("iai_scores must contain a column named 'IAI'.")

    classified_scores = iai_scores.copy()

    def assign_category(value):
        if pd.isna(value):
            return np.nan
        if value <= low_cutoff:
            return "low"
        if value <= high_cutoff:
            return "intermediate"
        return "high"

    classified_scores["IAI_category"] = classified_scores["IAI"].apply(assign_category)

    return classified_scores