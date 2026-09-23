# OrderFuse-PAM

Preview code release for **Order-Consistent Volumetric Photoacoustic Fusion: Guarantees and Noise--Fidelity Trade-offs**.

This repository currently provides the public evaluation layer used to audit source-order consistency, perturbation stability, exact paired statistics, and descriptive branch widths. It is intentionally a **pre-acceptance preview**, not a reproduction package.

## Included now

- dependency-light NumPy implementations of the reported metrics;
- exact two-sided sign tests with Bonferroni correction;
- hierarchical aggregation utilities that keep acquisition pairs, training seeds, and technical repeats distinct;
- apparent projected-branch FWHM measurement;
- a synthetic demonstration and unit tests;
- protocol and release documentation.

## Held until paper acceptance

- photoacoustic volumes and acquisition metadata;
- trained checkpoints and directional score tensors;
- model architecture and training implementation;
- data loaders, preprocessing constants, crop manifests, and inference pipeline;
- experiment configuration files and per-case outputs.

These components are withheld to protect the unpublished submission and because the underlying data and weights require a separate release review. Their absence means this preview **cannot reproduce the paper's numerical results**. Do not describe it as the full official implementation.

## Installation

```bash
python -m pip install -e .
```

## Run the synthetic example

```bash
python examples/synthetic_demo.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Planned acceptance release

After acceptance and completion of the data/weight permission review, the repository is intended to add training, inference, checkpoint, and data-access instructions. See [RELEASE_POLICY.md](RELEASE_POLICY.md).

## License

The preview code is released under the MIT License. Dataset and model-weight licenses will be specified separately if and when those artifacts are released.

