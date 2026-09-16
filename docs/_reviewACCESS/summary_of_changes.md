# Summary of Changes in the Revised Manuscript (`_v7`)

**Manuscript ID:** Access-2026-27912  
**Article Title:** Context-oriented Synthesis of Salt Domes in Labeled Seismic Images  
**Authors:** Luciano D. Terres and Jacob Scharcanski  
**Revision:** July 2026

### Reviewers Summary

**Reviewer 1** (`## 🔵 Reviewer 1` in `_Reviewer.md`) — 4 major points:

- R1.1 Comparison with Henriques et al. — **DONE** (Section II rewritten)
- R1.2 VAE implementation details — **DONE** (Section III, arch + hyperparams added)
- R1.3 Expert evaluation design (blinding) — **DONE** (blind experiment completed: 45 real + 45 synthetic + 10 control images, 3 experts; accuracy 63.7%, $p<0.001$; segmentation F1 real=0.849 vs. synthetic=0.840; hypothesis moderated from "virtually indistinguishable" to "geologically plausible and comparable for salt-body interpretation"; two result tables and analysis paragraph added in Sec. IV-C)
- R1.4 Statistical significance for DSSIM (~2.2%) — **DONE** (Comparative Analysis paragraphs reconciled with Table `tab:metricsSummary`: Ferreira DSSIM 0.3978, proposed 0.3891 → Δ 0.0087 (~2.2%); Wilcoxon infeasibility explained; MSE −16.7% and LBP −12.5% highlighted)

**Reviewer 2** (`## 🟠 Reviewer 2` in `_Reviewer.md`) — 5 points:

- R2.1 Downstream segmentation experiment — **DONE** (Experimental Setup corrected to n_real=1200/n_synth=1200; Table~\ref{tab:downstream} filled with real IoU results; analysis paragraph written — IoU-only, no Wilcoxon; Scenario B: IoU 0.4276±0.0062, +4.8% vs. Scenario A: 0.4081±0.0092)
- R2.2 Blind discrimination experiment — **DONE** (same experiment as R1.3; protocol aligned with manuscript; results inserted in Sec. IV-C)
- R2.3 Expanded baseline comparison (GAN/diffusion) — **DONE** (contextual comparison added: Related Work expanded; new subsubsection + Table~\\ref{tab:comparison_overview} in Sec IV; pix2pix2017 bibitem added)
- R2.4 Clearer experimental setting — **DONE** (added explicit note in Dataset section explaining the two experimental contexts: F3 400×400px N=600 vs TGS 101×101px; added Experimental setting note in Ablation Study section; clarified why MSE ranges differ by ~16×)
- R2.5 Reproducibility — **DONE** (VAE details and texture synthesis details added)

>
> All changes listed below are highlighted in `latex_build/Highlighted_PDF.pdf`  

> (yellow = additions, strikethrough = deletions).  

> Full rationale for each change is in [`response_to_reviewers.md`](./response_to_reviewers.md).
>

---

The table below lists every change made to the manuscript in response to reviewer comments. Each item references the originating comment, the affected section, and the exact line numbers in `_v7.tex`.


| #  | Comment     | Section in manuscript                                | Change description                                                                                                                                                                                                                                                                                                                                                                    | Lines in `_v7.tex` |
|----|-------------|------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|
| 1  | R1.1        | **Sec. II — Related Work**                         | Paragraph on Henriques et al. substantially rewritten: explicit contrast with proposed method on architecture (CNF vs. non-parametric), data requirements (24,872 annotated pairs vs. training-free), zone decomposition, and evaluation strategy                                                                                                                                     | 94–103           |
| 2  | R1.2 / R2.5 | **Sec. III-A — Context Generation Using a VAE**    | New implementation paragraph added: input dimension $1\\times64\\times64$, convolutional encoder (`Conv2d` $1\\to128\\to256\\to512$), latent dim $d=100$, reparameterization trick, MLP decoder ($100\\to256\\to512\\to1024\\to4096$), VAE loss (BCE + KL weighted by $N/B$), 20 epochs, batch 32, Adam, gradient clipping at 1.0                                                     | 139                |
| 3  | R1.3 / R2.2 | **Sec. IV — Results, opening paragraph**           | Qualitative evaluation criterion rewritten: sequential evaluation replaced by formal blind discrimination experiment; dual-evaluation strategy introduced                                                                                                                                                                                                                             | 350–363          |
| 4  | R1.3 / R2.2 | **Sec. IV-C — Qualitative Evaluation**             | New subsubsection *Blind Discrimination Experiment Protocol* added: single randomized interleaved sequence, experts blinded, classification + segmentation tasks, control images, order randomization                                                                                                                                                                                 | 487–506          |
| 5  | R1.4        | **Sec. IV-D — Comparative Analysis**               | MSE, DSSIM, LBP paragraphs and "Overall" synthesis reconciled with Table `tab:metricsSummary`: Ferreira DSSIM corrected from 0.39 to 0.3978 (table value); proposed values rounded to 4 significant figures (MSE 3926.2, DSSIM 0.3891, LBP 0.1500); DSSIM Δ recomputed as 0.0087 (~2.2%) and reframed as "modest advantage" (removed "marginal"/"candidly"); LBP Δ corrected to 12.5%; MSE paragraph rewritten to remove hedge (`potentially`) and add explicit −16.7% reduction; Wilcoxon infeasibility retained | 532–540          |
| 6  | R2.3        | **Sec. II — Related Work**                         | Ferreira et al. and Choi et al. paragraphs expanded; new synthesis paragraph added at end of Sec. II organizing four methods (Ferreira, Henriques, Choi, Wang) into a comparative landscape explaining why only Ferreira et al. enables direct numerical comparison                                                                                                                   | 92–103           |
| 7  | R2.3        | **Sec. IV — new subsubsection**                    | New subsubsection *Contextual Comparison with GAN-based and Diffusion-based Methods* added: structured discussion of Henriques et al. (VAE+CNF), Choi et al. (pix2pix GAN / conditional diffusion), Wang et al. (SeismoGen GAN)                                                                                                                                                       | 530–587          |
| 8  | R2.3        | **Sec. IV — Table**                                | New **Table (comparison_overview)** added: five-method comparison table (model type, target task, dataset, direct comparison feasibility)                                                                                                                                                                                                                                             | 545–560          |
| 9  | R2.3        | **Bibliography**                                     | New bibitem for Isola et al. (pix2pix, CVPR 2017) added to `\thebibliography{}`                                                                                                                                                                                                                                                                                                       | —                |
| 10 | R2.4        | **Sec. IV — Dataset subsection**                   | New note *"Note on experimental settings and numerical ranges"* added: F3 ($400\\times400$px, $N=600$, MSE ≈ 3,700–6,700) vs. TGS ($101\\times101$px, $N=110$, MSE ≈ 500–850); explains $\\sim15.7\\times$ area ratio as root cause of MSE scale discrepancy                                                                                                                  | 373                |
| 11 | R2.4        | **Sec. V — Ablation Study**                        | New note *"Experimental setting"* prepended: all ablation experiments on TGS dataset ($101\\times101$px); cross-reference to Dataset note                                                                                                                                                                                                                                             | 593                |
| 12 | R2.5        | **Sec. III-B — Non-parametric Texture Synthesis**  | Patch neighborhood size ($11\\times11$ px), sampling parameter ($\\sigma = \\text{kernel\\_size}/6.4 \\approx 1.72$), boundary dilation ($5\\times5$ kernel, 1 iteration → 5 px strip), texture database construction (up to 1,000 pairs, Probabilistic Hough Transform, `patches_db_cache.npz`) added                                                                              | 256–305          |
| 13 | R2.1        | **Sec. IV-E — Downstream Segmentation Evaluation** | Experimental Setup updated to actual experiment values (n_real=1200, n_synth=1200, total 2400 in Scenario B). Table~\ref{tab:downstream} filled with real IoU results (Scenario A: $0.4081 \pm 0.0092$; Scenario B context seismic: $\mathbf{0.4276 \pm 0.0062}$; $\Delta{=}+0.0195$, $+4.8\%$). [TODO] analysis paragraph replaced by full IoU-based analysis (Dice removed; Wilcoxon not calculated). Evaluation metrics paragraph simplified to IoU only. | ~600–650          |
| 14 | R2.1        | **Sec. I — Introduction (paper overview)**         | Paper overview sentence updated: `Section~\ref{sec:results}` description now mentions downstream segmentation experiment and cross-references `Section~\ref{sec:downstream}`                                                                                                                                                                                                          | 80                 |
| 15 | R1.3 / R2.2 | **Operational support files (outside manuscript)** | Practical execution material prepared for the blind discrimination experiment in `docs/R2.2-experiment-blind/`: `experiment-protocol.md`, `blind_discrimination_experiment_template.csv`, `blind_discrimination_image_manifest.csv`, and `blind_discrimination_experiment_template_README.md`. These files align the experiment execution workflow with the protocol described in Sec. IV-C of `_v7.tex`. | — |



