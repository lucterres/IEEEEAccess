# Response to Reviewers

**Original Manuscript ID:** Access-2026-27912  
**Original Article Title:** Context-oriented Synthesis of Salt Domes in Labeled Seismic Images

To: IEEE Access Editor

Re: Response to reviewers

**Authors:** Luciano D. Terres and Jacob Scharcanski  
**Journal:** IEEE Access  
**Revision submitted:** July 2026

---

Dear Editor,

We thank the reviewers for their careful reading of the manuscript and for their constructive comments. We have addressed each point below. All changes to the manuscript are highlighted in the accompanying Highlighted PDF (`latex_build/Highlighted_PDF.pdf`), where additions appear in yellow and deletions appear strikethrough.
---

## Response to Reviewer 1

### Comment R1.1 — Comparison with Henriques et al.

> *"The related work mentions their approach, but does not clearly articulate the technical novelty of your method. Please explicitly state the main architectural differences and why your texture synthesis strategy is advantageous over their generative model."*

**Response:**

We thank the reviewer for this observation. We agree that the original manuscript did not sufficiently differentiate the proposed method from Henriques et al.~[Henriques2021]. The original paragraph (Section II, Related Work) described their method only briefly as *"a very similar data augmentation method"* without articulating the specific architectural and practical differences.

**Author Action taken in the revised manuscript (_v7.tex):**  
The paragraph describing Henriques et al. in **Section II (Related Work)** was substantially rewritten to explicitly contrast the two approaches along three dimensions:

1. **Architecture for texture synthesis:** Henriques et al. use a **Conditional Normalizing Flow (CNF)** model as the second stage of their pipeline to synthesize seismic textures conditioned on VAE-generated masks. The proposed method replaces this learned generative texture model with a **non-parametric context-oriented texture synthesis algorithm** — a fundamentally different design choice.

2. **Data requirements:** The CNF model of Henriques et al. requires training on **24,872 annotated patch pairs**, which is a significant burden in geoscience applications where large annotated datasets are rarely available. The proposed texture synthesis component **requires no training** and operates directly from a small set of reference patches, making it more practical in data-scarce scenarios.

3. **Handling of non-stationary textures:** The proposed method explicitly decomposes the seismic image into **three distinct geological zones** (salt body, surrounding rock, and boundary regions) and synthesizes each zone independently. This zone-specific treatment directly captures the non-stationary texture properties inherent to seismic data — a property not explicitly modeled by Henriques et al.

4. **Evaluation strategy:** Henriques et al. evaluate their results only indirectly, measuring improvements in downstream segmentation performance on a different synthetic dataset, which precludes a direct quantitative comparison with the proposed method. The proposed work provides both qualitative expert evaluation and direct quantitative image similarity measures (MSE, DSSIM, LBP Distance) on the same dataset.

**Changes made to the manuscript:**

- **Section II (Related Work), paragraph on Henriques et al.** *(line 94 in `_v7.tex`)*: The original two-sentence description was replaced by a detailed paragraph explicitly stating: (a) that both approaches share the VAE for mask generation; (b) that the key divergence is in the texture synthesis stage (CNF vs. non-parametric context-oriented); (c) the data requirement contrast (24,872 annotated pairs vs. training-free); (d) the zone-decomposition advantage for non-stationary textures; and (e) the evaluation strategy difference.

**Revised paragraph (lines 94–103 in `_v7.tex`):**

> *"Similarly, Henriques et al. [Henriques2021] proposed a two-stage generative pipeline for data augmentation. In their method, a VAE generates salt body masks, and a Conditional Normalizing Flow (CNF) model subsequently synthesizes seismic image patches conditioned on those masks. While both approaches use a VAE for mask generation, they differ fundamentally in architecture and practice. The CNF model for texture synthesis required training on 24,872 annotated patch pairs, which hinders implementation where only small annotated seismic datasets are available, a common situation in geosciences applications. In contrast, the proposed method replaces the learned generative texture model with a non-parametric context-oriented texture synthesis algorithm that does not require training and operates directly from a small set of reference patches. By explicitly decomposing the seismic image into distinct geological zones — salt body, surrounding rock, and boundary regions — and synthesizing each zone independently, the proposed method also captures the non-stationary texture properties inherent to seismic data. Finally, Henriques et al. evaluate their results only indirectly, measuring improvements in downstream segmentation performance on a different synthetic dataset, which precludes a direct quantitative comparison."*

---

### Comment R1.3 — Expert Evaluation Design

>
> *"It is not clear whether the experts were blinded to the real/synthetic distinction. If not, please acknowledge this as a limitation. Also clarify whether real and synthetic images were mixed during evaluation."*
>

**Response:**

We thank the reviewer for this important methodological observation. We fully agree that the original evaluation design — where real and synthetic images were presented in separate, sequential phases — does not constitute a formal blind discrimination test, and that this represents a significant limitation of the original submission.

**Author Action taken in the revised manuscript (_v7.tex):**  
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

*[Additional responses to Reviewer 1 — Comments R1.2, R1.4 — to be added]*

---

## Response to Reviewer 2
*[Responses to Reviewer 2 comments — to be added]*

---

---

## Summary of Changes in the Revised Manuscript (_v7)

The table below lists every change made to the manuscript in response to reviewer comments. Each item references the affected section and the exact line numbers in `_v7.tex`.


| # | Section                             | Line(s) in `_v7.tex` | Change Type          | Description                                                                                                                                                                                                                                                                                                                           |
|---|-------------------------------------|----------------------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0 | Section II — Related Work           | 94–103               | **Replaced**         | Paragraph on Henriques et al. substantially rewritten. Now explicitly contrasts: (a) CNF vs. non-parametric texture synthesis; (b) data requirements (24,872 annotated pairs vs. training-free); (c) zone-decomposition advantage for non-stationary textures; (d) evaluation strategy. Addresses Reviewer 1, Comment 1. |
| 1 | Abstract                            | 59                   | **Replaced**         | Removed reference to sequential evaluation results. Added sentence describing the blind discrimination experiment as currently being conducted. Added `[TODO: Update abstract with blind experiment results when available.]` marker.                                                                                                 |
| 2 | Section IV, Criterion 1             | 351–363            | **Replaced**         | The first evaluation criterion was rewritten from sequential expert evaluation to *"Qualitative Evaluation by Experts — Blind Discrimination Experiment"*. Description now reflects randomized, interleaved presentation. Added `[TODO: Replace this description with the results of the blind experiment when available.]` marker. |
| 3 | Section IV-C, subsection heading    | 488                  | **Kept**             | `\subsection{Qualitative Evaluation}` retained; introductory sentence updated (line 490).                                                                                                                                                                                                                                             |
| 4 | Section IV-C, new subsubsection     | 492                  | **Added**            | New `\subsubsection{Blind Discrimination Experiment Protocol}` inserted at line 492.                                                                                                                                                                                                                                                  |
| 5 | Section IV-C, protocol description  | 493–501            | **Added**            | Full description of the blind experiment: randomized interleaved presentation, experts unaware of image origin, two tasks per image (classify as real/synthetic + segment salt body), inclusion of control images without salt, full randomization across participants.                                                               |
| 6 | Section IV-C, TODO placeholder      | 503–507            | **Added**            | Yellow-highlighted `TODO` box (lines 504–506) stating that the blind experiment is in progress and that results (classification accuracy, segmentation F1-scores) will replace the placeholder.                                                                                                                                     |
| 7 | Section IV-C, old evaluation tables | 451–485            | **Removed from PDF** | The two tables reporting sequential evaluation results (F1 = 0.88159 for real, F1 = 0.86901 for synthetic) were wrapped in `\begin{comment}` (line 451) / `\end{comment}` (line 485) and are thus absent from the compiled PDF. Preserved in source as historical reference.                                                          |
| 8 | Section V (Concluding Remarks)      | 614                  | **Replaced**         | The paragraph summarizing expert evaluation results was updated to state that the formal blind experiment is currently being conducted. Added `[TODO: Update this paragraph with the results of the blind expert evaluation experiment, replacing the preliminary sequential evaluation results.]` marker.                            |