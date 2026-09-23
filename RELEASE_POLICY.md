# Release policy

## Preview stage

The preview contains only evaluation and auditing utilities. It excludes any file that would disclose private data paths, unpublished model implementation, trained parameters, experiment manifests, or source volumes.

## Acceptance stage

Subject to paper acceptance and permission review, a later tagged release may add:

1. model and training source code;
2. inference and patch-blending implementation;
3. checkpoints with checksums and license terms;
4. public or access-controlled data instructions;
5. frozen experiment configurations and result manifests;
6. an end-to-end reproduction guide.

The preview history will remain available. The full release should use a new semantic version and document every newly released artifact.

