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
### Comment R1.2 — VAE Implementation Details
> *"The architecture is described only as stacked dense layers. Please specify the number of neurons per layer, latent dimension d, training hyperparameters, and whether convolutional layers were used (and why)."*

**Response:**

We thank the reviewer for this precise and constructive request. The original manuscript described the VAE architecture only generically as *"a simple feedforward network"* with *"four stacked dense layers"* for the encoder and *"five stacked dense layers"* for the decoder, providing no quantitative detail. We have now fully specified the architecture, training configuration, and design rationale.

**Action taken in the revised manuscript (`_v7.tex`):**

The paragraph beginning *"We use the generated masks as contexts..."* in **Section III-A** (*Context Generation Using a Variational Autoencoder*) was replaced with a detailed implementation description covering:

1. **Input dimension:** grayscale masks, $1 \times 64 \times 64$
2. **Encoder architecture:** three `Conv2d` layers with channel progression $1 \to 128 \to 256 \to 512$ (kernel 3, stride 2, padding 1), followed by flattening and two linear projections for $\mu$ and $\log\sigma^2$
3. **Latent dimension:** $d = 100$
4. **Reparameterization:** $z = \mu + \sigma \odot \epsilon$, $\epsilon \sim \mathcal{N}(0, I)$
5. **Decoder architecture:** MLP with layers $100 \to 256 \to 512 \to 1024 \to 4096$, reshaped to $1 \times 64 \times 64$ + sigmoid
6. **Loss function:** standard VAE loss $\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{KL}}$ (BCE + KL), KL weighted by $N/B$
7. **Training hyperparameters:** 20 epochs, batch size 32, Adam optimizer (default learning rate), gradient clipping by norm at 1.0
8. **Justification for convolutional encoder:** preserves local spatial structure of masks (salt-body contours and region patterns), reduces parameter count versus a fully dense encoder, yields latent representations better suited to image data

**Revised text (Section III-A, `_v7.tex`):**

> *"The VAE model used in this work operates on grayscale seismic masks with input dimension $1 \times 64 \times 64$. The encoder is convolutional, consisting of three* `Conv2d` *layers with channel progression $1 \rightarrow 128 \rightarrow 256 \rightarrow 512$ (kernel size 3, stride 2, padding 1), followed by a flattening operation and two independent linear projections that output the parameters of the latent distribution, $\mu$ and $\log \sigma^2$, both with dimensionality $d = 100$. Latent codes are drawn via the reparameterization trick, $z = \mu + \sigma \odot \epsilon$, with $\epsilon \sim \mathcal{N}(0, I)$. The decoder is a multilayer perceptron (MLP) with fully connected layers $100 \rightarrow 256 \rightarrow 512 \rightarrow 1024 \rightarrow 4096$, whose output is reshaped to $1 \times 64 \times 64$ and passed through a sigmoid activation. The model is trained with the standard VAE loss $\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{KL}}$, where $\mathcal{L}_{\mathrm{rec}}$ is the binary cross-entropy reconstruction term and $\mathcal{L}_{\mathrm{KL}}$ is the KL-divergence regularizer towards $\mathcal{N}(0, I)$, weighted by a factor proportional to $N/B$ (dataset size over batch size). Training used 20 epochs, batch size 32, the Adam optimizer with its default learning rate, and gradient clipping by norm at 1.0. Convolutional layers were chosen for the encoder because they preserve and exploit the local spatial structure of the masks — capturing salt-body contours and region patterns — while substantially reducing the number of parameters compared to a fully dense encoder, and yielding latent representations better suited to image data."*

---
### Comment R1.3 — Expert Evaluation Design

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

## Response to Reviewer 2
### Comment R2.5 — Reproducibility

> *"The paper should improve reproducibility. Important implementation details are missing, including VAE latent dimension, training epochs, optimizer, learning rate, loss settings, patch size, boundary dilation width, texture database construction, and sampling parameters. These details are essential for readers who wish to reproduce or extend the work."*

**Response:**

We thank the reviewer for this detailed and constructive list of missing implementation details. We have addressed every item enumerated in the comment, distributing the information across two sections of the revised manuscript: VAE-related parameters in Section III-A, and texture synthesis parameters in Section III-B.

**Action taken in the revised manuscript (`_v7.tex`):**

**Section III-A** (*Context Generation Using a Variational Autoencoder*) — VAE parameters:

| Parameter requested | Value added to manuscript |
|---|---|
| VAE latent dimension | $d = 100$ |
| Training epochs | 20 |
| Optimizer | Adam (default learning rate) |
| Loss settings | BCE reconstruction + KL divergence, KL weighted by $N/B$ |
| Architecture (neurons/layers) | Encoder: Conv2d $1\to128\to256\to512$; Decoder MLP $100\to256\to512\to1024\to4096$ |

**Section III-B** (*Non-parametric Seismic Texture Synthesis Algorithm* and *Context-based Seismic Image Synthesis*) — texture synthesis parameters:

| Parameter requested | Value added to manuscript |
|---|---|
| Patch size / neighborhood | $11 \times 11$ pixels (Item 1 — Neighborhood) |
| Sampling parameter $\sigma$ | $\sigma = \text{kernel\_size}/6.4 \approx 1.72$ (Item 3 — Random Sampling) |
| Boundary dilation width | $5 \times 5$ kernel, 1 iteration → boundary strip of 5 pixels total width |
| Texture database construction | Up to 1,000 image/mask pairs (TGS, $101\times101$ px); patches extracted via Probabilistic Hough Transform (`cv2.HoughLinesP`, threshold = 15, minimum points = 15, maximum gap = 15 px); segments filtered by area $> 100$ px; indexed by line angle; cached to `patches_db_cache.npz` |

**Revised passages:**
*Section III-B, Item 1 (Neighborhood):*
> *"In our implementation, the neighborhood window is $11 \times 11$ pixels, following the default configuration of the non-parametric synthesis algorithm of Efros and Leung [Efros1999]."*
*Section III-B, Item 3 (Random Sampling):*
> *"In our implementation, $\sigma$ is computed dynamically as $\sigma = \text{kernel\_size} / 6.4 \approx 1.72$, following the reference implementation of Efros and Leung [Efros1999]."*
*Section III-B, Context-based paragraph:*
> *"...make it thicker, creating an edge strip using a $5 \times 5$ dilation kernel applied once (one iteration), which expands the Canny edge map by 2 pixels on each side, yielding a boundary strip of 5 pixels total width. [...] The texture patch database is constructed from up to 1,000 image/mask pairs drawn from the TGS Salt Identification Challenge dataset ($101 \times 101$ pixels each). Boundary patches are extracted by detecting line segments via Probabilistic Hough Transform (`cv2.HoughLinesP`, threshold = 15, minimum points = 15, maximum gap = 15 pixels), retaining only segments whose bounding region exceeds 100 pixels in area; patches are indexed by the detected line angle to enable angle-guided selection during synthesis. The database is cached to disk (`patches_db_cache.npz`) to avoid recomputation."*

**Note on cross-reference with Reviewer 1 (R1.2):** The VAE implementation details above were also requested by Reviewer 1, Comment 2. Both responses refer to the same manuscript changes in Section III-A.

---

*[Additional responses to Reviewer 1 — Comments R1.4 — to be added]*

---

---

