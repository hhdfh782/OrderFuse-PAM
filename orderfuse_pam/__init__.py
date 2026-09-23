"""Public evaluation utilities for the OrderFuse-PAM preview."""

from .metrics import (
    apparent_fwhm,
    bonferroni,
    exact_two_sided_sign_test,
    exchange_nrmse,
    hierarchical_case_summary,
    relative_nrmse,
)

__all__ = [
    "apparent_fwhm",
    "bonferroni",
    "exact_two_sided_sign_test",
    "exchange_nrmse",
    "hierarchical_case_summary",
    "relative_nrmse",
]

