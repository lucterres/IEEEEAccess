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

**Action taken in the revised manuscript :**

The paragraph beginning *"We use the generated masks as contexts..."* in **Section III-A** (*Context Generation Using a Variational Autoencoder*) was replaced with a detailed implementation description covering:

1. **Input:** binary salt-body masks; original $101 \times 101$ masks resized to $64 \times 64$, yielding input dimension $1 \times 64 \times 64$
2. **Encoder architecture:** three `Conv2d` layers with channel progression $1 \to 128 \to 256 \to 512$ (kernel 3, stride 2, padding 1), producing a $512 \times 8 \times 8$ feature map, followed by flattening and two independent linear layers for $\mu$ and $\log\sigma^2$
3. **Latent dimension:** $d = 100$
4. **Reparameterization:** $z = \mu + \sigma \odot \epsilon$, where $\sigma = \exp(\frac{1}{2}\log\sigma^2)$ and $\epsilon \sim \mathcal{N}(0, I)$
5. **Decoder architecture:** MLP $100 \to 256 \to 512 \to 1024 \to 4096$, reshaped to $1 \times 64 \times 64$ + sigmoid
6. **Loss function:** $\mathcal{L} = \mathcal{L}_{\mathrm{BCE}} + \lambda\mathcal{L}_{\mathrm{KL}}$, where $\lambda = N/B$ ($N$ = number of training samples, $B$ = batch size)
7. **Training hyperparameters:** 20 epochs, batch size 32, Adam optimizer (default learning rate), gradient clipping with maximum norm 1.0
8. **Justification for convolutional encoder:** preserves local spatial structure of masks (salt-body contours and region patterns), provides an image-appropriate inductive bias

**Revised text (Section III-A, `_v7.tex`):**

> *"We use the generated masks as contexts for the texture synthesis process. Once the boundary of a salt body is identified, its interior is assumed to correspond to the salt region. The VAE operates on binary salt-body masks. The original $101 \times 101$ masks are resized to $64 \times 64$ before being used as inputs, yielding an input dimension of $1 \times 64 \times 64$. The encoder consists of three* `Conv2d` *layers with channel progression $1 \rightarrow 128 \rightarrow 256 \rightarrow 512$, kernel size 3, stride 2, and padding 1. The resulting $512 \times 8 \times 8$ feature map is flattened and passed to two independent linear layers that estimate the latent mean $\mu$ and log-variance $\log\sigma^2$, both with dimensionality $d=100$. Latent codes are sampled using $z=\mu+\sigma\odot\epsilon$, where $\sigma=\exp(\frac{1}{2}\log\sigma^2)$ and $\epsilon\sim\mathcal{N}(0,\mathrm{I})$. The decoder is an MLP with layer dimensions $100\rightarrow256\rightarrow512\rightarrow1024\rightarrow4096$. Its 4096-dimensional output is reshaped into a $1\times64\times64$ mask and passed through a sigmoid activation. The model is trained using the objective $\mathcal{L}=\mathcal{L}_{\mathrm{BCE}}+\lambda\mathcal{L}_{\mathrm{KL}}$, where $\mathcal{L}_{\mathrm{BCE}}$ is the binary cross-entropy reconstruction loss, $\mathcal{L}_{\mathrm{KL}}$ is the Kullback–Leibler divergence from the approximate posterior to $\mathcal{N}(0,\mathrm{I})$, and $\lambda=N/B$, with $N$ denoting the number of training samples and $B$ the batch size. Training used 20 epochs, batch size 32, the Adam optimizer with its default learning rate, and gradient clipping with maximum norm 1.0. The convolutional encoder was selected to preserve local spatial structure and capture salt-body contours while providing an image-appropriate inductive bias."*

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

- **Abstract** *(lines 58–60 in `_v7.tex`)*: Updated with the blind discrimination experiment results: discrimination accuracy (63.7%), statistical significance ($p = 0.000004$), and segmentation F1-scores (real 0.849 ± 0.065 vs. synthetic 0.840 ± 0.067).
- **Section IV, Criterion 1** *(lines 352–365 in `_v7.tex`)*: The opening paragraph of the Results section was updated. The claim "highly realistic" was moderated to *"sufficiently realistic to challenge expert discrimination"*; the dual evaluation strategy now explicitly cites Ferreira et al.~\cite{Ferreira2020}; the LBP metric description was clarified to *"Euclidean distance between Local Binary Pattern (LBP) histograms"*.
- **Section IV-C, protocol description** *(lines 459–467)*: Full experimental design described: 45 real + 45 synthetic + 10 control = 100 images per evaluator, randomized interleaved sequence, experts blinded.
- **Section IV-C — Qualitative Evaluation** *(lines 455–514 in `_v7.tex`)*: Subsection restructured as a formal blind discrimination experiment. Subsubsection *Blind Discrimination Experiment Protocol* added (lines 459–467). Subsubsection *Blind Discrimination Results* added with two tables (`tab:blind_classification`, `tab:blind_segmentation`) and analysis paragraph including binomial test ($k=172$, $n=270$, $p=0.000004$) (lines 468–514).
- **Section VI — Concluding Remarks** *(lines 712–718 in `_v7.tex`)*: Paragraph updated with the blind experiment outcome (63.7% accuracy, F1 real 0.849 ± 0.065 vs. synthetic 0.840 ± 0.067) and the moderated hypothesis (*"geologically plausible, visually realistic, and comparable to real seismic images for salt-body interpretation"*).

### Comment R1.4 — Statistical Significance for DSSIM

> *"The improvement in DSSIM is small (~2.2%). Please add a statistical test (e.g., Wilcoxon) to confirm significance, or otherwise discuss the result candidly while highlighting gains in MSE and LBP."*

**Response:**

We thank the reviewer for this precise and constructive observation. We agree that the original manuscript did not adequately address the practical meaning of the DSSIM result, and we have revised the relevant paragraph accordingly.

**Clarification on the reported DSSIM difference:**
The reviewer refers to a ~2.2% difference; for completeness, we note that the exact values in Table `tab:metricsSummary` are: Ferreira et al. median DSSIM = 0.3978, proposed method median DSSIM = 0.3891, corresponding to an absolute reduction of ~0.0087 (~2.2% relative). We discuss this result transparently below.

**Why a Wilcoxon test between the two methods is not feasible:**
A paired Wilcoxon signed-rank test — the appropriate non-parametric procedure for comparing two paired sample distributions — requires the sample-level DSSIM values from both methods on the same or matched inputs. The results reported by Ferreira et al.~[Ferreira2020] were published exclusively as aggregated statistics (minimum, median, and maximum over the F3 dataset); the individual sample-level DSSIM values were not publicly released. This precludes any formal inter-method significance test for DSSIM.

**Transparent discussion of the DSSIM result:**
We acknowledge that the DSSIM improvement is modest in magnitude compared to the gains in MSE and LBP Distance. The DSSIM result indicates that **both methods operate in a similar structural-similarity regime**, with a modest advantage for the proposed approach — a finding that reinforces the argument that the high-level structural layout of the synthesized seismic images is preserved by both approaches, while the more pronounced differentiators are captured by MSE and LBP Distance. The direction of the DSSIM difference is nevertheless consistent with the gains observed in the other two measures.

The gains across all three measures are summarized below:

| Metric | Ferreira et al. (median) | Proposed (median) | Relative improvement |
|--------|--------------------------|-------------------|----------------------|
| MSE | 4712.1 | 3926.2 | **−16.7%** |
| DSSIM | 0.3978 | 0.3891 | −2.2% |
| LBP Distance | 0.1714 | 0.1500 | **−12.5%** |

The MSE reduction of ~16.7% reflects substantially improved pixel-level fidelity, and the LBP Distance reduction of ~12.5% indicates that the proposed method generates textures with meaningfully higher similarity to the original seismic images in the local binary pattern feature space. These two metrics together provide a consistent and practically relevant signal of improvement, with DSSIM confirming that the structural regime is preserved.

**Action taken in the revised manuscript :**

The MSE, DSSIM, and LBP Distance paragraphs of **Section IV-D** (*Comparative Analysis*) and the "Overall" synthesis paragraph were reconciled with Table `tab:metricsSummary` and rewritten to:

1. Report all values using the precision of Table `tab:metricsSummary` (Ferreira DSSIM 0.3978 instead of 0.39; proposed values as 3926.2, 0.3891, 0.1500), removing spurious decimal precision;
2. Quantify the DSSIM difference correctly as ~0.0087 (~2.2%), replacing the previous incorrect ~0.2% figure that stemmed from comparing the rounded Ferreira value (0.39) with the higher-precision proposed value;
3. Explain that a paired Wilcoxon test between the two methods is not feasible because the sample-level DSSIM values of Ferreira et al. were not publicly released;
4. Reframe the DSSIM result as a modest advantage in a similar structural-similarity regime, confirming that structural layout is preserved by the synthesis strategy;
5. Explicitly quantify and highlight the more pronounced improvements in MSE (−16.7%) and LBP Distance (−12.5%), and note that the DSSIM difference direction is consistent with these gains.

**Revised paragraph (Section IV-D, `_v7.tex`, lines 534–538):**

> *"Ferreira et al.~[Ferreira2020] reported a median DSSIM of 0.3978 using its best-performing configuration. Our proposed context-oriented approach achieved a median DSSIM of 0.3891, corresponding to an absolute reduction of approximately 0.0087 (≈ 2.2%). A paired Wilcoxon signed-rank test between the two methods would be the appropriate statistical procedure to assess significance; however, the sample-level DSSIM values of Ferreira et al.~[Ferreira2020] were not publicly released, so only their aggregated statistics (minimum, median, and maximum) are available for comparison. This precludes any formal inter-method significance test for DSSIM. The DSSIM result indicates that both methods operate in a similar structural-similarity regime, with a modest advantage for the proposed approach --- a finding that supports the argument that the structural layout of the synthesized images is preserved regardless of the synthesis strategy, while the more pronounced differentiators are captured by MSE and LBP Distance."*

**Revised "Overall" paragraph (Section IV-D, `_v7.tex`, line 538):**

> *"[...] The improvement is most pronounced in MSE (≈ 16.7% reduction: from 4712.1 to 3926.2) and LBP Distance (≈ 12.5% reduction: from 0.1714 to 0.1500), which together suggest meaningful gains in pixel-level accuracy and textural fidelity. The DSSIM improvement is more modest (≈ 2.2% reduction: from 0.3978 to 0.3891); we do not claim statistical significance for it because the sample-level DSSIM values of Ferreira et al.~[Ferreira2020] were not publicly released, but the direction of the difference is consistent with the gains observed in the other two measures."*

---

## Response to Reviewer 2
### Comment R2.1 — Downstream Segmentation Experiment

> *"The practical value of the proposed synthetic data generation method should be demonstrated more directly. Please include a downstream segmentation experiment showing whether augmenting the training set with the proposed synthetic samples improves segmentation performance on real seismic images."*

**Response:**

We thank the reviewer for this important suggestion. We agree that a downstream task evaluation provides a more direct and practically meaningful validation of the proposed synthesis framework. In response, we added a new subsection entitled **"Downstream Segmentation Evaluation"** to the revised manuscript, reporting a controlled U-Net segmentation experiment on the TGS Salt Identification Challenge dataset.

The purpose of this experiment is to test whether synthetic samples generated by the proposed context-oriented method improve segmentation performance on a fixed real test set when used for data augmentation during training.

**Action taken in the revised manuscript :**

A new subsection **Section IV-E — Downstream Segmentation Evaluation** was inserted and completed with the experimental protocol, numerical results, and interpretation.

The experiment compares two training scenarios under the same U-Net architecture and optimization settings:

1. **Scenario A — Real only:** training with 1,200 real images;
2. **Scenario B — Real + Synthetic:** training with 1,200 real images plus 1,200 synthetic images generated by the proposed method.

Both scenarios were repeated with three random seeds (42, 123, 456), and performance was evaluated on the same fixed real test set using **IoU** as the primary metric.

**Main result:**
- **Scenario A:** IoU = **0.4081 ± 0.0092**
- **Scenario B (context seismic):** IoU = **0.4276 ± 0.0062**
- **Absolute gain:** **+0.0195 IoU**
- **Relative gain:** **+4.8%**

Importantly, the gain was consistent across all three seeds:
- seed 42: **+0.0292**
- seed 123: **+0.0168**
- seed 456: **+0.0125**

These results indicate that the proposed synthetic samples improve downstream segmentation on real seismic data and reduce variance across runs.

In addition, we included a second table ranking the augmentation methods tested in **Scenario B**, showing that the proposed **context seismic** strategy achieved the highest mean IoU among all evaluated augmentations:

| Rank | Augmentation method | Mean IoU | Std IoU |
|------|---------------------|----------|---------|
| 1 | **context seismic** | **0.4276** | 0.0062 |
| 2 | elastic transform | 0.4272 | 0.0036 |
| 3 | random brightness/contrast | 0.4271 | 0.0068 |
| 4 | grid distortion | 0.4270 | 0.0163 |
| 5 | random gamma | 0.4193 | 0.0050 |
| 6 | optical distortion | 0.4166 | 0.0122 |
| 7 | clahe | 0.4147 | 0.0056 |

This ranking allowed us to make two additional points explicit in the manuscript:
1. the proposed method achieved the **best mean downstream result** among all tested augmentations; and
2. this empirical outcome supports the **central hypothesis of the paper**, namely, that synthetic seismic images generated by combining VAE-based mask generation with context-oriented texture synthesis are sufficiently realistic and informative to improve the training of segmentation models on real seismic data.

**Changes made to the manuscript:**

- **Section I — Introduction** *(paper overview sentence)*: updated to mention the new downstream segmentation experiment in Section IV-E.
- **Section IV-E — Downstream Segmentation Evaluation**: completed with:
  - corrected experimental setup using the actual experiment values (**1,200 real / 1,200 synthetic**),
  - results table comparing **Scenario A vs. Scenario B**,
  - interpretation paragraph discussing the consistent gain across seeds and lower variance,
  - new table ranking the **seven augmentation methods** evaluated in Scenario B,
  - explicit statement that the best result obtained by **context seismic** supports the paper's central hypothesis.

**Revised text added in Section IV-F:**

> *"Scenario B consistently outperforms Scenario A across all three random seeds (seeds 42, 123, and 456), with individual IoU gains of +0.0292, +0.0168, and +0.0125, respectively. The mean IoU improves from 0.4081 (Scenario A) to 0.4276 (Scenario B), an absolute gain of +0.0195 (+4.8%). The lower standard deviation of Scenario B (0.0062 vs. 0.0092) further indicates that augmenting with context-seismic synthetic images not only improves segmentation performance but also stabilizes training across different initialization seeds."*

> *"Table~\ref{tab:downstream_augments} shows that the proposed context seismic augmentation achieved the highest mean IoU among all Scenario B strategies. (...) Most importantly, the fact that the best downstream segmentation performance is achieved when the additional training data are generated by the proposed context seismic synthesis scheme provides empirical support for the central hypothesis of this paper: synthetic seismic images produced by combining VAE-based mask generation with context-oriented texture synthesis are not only visually plausible, but also sufficiently realistic and informative to improve the training of segmentation models on real seismic data."*

---
### Comment R2.2 — Blind Discrimination Experiment

> *"The claim that synthetic images are 'virtually indistinguishable' from real images should be moderated or supported by a proper blind discrimination experiment. The current expert evaluation measures how experts identify salt regions, but it does not directly test whether experts can distinguish real images from generated ones."*

**Response:**

This comment is addressed jointly with **Comment R1.3** (Reviewer 1 — Expert Evaluation Design), which raised the same methodological concern. Please refer to the full response under [Comment R1.3](#comment-r13--expert-evaluation-design) above for the complete description of the redesigned blind discrimination experiment and its results.

In summary: a formal blind discrimination experiment was conducted with three expert geoscientists (45 real + 45 synthetic + 10 control images; 270 classification decisions total). Overall discrimination accuracy was 63.7% ($p < 0.001$ vs. chance). Segmentation F1-scores were comparable: real 0.849 ± 0.065 vs. synthetic 0.840 ± 0.067. The original claim of "virtually indistinguishable" was moderated to **"geologically plausible, visually convincing synthetic seismic images that are comparable to real ones for salt-body interpretation"**. All manuscript changes are described in the R1.3 response.

---
### Comment R2.3 — Expanded Baseline Comparison

> *"The comparison with existing methods should be expanded. The manuscript mainly compares with Ferreira et al., but stronger or more recent generative baselines, such as GAN-based, conditional GAN-based, diffusion-based, or conditional diffusion-based seismic image synthesis methods, should be considered."*

**Response:**

We thank the reviewer for this important suggestion. We agree that the comparison section of the original manuscript was narrow, relying exclusively on Ferreira et al.~[Ferreira2020] as the baseline. We have expanded the related work and comparison sections to address this concern, while being transparent about the constraints that limit direct numerical comparison with other methods.

**Why a direct numerical comparison with GAN/diffusion baselines is not feasible:**
We thoroughly reviewed the available methods in GAN-based and diffusion-based seismic image synthesis, specifically:

| Method | Model | Evaluation | Dataset |
|--------|-------|-----------|---------|
| Henriques et al.~[Henriques2021] | VAE + Conditional Normalizing Flow | Downstream segmentation (IoU/F1) on proprietary synthetic dataset | Not public |
| Choi et al.~[Choi2025] | Conditional pix2pix GAN / Conditional diffusion | Downstream fault detection (F1, IoU) | Private |
| Wang et al.~[Wang2021] | GAN | Waveform-level metrics | Seismic waveforms (incompatible) |
| **Ferreira et al.~[Ferreira2020]** | cGAN (pix2pix) | **MSE, DSSIM, LBP Distance on F3 dataset** | **F3 (public)** |

None of the GAN-based or diffusion-based methods in the salt dome synthesis literature report MSE, DSSIM, or LBP Distance on the public F3 benchmark. Their evaluations use either downstream segmentation metrics (IoU, F1-score for fault detection or salt segmentation) on private or non-public datasets, or waveform-level measures incompatible with image-level similarity evaluation. **Ferreira et al.~[Ferreira2020] remains the only baseline for which a direct, fair numerical comparison on a common public benchmark using the same metrics is possible.**

This is a known limitation acknowledged candidly in the revised manuscript, and it reflects the broader challenge of the absence of a universally adopted benchmark for seismic image synthesis.

**Actions taken in the revised manuscript :**

1. **Section II (Related Work):**
   - The paragraph on **Ferreira et al.** was expanded to explicitly describe their cGAN/pix2pix architecture (conditional generator + discriminator, sketch-based conditioning), contextualizing them as the closest directly comparable baseline (same task, same dataset, same metrics).
   - The paragraph on **Choi et al.** was expanded to cover both their conditional pix2pix GAN and conditional diffusion model variants, noting that their evaluation targets fault detection on a private dataset.
   - A new **synthesis paragraph** was added at the end of Section II that explicitly organizes the four methods (Ferreira, Henriques, Choi, Wang) into a comparative landscape, contrasting them along architectural choices, data requirements, and evaluation methodology, and explaining why only Ferreira et al. enables direct numerical comparison.

2. **Section IV (Results), new subsubsection — *Contextual Comparison with GAN-based and Diffusion-based Methods*:**
   A new subsubsection was added after the Comparative Analysis, providing:
   - A structured discussion of Henriques et al.~[Henriques2021] (VAE + CNF): architecturally the closest alternative, but evaluated only indirectly on downstream segmentation using a non-public dataset; the proposed method's training-free texture stage is explicitly contrasted with the CNF's requirement for 24,872 annotated training pairs.
   - A discussion of Choi et al.~[Choi2025] (pix2pix GAN and conditional diffusion): evaluated on fault detection with private datasets and downstream metrics; the proposed method's single-pass generation and training-free texture synthesis are contrasted with the hundreds of denoising steps and large training datasets required by diffusion models.
   - A discussion of Wang et al.~[Wang2021] (SeismoGen GAN): operates on waveform-level evaluation, incompatible with image-level structural metrics.
   - A new **Table~\ref{tab:comparison_overview}** summarizing the key characteristics of all five methods (model type, target task, dataset, and whether direct numerical comparison is possible).

**New Table (Table~\ref{tab:comparison_overview} in revised `_v7.tex`):**

| Method | Generative model | Target task | Direct comparison |
|--------|-----------------|-------------|-------------------|
| Ferreira et al. | cGAN (pix2pix) | Salt domes, faults | **Yes** (F3, same metrics) |
| Henriques et al. | VAE + CNF | Salt domes | No (different dataset & metrics) |
| Choi et al. | Cond. pix2pix GAN / Diffusion | Fault detection | No (private dataset, downstream metrics) |
| Wang et al. | GAN | Waveforms | No (waveform-level evaluation) |
| **Proposed** | VAE + Non-param. texture | Salt domes | — |

**Also added:** the pix2pix reference (Isola et al., CVPR 2017) was added to the bibliography, since both Ferreira et al. and Choi et al. build on this framework and it was not previously cited.

---
### Comment R2.4 — Clearer Experimental Setting

> *"The experimental setting needs clearer explanation. In particular, the quantitative results in Table 3 and the ablation study appear to use different numerical ranges and possibly different datasets or protocols. The authors should clarify the datasets, sample sizes, preprocessing, normalization, and evaluation procedures used in each experiment."*

**Response:**

We thank the reviewer for this important observation. The reviewer correctly identified that the quantitative results in Table~3 and those in the ablation study operate at different numerical scales. This discrepancy arises because the two experimental contexts use **different datasets and image dimensions**, which was not sufficiently explained in the original manuscript. We have now added explicit clarifications in two places.

**Root cause of the numerical range discrepancy:**
| Experiment | Dataset | Image size | Sample size | Typical MSE range |
|---|---|---|---|---|
| Table 3 — Quantitative comparison | F3 (Dutch North Sea) | $400 \times 400$ px | 600 synthetic images | ~3,700–6,700 |
| Ablation (texture synthesis) | TGS Salt Challenge | $101 \times 101$ px | 110 synthetic images (66 valid) | ~542–837 |
| Ablation (mask generation) | TGS Salt Challenge | $101 \times 101$ px | 200 masks + 1,617 GT masks | N/A (shape metrics) |

MSE is defined as the mean of squared pixel differences over all pixels of an image. With $400^2 = 160{,}000$ pixels (F3) vs.\ $101^2 = 10{,}201$ pixels (TGS), the image area differs by a factor of approximately 15.7×, which directly explains the order-of-magnitude difference in absolute MSE values. DSSIM and LBP Distance are less sensitive to image size but are also affected by the distinct image content characteristics of the two datasets.

**Action taken in the revised manuscript :**

1. **Section IV — Dataset subsection** *(after the F3 paragraph)*: A new explanatory note was added that explicitly states:
   - The quantitative comparison (Table 3) uses the **F3 dataset**, $400 \times 400$ px patches, normalized to $[0, 255]$, 600 synthetic images.
   - The ablation study uses the **TGS dataset**, $101 \times 101$ px images, 8-bit grayscale, 110 images (texture ablation) or 200 masks (VAE ablation).
   - The difference in image area accounts for the order-of-magnitude difference in absolute MSE values.
   - The two experimental contexts are **not directly numerically comparable** and should be interpreted independently.

2. **Section V — Ablation Study** *(opening paragraph)*: A new "Experimental setting" note was prepended, reminding readers that all ablation experiments use the TGS dataset ($101 \times 101$ px) and cross-referencing the explanatory note in the Dataset section.

**Revised note added to Dataset section :**

> *"The two experimental contexts in this work — the quantitative comparison with the state-of-the-art (Section IV) and the ablation study (Section V) — use different datasets, image dimensions, and sample sizes, and are therefore not directly numerically comparable. The quantitative comparison with Ferreira et al. is conducted on the F3 dataset using $400 \times 400$ pixel images ($N = 600$ synthetic images), producing MSE values in the range of approximately 3,700–6,700. The ablation study is conducted on the TGS dataset using $101 \times 101$ pixel images ($N = 110$ images for the texture ablation; $N = 200$ masks for the VAE ablation), producing MSE values in the range of approximately 500–850. The substantially smaller image area ($101^2 = 10{,}201$ pixels vs.\ $400^2 = 160{,}000$ pixels) accounts for the order-of-magnitude difference in absolute MSE values between the two experimental contexts, since MSE is computed as the mean of squared pixel differences over all pixels of each image pair."*

---
### Comment R2.5 — Reproducibility

> *"The paper should improve reproducibility. Important implementation details are missing, including VAE latent dimension, training epochs, optimizer, learning rate, loss settings, patch size, boundary dilation width, texture database construction, and sampling parameters. These details are essential for readers who wish to reproduce or extend the work."*

**Response:**

We thank the reviewer for this detailed and constructive list of missing implementation details. We have addressed every item enumerated in the comment, distributing the information across two sections of the revised manuscript: VAE-related parameters in Section III-A, and texture synthesis parameters in Section III-B.

**Action taken in the revised manuscript :**

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
## Additional Editorial and Formatting Corrections

In addition to the reviewer-specific revisions, we performed the following consistency and editorial checks across the revised manuscript:

1. **IEEE citation style:** Narrative constructions such as “Ferreira et al.~\cite{Ferreira2020}” were replaced with IEEE-compatible numerical citations, such as “the method in~\cite{Ferreira2020}”. Citations were positioned before punctuation, and multiple references were written individually rather than as compressed ranges.
2. **Grammar and academic style:** The revised passages in the related-work, experimental-setting, quantitative-comparison, and concluding sections were edited for grammatical correctness, clarity, and consistent scientific terminology.
3. **Figure and table citations:** All figure and table labels in `_v7.tex` were checked against their in-text references. No defined figure or table remains uncited, and no orphan figure or table reference was found.
4. **Bibliographic consistency:** All 21 `\bibitem` entries in `_v7.tex` were checked against the citation commands. Every bibliography entry is cited at least once, and no citation points to a missing bibliography entry.


