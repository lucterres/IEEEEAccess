# Summary of Changes in the Revised Manuscript (`_v7`)

**Manuscript ID:** Access-2026-27912  
**Article Title:** Context-oriented Synthesis of Salt Domes in Labeled Seismic Images  
**Authors:** Luciano D. Terres and Jacob Scharcanski  
**Revision:** July 2026

> All changes listed below are highlighted in `latex_build/Highlighted_PDF.pdf`  
> (yellow = additions, strikethrough = deletions).  
> Full rationale for each change is in [`response_to_reviewers.md`](./response_to_reviewers.md).

---

The table below lists every change made to the manuscript in response to reviewer comments. Each item references the originating comment, the affected section, and the exact line numbers in `_v7.tex`.

| # | Comment | Section in manuscript | Change description | Lines in `_v7.tex` |
|---|---------|----------------------|-------------------|-------------------|
| 1 | R1.1 | **Sec. II — Related Work** | Paragraph on Henriques et al. substantially rewritten: explicit contrast with proposed method on architecture (CNF vs. non-parametric), data requirements (24,872 annotated pairs vs. training-free), zone decomposition, and evaluation strategy | 94–103 |
| 2 | R1.2 / R2.5 | **Sec. III-A — Context Generation Using a VAE** | New implementation paragraph added: input dimension $1\times64\times64$, convolutional encoder (`Conv2d` $1\to128\to256\to512$), latent dim $d=100$, reparameterization trick, MLP decoder ($100\to256\to512\to1024\to4096$), VAE loss (BCE + KL weighted by $N/B$), 20 epochs, batch 32, Adam, gradient clipping at 1.0 | 139 |
| 3 | R1.3 / R2.2 | **Sec. IV — Results, opening paragraph** | Qualitative evaluation criterion rewritten: sequential evaluation replaced by formal blind discrimination experiment; dual-evaluation strategy introduced | 350–363 |
| 4 | R1.3 / R2.2 | **Sec. IV-C — Qualitative Evaluation** | New subsubsection *Blind Discrimination Experiment Protocol* added: single randomized interleaved sequence, experts blinded, classification + segmentation tasks, control images, order randomization | 487–506 |
| 5 | R1.4 | **Sec. IV-D — Comparative Analysis** | DSSIM paragraph rewritten: marginal ~0.2% difference acknowledged candidly; Wilcoxon test explained as infeasible (sample-level data not public); MSE (−16.7%) and LBP Distance (−12.4%) improvements highlighted as practically meaningful | 524–529 |
| 6 | R2.3 | **Sec. II — Related Work** | Ferreira et al. and Choi et al. paragraphs expanded; new synthesis paragraph added at end of Sec. II organizing four methods (Ferreira, Henriques, Choi, Wang) into a comparative landscape explaining why only Ferreira et al. enables direct numerical comparison | 92–103 |
| 7 | R2.3 | **Sec. IV — new subsubsection** | New subsubsection *Contextual Comparison with GAN-based and Diffusion-based Methods* added: structured discussion of Henriques et al. (VAE+CNF), Choi et al. (pix2pix GAN / conditional diffusion), Wang et al. (SeismoGen GAN) | 530–587 |
| 8 | R2.3 | **Sec. IV — Table** | New **Table (comparison_overview)** added: five-method comparison table (model type, target task, dataset, direct comparison feasibility) | 545–560 |
| 9 | R2.3 | **Bibliography** | New bibitem for Isola et al. (pix2pix, CVPR 2017) added to `\thebibliography{}` | — |
| 10 | R2.4 | **Sec. IV — Dataset subsection** | New note *"Note on experimental settings and numerical ranges"* added: F3 ($400\times400$px, $N=600$, MSE ≈ 3,700–6,700) vs. TGS ($101\times101$px, $N=110$, MSE ≈ 500–850); explains $\sim15.7\times$ area ratio as root cause of MSE scale discrepancy | 373 |
| 11 | R2.4 | **Sec. V — Ablation Study** | New note *"Experimental setting"* prepended: all ablation experiments on TGS dataset ($101\times101$px); cross-reference to Dataset note | 593 |
| 12 | R2.5 | **Sec. III-B — Non-parametric Texture Synthesis** | Patch neighborhood size ($11\times11$ px), sampling parameter ($\sigma = \text{kernel\_size}/6.4 \approx 1.72$), boundary dilation ($5\times5$ kernel, 1 iteration → 5 px strip), texture database construction (up to 1,000 pairs, Probabilistic Hough Transform, `patches_db_cache.npz`) added | 256–305 |
