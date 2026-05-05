import pandas as pd


def detect_modality(column_name: str | None) -> str | None:
    """
    Detects the experimental modality from a column name.
    """

    if column_name is None:
        return None

    if "MFI" in column_name or "percent" in column_name:
        return "flow"
    if "pg_ml" in column_name:
        return "elisa"
    if "relative" in column_name or "ratio" in column_name:
        return "western_blot"

    return "rna"


def validate_input(
    df: pd.DataFrame,
    feature_map: dict,
    marker_catalog: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """
    Validates which IAI markers are available in the input dataset.

    Parameters
    ----------
    df:
        Input dataset. Rows are samples and columns are features.

    feature_map:
        Dictionary mapping marker IDs to accepted column names.

    marker_catalog:
        Master marker catalog.

    Returns
    -------
    validation_report:
        Marker-level availability report.

    summary:
        Dataset-level coverage summary.
    """

    detected = []

    for marker_id, possible_columns in feature_map.items():
        found_columns = [col for col in possible_columns if col in df.columns]

        if found_columns:
            available = True
            selected_column = found_columns[0]
            modality = detect_modality(selected_column)
        else:
            available = False
            selected_column = None
            modality = None

        catalog_row = marker_catalog[marker_catalog["marker_id"] == marker_id]

        if not catalog_row.empty:
            domain = catalog_row["domain"].iloc[0]
            core = bool(catalog_row["core"].iloc[0])
        else:
            domain = None
            core = False

        detected.append({
            "marker_id": marker_id,
            "available": available,
            "selected_column": selected_column,
            "all_matching_columns": found_columns,
            "modality": modality,
            "domain": domain,
            "core": core,
        })

    validation_report = pd.DataFrame(detected)

    total_markers = len(validation_report)
    available_markers = int(validation_report["available"].sum())

    core_markers = int(validation_report["core"].sum())
    available_core_markers = int(
        (validation_report["available"] & validation_report["core"]).sum()
    )

    coverage = available_markers / total_markers if total_markers > 0 else 0
    core_coverage = available_core_markers / core_markers if core_markers > 0 else 0

    if coverage >= 0.80 and core_coverage >= 0.80:
        score_type = "full"
        reliability = "high"
    elif core_coverage >= 0.60:
        score_type = "core"
        reliability = "moderate"
    else:
        score_type = "approx"
        reliability = "low"

    summary = {
        "total_markers": total_markers,
        "available_markers": available_markers,
        "coverage": round(float(coverage), 3),
        "core_markers": core_markers,
        "available_core_markers": available_core_markers,
        "core_coverage": round(float(core_coverage), 3),
        "score_type": score_type,
        "reliability": reliability,
    }

    return validation_report, summary