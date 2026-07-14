# Response to Reviewers

**Original Manuscript ID:** Access-2026-27912  
**Original Article Title:** Context-oriented Synthesis of Salt Domes in Labeled Seismic Images  

To: IEEE Access Editor

Re: Response to reviewers


**Authors:** Luciano D. Terres and Jacob Scharcanski  
**Journal:** IEEE Access  
**Revision submitted:** July 2026

---

We thank the reviewers for their careful reading of the manuscript and for their constructive comments. We have addressed each point below. All changes to the manuscript are highlighted in the accompanying Highlighted PDF (`latex_build/review_clean.pdf`), where additions appear in blue and deletions appear in red strikethrough.

---

## Summary of Changes in the Revised Manuscript (_v7)

The table below lists every change made to the manuscript in response to reviewer comments. Each item references the affected section and the exact line numbers in `_v7.tex`.

| # | Section | Line(s) in `_v7.tex` | Change Type | Description |
|---|---------|----------------------|-------------|-------------|
| 1 | Abstract | 59 | **Replaced** | Removed reference to sequential evaluation results. Added sentence describing the blind discrimination experiment as currently being conducted. Added `[TODO: Update abstract with blind experiment results when available.]` marker. |
| 2 | Section IV, Criterion 1 | 351–363 | **Replaced** | The first evaluation criterion was rewritten from sequential expert evaluation to *"Qualitative Evaluation by Experts — Blind Discrimination Experiment"*. Description now reflects randomized, interleaved presentation. Added `[TODO: Replace this description with the results of the blind experiment when available.]` marker. |
| 3 | Section IV-C, subsection heading | 488 | **Kept** | `\subsection{Qualitative Evaluation}` retained; introductory sentence updated (line 490). |
| 4 | Section IV-C, new subsubsection | 492 | **Added** | New `\subsubsection{Blind Discrimination Experiment Protocol}` inserted at line 492. |
| 5 | Section IV-C, protocol description | 493–501 | **Added** | Full description of the blind experiment: randomized interleaved presentation, experts unaware of image origin, two tasks per image (classify as real/synthetic + segment salt body), inclusion of control images without salt, full randomization across participants. |
| 6 | Section IV-C, TODO placeholder | 503–507 | **Added** | Yellow-highlighted `TODO` box (lines 504–506) stating that the blind experiment is in progress and that results (classification accuracy, segmentation F1-scores) will replace the placeholder. |
| 7 | Section IV-C, old evaluation tables | 451–485 | **Removed from PDF** | The two tables reporting sequential evaluation results (F1 = 0.88159 for real, F1 = 0.86901 for synthetic) were wrapped in `\begin{comment}` (line 451) / `\end{comment}` (line 485) and are thus absent from the compiled PDF. Preserved in source as historical reference. |
| 8 | Section V (Concluding Remarks) | 614 | **Replaced** | The paragraph summarizing expert evaluation results was updated to state that the formal blind experiment is currently being conducted. Added `[TODO: Update this paragraph with the results of the blind expert evaluation experiment, replacing the preliminary sequential evaluation results.]` marker. |

---

## Response to Reviewer 1

### Comment R1.3 — Expert Evaluation Design

> *"It is not clear whether the experts were blinded to the real/synthetic distinction. If not, please acknowledge this as a limitation. Also clarify whether real and synthetic images were mixed during evaluation."*

**Response:**

We thank the reviewer for this important methodological observation. We fully agree that the original evaluation design — where real and synthetic images were presented in separate, sequential phases — does not constitute a formal blind discrimination test, and that this represents a significant limitation of the original submission.

**What the original evaluation did (removed from revised manuscript):**  
The prior evaluation was conducted in two sequential, separate phases: experts first annotated 20 real seismic images (to establish a performance baseline), and then annotated 30 synthetic seismic images in a second, distinct phase. The experts were aware they were evaluating synthetic images in the second phase. This design measured the specialists' ability to correctly identify salt body structures (via F1-score), but did **not** test their ability to distinguish real from synthetic images. The tables reporting those results (F1-scores of 0.88159 for real and 0.86901 for synthetic images) have been removed from the manuscript PDF and are preserved only as a commented-out block in the source file.

**Action taken in the revised manuscript (_v7.tex):**  
In response to this limitation, we have **redesigned the expert evaluation as a formal blind discrimination experiment**. The revised protocol, now described in Section IV-C (*Blind Discrimination Experiment Protocol*) of the manuscript, is as follows:

- Real and synthetic seismic images from the TGS Salt Identification Challenge dataset are presented to expert geoscientists in a **single, randomized, interleaved sequence**;
- Experts are **not informed** of the origin of each image prior to evaluation;
- For each image, experts are asked to: (1) **classify** the image as *real* or *synthetic*, and (2) **identify and segment** the salt body regions using a graphics computer program;
- Control images without any saline body are included in the stimulus set to assess experts' baseline response tendency;
- Image identity and sequence are **fully randomized** across participants to avoid order effects.

This design provides direct evidence for the "virtually indistinguishable" hypothesis and fully addresses the reviewer's concern about blinding and image mixing.

**Changes made to each section of the manuscript:**

- **Abstract** *(line 59)*: Replaced the reference to the sequential evaluation with a sentence describing the blind discrimination experiment as currently being conducted. A `[TODO]` marker was added to indicate where results will be inserted.

- **Section IV, Criterion 1** *(lines 351–363)*: The qualitative evaluation criterion was rewritten. The title now reads *"Qualitative Evaluation by Experts — Blind Discrimination Experiment"* and the description introduces the blind protocol in the context of the dual evaluation strategy.

- **Section IV-C** *(lines 492–507)*: The subsection *Qualitative Evaluation* was restructured. A new subsubsection *Blind Discrimination Experiment Protocol* was added at line 492, describing the full experimental design. A prominent yellow/red `TODO` box (lines 504–506) was inserted as a placeholder for results.

- **Section IV-C, old tables** *(lines 451–485 in source)*: The two tables previously reporting sequential evaluation results were wrapped in `\begin{comment}` (line 451) / `\end{comment}` (line 485) and are thus absent from the compiled PDF. A source comment marks them as historical reference to be replaced by the blind experiment results.

- **Section V (Concluding Remarks)** *(line 614)*: The paragraph summarizing the expert evaluation outcome was updated to reflect the ongoing blind experiment and include a `[TODO]` marker for the final results.

**Current status:**  
The blind experiment is currently being conducted. All `[TODO]` markers in the manuscript indicate the exact locations where the results will be inserted upon completion of data collection.

---

*[Additional responses to Reviewer 1 — Comments R1.1, R1.2, R1.4 — to be added]*

---

## Response to Reviewer 2

*[Responses to Reviewer 2 comments — to be added]*

---
