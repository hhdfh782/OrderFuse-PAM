"""Metrics disclosed in the pre-acceptance OrderFuse-PAM preview."""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence

import numpy as np


def relative_nrmse(changed: np.ndarray, reference: np.ndarray, eps: float = 1e-12) -> float:
    """Return ||changed-reference||_2 / max(||reference||_2, eps)."""
    changed = np.asarray(changed, dtype=np.float64)
    reference = np.asarray(reference, dtype=np.float64)
    if changed.shape != reference.shape:
        raise ValueError("changed and reference must have identical shapes")
    denominator = max(float(np.linalg.norm(reference.ravel())), float(eps))
    return float(np.linalg.norm((changed - reference).ravel()) / denominator)


def exchange_nrmse(output_ab: np.ndarray, output_ba: np.ndarray, eps: float = 1e-12) -> float:
    """Measure source-order inconsistency relative to the AB output."""
    return relative_nrmse(output_ba, output_ab, eps=eps)


def exact_two_sided_sign_test(differences: Sequence[float]) -> float:
    """Exact paired sign-test p-value after dropping zero differences."""
    values = np.asarray(differences, dtype=np.float64)
    values = values[values != 0]
    n = int(values.size)
    if n == 0:
        return 1.0
    positive = int(np.sum(values > 0))
    extreme = min(positive, n - positive)
    lower_tail = sum(math.comb(n, k) for k in range(extreme + 1)) / (2**n)
    return min(1.0, 2.0 * lower_tail)


def bonferroni(p_values: Iterable[float]) -> np.ndarray:
    """Return Bonferroni-adjusted p-values."""
    values = np.asarray(list(p_values), dtype=np.float64)
    if np.any((values < 0) | (values > 1)):
        raise ValueError("p-values must lie in [0, 1]")
    return np.minimum(1.0, values * values.size)


def hierarchical_case_summary(values: np.ndarray) -> dict[str, float | int]:
    """Average repeats, then model seeds, and summarize acquisition cases.

    Input dimensions are ``[case, model_seed, technical_repeat]``. This avoids
    treating repeats or training seeds as additional acquisition samples.
    """
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 3:
        raise ValueError("values must have shape [case, model_seed, technical_repeat]")
    per_case = values.mean(axis=2).mean(axis=1)
    return {
        "n_cases": int(per_case.size),
        "mean": float(per_case.mean()),
        "sample_sd": float(per_case.std(ddof=1)) if per_case.size > 1 else float("nan"),
    }


def apparent_fwhm(profile: Sequence[float]) -> float:
    """Return half-height width using a profile-minimum baseline.

    The crossings around the largest peak are linearly interpolated. This is a
    descriptive projected width, not a calibrated optical resolution metric.
    """
    y = np.asarray(profile, dtype=np.float64)
    if y.ndim != 1 or y.size < 3 or not np.all(np.isfinite(y)):
        raise ValueError("profile must be a finite one-dimensional sequence")
    peak = int(np.argmax(y))
    baseline = float(np.min(y))
    half = baseline + (float(y[peak]) - baseline) / 2.0
    left = next((i for i in range(peak - 1, -1, -1) if y[i] <= half), None)
    right = next((i for i in range(peak + 1, y.size) if y[i] <= half), None)
    if left is None or right is None:
        raise ValueError("profile has no two-sided half-height crossings")
    left_x = left + (half - y[left]) / (y[left + 1] - y[left])
    right_x = right - 1 + (half - y[right - 1]) / (y[right] - y[right - 1])
    return float(right_x - left_x)

