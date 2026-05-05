from .config import (
    get_marker_catalog,
    get_feature_map,
    get_initial_domain_weights,
)

from .features import validate_input
from .preprocessing import normalize_input
from .scoring import assign_initial_weights, compute_iai, classify_iai
from .reporting import build_iai_report