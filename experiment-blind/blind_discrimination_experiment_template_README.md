# Blind Discrimination Experiment CSV — Column Guide

File: `blind_discrimination_experiment_template.csv`

This CSV is designed to record one row per **image × evaluator** in the blind discrimination experiment.

## Related files

- `blind_discrimination_experiment_template.csv` — evaluator responses and segmentation results
- `blind_discrimination_image_manifest.csv` — image ground truth / manifest

## Column definitions — evaluator response sheet

| Column | Meaning |
|---|---|
| `session_id` | Identifier of the experimental session or batch. |
| `evaluator_id` | Short identifier for the evaluator, e.g. `E1`, `E2`, `E3`. |
| `evaluator_name` | Full evaluator name or anonymized label. |
| `image_id` | Unique identifier of the image in the experiment. |
| `image_filename` | Filename of the displayed image. |
| `image_source_ground_truth` | True origin of the image: `real` or `synthetic`. |
| `random_order` | Presentation order for that evaluator. |
| `shown_timestamp` | Date/time when the image was shown, if available. |
| `predicted_source` | Evaluator judgment: `real` or `synthetic`. |
| `segmentation_mask_file` | Path or filename of the evaluator-produced segmentation mask. |
| `segmentation_done` | Whether segmentation was performed: `yes` or `no`. |
| `precision` | Precision of evaluator segmentation against ground truth. |
| `recall` | Recall of evaluator segmentation against ground truth. |
| `f1_score` | F1-score of evaluator segmentation against ground truth. |
| `notes` | Free-text observations, comments, anomalies, or special cases. |

## Column definitions — image manifest

| Column | Meaning |
|---|---|
| `session_id` | Identifier of the experimental session or batch. |
| `image_id` | Unique identifier of the image in the experiment. |
| `image_filename` | Filename of the image. |
| `image_source_ground_truth` | True origin of the image: `real` or `synthetic`. |
| `ground_truth_mask_file` | Path or filename of the corresponding ground-truth mask. |
| `randomization_pool` | Group used during randomization, e.g. `main` or `control`. |
| `notes` | Optional remarks about the image. |

## Recommended workflow

1. Use `blind_discrimination_image_manifest.csv` as the source of truth for image metadata.
2. Pre-fill these columns in `blind_discrimination_experiment_template.csv` before the session:
   - `session_id`
   - `evaluator_id`
   - `evaluator_name`
   - `image_id`
   - `image_filename`
   - `image_source_ground_truth`
   - `random_order`
3. During the session, fill:
   - `shown_timestamp`
   - `predicted_source`
   - `segmentation_mask_file`
   - `segmentation_done`
   - `notes`
4. After the session, compute and fill:
   - `precision`
   - `recall`
   - `f1_score`

## Suggested controlled values

- `image_source_ground_truth`: `real`, `synthetic`
- `predicted_source`: `real`, `synthetic`
- `segmentation_done`: `yes`, `no`
- `randomization_pool`: `main`, `control`

## Notes

- These CSVs were simplified to remain strictly aligned with the blind discrimination protocol described in `_v7.tex`.
- The manifest file is intended to remain fixed, while the experiment template is the file filled during evaluator sessions.
- If evaluator identity must be anonymized, keep only `evaluator_id` and remove personal names.
