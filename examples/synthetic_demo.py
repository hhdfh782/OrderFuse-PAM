"""Synthetic demonstration; it does not reproduce manuscript experiments."""

from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orderfuse_pam import (  # noqa: E402
    apparent_fwhm,
    bonferroni,
    exact_two_sided_sign_test,
    exchange_nrmse,
    hierarchical_case_summary,
    relative_nrmse,
)

rng = np.random.default_rng(7)
clean = rng.normal(size=(16, 16, 16))
perturbed = clean + 0.01 * rng.normal(size=clean.shape)

print("output-change NRMSE:", relative_nrmse(perturbed, clean))
print("exchange NRMSE:", exchange_nrmse(clean, clean.copy()))
differences = [-0.1] * 8
p = exact_two_sided_sign_test(differences)
print("exact sign p:", p)
print("Bonferroni-adjusted p:", bonferroni([p, p, p]).tolist())
print("hierarchical summary:", hierarchical_case_summary(rng.random((8, 3, 3))))
print("apparent FWHM:", apparent_fwhm([0, 1, 3, 1, 0]))

