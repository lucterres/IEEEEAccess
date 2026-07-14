# Response to Reviewers

**Manuscript:** Context-oriented Synthesis of Salt Domes in Labeled Seismic Images  
**Authors:** Luciano D. Terres and Jacob Scharcanski  
**Journal:** IEEE Access  

---

We thank the reviewers for their careful reading of the manuscript and for their constructive comments. We have addressed each point below. Changes to the manuscript are indicated in the revised version.

---

## Response to Reviewer 1

### Comment R1.3 — Expert Evaluation Design

> *"It is not clear whether the experts were blinded to the real/synthetic distinction. If not, please acknowledge this as a limitation. Also clarify whether real and synthetic images were mixed during evaluation."*

**Response:**

We thank the reviewer for this important methodological observation. We fully agree that the original evaluation design — where real and synthetic images were presented in separate, sequential phases — does not constitute a formal blind discrimination test, and that this represents a significant limitation of the original submission.

**What the original evaluation did:**  
The prior evaluation was conducted in two sequential, separate phases: experts first annotated 20 real seismic images (to establish a performance baseline), and then annotated 30 synthetic seismic images in a second, distinct phase. The experts were aware they were evaluating synthetic images in the second phase. This design measured the specialists' ability to correctly identify salt body structures (via F1-score), but did **not** test their ability to distinguish real from synthetic images.

**Action taken in the revised manuscript:**  
In response to this limitation, we have **redesigned the expert evaluation as a formal blind discrimination experiment**. The revised protocol, now described in Section IV-C of the manuscript, is as follows:

- Real and synthetic seismic images from the TGS Salt Identification Challenge dataset are presented to expert geoscientists in a **single, randomized, interleaved sequence**;
- Experts are **not informed** of the origin of each image prior to evaluation;
- For each image, experts are asked to: (1) **classify** the image as *real* or *synthetic*, and (2) **segment** the salt body regions;
- Control images without any saline body are included in the stimulus set;
- Image identity and sequence are **fully randomized** across participants to avoid order effects.

This design provides direct evidence for the "virtually indistinguishable" hypothesis and fully addresses the reviewer's concern.

**Current status:**  
The blind experiment is currently being conducted. The prior sequential evaluation results (Tables previously reporting F1-scores of 0.88159 for real and 0.86901 for synthetic images) have been **removed from the manuscript PDF** and are preserved only as a commented-out reference in the source file. A prominent placeholder (`TODO` marker) has been inserted in the manuscript in all relevant locations — Abstract, Section IV-C (Qualitative Evaluation), and Section V (Concluding Remarks) — to clearly indicate where the new results will be incorporated once available.

---

*[Additional responses to Reviewer 1 — Comments R1.1, R1.2, R1.4 — to be added]*

---

## Response to Reviewer 2

*[Responses to Reviewer 2 comments — to be added]*

---
