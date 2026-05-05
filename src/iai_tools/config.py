import pandas as pd


def get_marker_catalog() -> pd.DataFrame:
    """
    Returns the master marker catalog for the Immune Exhaustion Index (IAI).
    """

    return pd.DataFrame([
        {
            "marker_id": "PD1",
            "gene": "PDCD1",
            "protein": "PD-1",
            "domain": "phenotypic",
            "core": True,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["rna", "flow"],
        },
        {
            "marker_id": "CD39",
            "gene": "ENTPD1",
            "protein": "CD39",
            "domain": "phenotypic",
            "core": True,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["rna", "flow"],
        },
        {
            "marker_id": "TIM3",
            "gene": "HAVCR2",
            "protein": "TIM-3",
            "domain": "phenotypic",
            "core": False,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["rna", "flow"],
        },
        {
            "marker_id": "LAG3",
            "gene": "LAG3",
            "protein": "LAG-3",
            "domain": "phenotypic",
            "core": False,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["rna", "flow"],
        },
        {
            "marker_id": "CD73",
            "gene": "NT5E",
            "protein": "CD73",
            "domain": "phenotypic",
            "core": False,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["rna", "flow"],
        },
        {
            "marker_id": "TOX",
            "gene": "TOX",
            "protein": "TOX",
            "domain": "transcriptional_program",
            "core": True,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["rna", "western_blot", "flow_intracellular"],
        },
        {
            "marker_id": "TCF1",
            "gene": "TCF7",
            "protein": "TCF-1",
            "domain": "transcriptional_program",
            "core": False,
            "expected_direction": "context_dependent",
            "possible_modalities": ["rna", "western_blot", "flow_intracellular"],
        },
        {
            "marker_id": "IL10",
            "gene": "IL10",
            "protein": "IL-10",
            "domain": "functional",
            "core": True,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["rna", "elisa"],
        },
        {
            "marker_id": "TGFB1",
            "gene": "TGFB1",
            "protein": "TGF-beta",
            "domain": "functional",
            "core": True,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["rna", "elisa"],
        },
        {
            "marker_id": "IL6",
            "gene": "IL6",
            "protein": "IL-6",
            "domain": "functional_inflammatory_context",
            "core": False,
            "expected_direction": "context_dependent",
            "possible_modalities": ["rna", "elisa"],
        },
        {
            "marker_id": "PSTAT3",
            "gene": None,
            "protein": "p-STAT3/STAT3",
            "domain": "signaling",
            "core": True,
            "expected_direction": "increase_with_exhaustion",
            "possible_modalities": ["western_blot"],
        },
    ])


def get_feature_map() -> dict:
    """
    Returns accepted column names for each biological marker.
    """

    return {
        "PD1": ["PDCD1", "PD1_MFI", "PD1_percent"],
        "CD39": ["ENTPD1", "CD39_MFI", "CD39_percent"],
        "TIM3": ["HAVCR2", "TIM3_MFI", "TIM3_percent"],
        "LAG3": ["LAG3", "LAG3_MFI", "LAG3_percent"],
        "CD73": ["NT5E", "CD73_MFI", "CD73_percent"],
        "TOX": ["TOX", "TOX_relative"],
        "TCF1": ["TCF7", "TCF1_relative"],
        "IL10": ["IL10", "IL10_pg_ml"],
        "TGFB1": ["TGFB1", "TGFB1_pg_ml"],
        "IL6": ["IL6", "IL6_pg_ml"],
        "PSTAT3": ["pSTAT3_STAT3_ratio"],
    }


def get_initial_domain_weights() -> dict:
    """
    Returns provisional domain-level weights.
    These are temporary and should be replaced by model-derived weights later.
    """

    return {
        "phenotypic": 0.35,
        "functional": 0.25,
        "functional_inflammatory_context": 0.10,
        "transcriptional_program": 0.20,
        "signaling": 0.10,
    }