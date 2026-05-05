import numpy as np
import pandas as pd


def normalize_input(
    df: pd.DataFrame,
    validation_report: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Normalizes available IAI markers to a 0-1 scale using min-max scaling.
    """

    available_features = validation_report[
        validation_report["available"] == True
    ].copy()

    normalized_data = {}
    params = []

    for _, row in available_features.iterrows():
        marker_id = row["marker_id"]
        column = row["selected_column"]

        values = pd.to_numeric(df[column], errors="coerce")

        min_value = values.min()
        max_value = values.max()

        if pd.isna(min_value) or pd.isna(max_value):
            normalized_values = pd.Series(np.nan, index=df.index)
        elif max_value == min_value:
            normalized_values = pd.Series(0.0, index=df.index)
        else:
            normalized_values = (values - min_value) / (max_value - min_value)

        normalized_data[marker_id] = normalized_values

        params.append({
            "marker_id": marker_id,
            "source_column": column,
            "min_value": min_value,
            "max_value": max_value,
            "modality": row["modality"],
            "domain": row["domain"],
            "core": row["core"],
        })

    normalized_df = pd.DataFrame(normalized_data, index=df.index)
    normalization_params = pd.DataFrame(params)

    return normalized_df, normalization_params