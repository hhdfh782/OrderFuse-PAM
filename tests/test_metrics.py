import unittest

import numpy as np

from orderfuse_pam import (
    apparent_fwhm,
    bonferroni,
    exact_two_sided_sign_test,
    exchange_nrmse,
    hierarchical_case_summary,
    relative_nrmse,
)


class MetricTests(unittest.TestCase):
    def test_identity_metrics_are_zero(self):
        x = np.arange(8, dtype=float).reshape(2, 2, 2)
        self.assertEqual(relative_nrmse(x, x), 0.0)
        self.assertEqual(exchange_nrmse(x, x), 0.0)

    def test_eight_concordant_pairs(self):
        p = exact_two_sided_sign_test([-1.0] * 8)
        self.assertAlmostEqual(p, 0.0078125)
        self.assertAlmostEqual(float(bonferroni([p, p, p])[0]), 0.0234375)

    def test_hierarchy_uses_cases(self):
        x = np.ones((8, 3, 3))
        result = hierarchical_case_summary(x)
        self.assertEqual(result["n_cases"], 8)
        self.assertEqual(result["mean"], 1.0)

    def test_fwhm(self):
        self.assertAlmostEqual(apparent_fwhm([0, 1, 3, 1, 0]), 1.5)


if __name__ == "__main__":
    unittest.main()

