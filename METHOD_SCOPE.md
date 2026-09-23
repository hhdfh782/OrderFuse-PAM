# Public method scope

OrderFuse-PAM studies two-source volumetric photoacoustic fusion under source exchange and unequal noise. The paper evaluates complementary convex source weights, structural order consistency, and perturbation sensitivity.

This preview exposes only the definitions needed to independently inspect reported metrics:

- **Exchange NRMSE:** relative difference between outputs obtained from reversed source order.
- **Output-change NRMSE:** relative difference between a method's perturbed-input output and its own clean-input output.
- **Exact sign test:** a paired volume is the statistical unit; training and noise seeds are technical or model repeats, not extra acquisitions.
- **Projected branch FWHM:** descriptive half-height width on a fixed profile; it is not a calibrated point-spread-function resolution measurement.

The preview does not specify the unpublished network, preprocessing, training schedule, or data membership needed to recreate paper results.

