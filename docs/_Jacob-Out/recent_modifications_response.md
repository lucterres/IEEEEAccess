# Síntese das respostas às questões 2 e 3 

**Manuscript:** Context-oriented Synthesis of Salt Domes in Labeled Seismic Images

## Question 2 -- Relationship Between Origin Recognition and Expert Segmentation

### 1. Question

Does expert segmentation quality differ between real and synthetic images depending on whether the expert correctly recognizes the image origin?

### 2. Response

Não houve diferença estatisticamente significativa na qualidade da segmentação entre imagens reais e sintéticas, independentemente do reconhecimento correto da origem.

The existing blind-evaluation data were grouped by image source and classification outcome. The pooled F1-score results were:

| Source | Outcome | n | Mean F1 | Std. F1 |
|---|---|---:|---:|---:|
| Real | Correct | 85 | 0.849 | 0.059 |
| Real | Incorrect | 50 | 0.848 | 0.074 |
| Synthetic | Correct | 87 | 0.843 | 0.065 |
| Synthetic | Incorrect | 48 | 0.836 | 0.071 |

The real/synthetic difference was 0.001 F1 for correctly classified images and 0.012 for incorrectly classified images. A Mann--Whitney U test did not detect a statistically significant difference between the real and synthetic F1 distributions (`U = 9632`, `p = 0.419`).

These results indicate comparable expert segmentation performance, without a clear dependence on whether the image origin was recognized. They do not establish formal statistical equivalence.

### 3. Actions Taken in Manuscript `_v7.tex`
- Added `tab:blind_seg_breakdown` in Section IV-C.
- Reported F1/Dice by image source and classification outcome.
- Added the Mann--Whitney U result and its cautious interpretation.

## Question 3 -- Improvement in Automated Segmentation

### 1. Question

Does adding synthetic image--mask pairs improve automated salt-body segmentation on real seismic images?

### 2. Response

Sim. A adição de pares imagem--máscara sintéticos melhorou o IoU observado na segmentação automatizada de imagens sísmicas reais.

A controlled downstream U-Net experiment compared training with 1,200 real images against training with 1,200 real plus 1,200 synthetic images. Both scenarios used the same fixed real test set and were repeated with seeds 42, 123, and 456.

| Training scenario | IoU (mean +/- std.) |
|---|---:|
| Real only | 0.4081 +/- 0.0092 |
| Real + Synthetic | 0.4276 +/- 0.0062 |

The observed gain was `+0.0195` IoU, or `+4.8%`, and was positive for all three seeds: `+0.0292`, `+0.0168`, and `+0.0125`. The result is limited to the evaluated protocol and is not presented as a definitive claim of statistical significance or universal generalization.

### 3. Actions Taken in Manuscript `_v7.tex`

- Added Section IV-E, `Downstream Segmentation Evaluation`.
- Added the Scenario A versus Scenario B comparison table.
- Added the ranking of seven augmentation strategies.
- Reported the observed IoU gain and limited the interpretation to the evaluated protocol.

## Additional Updates in Manuscript `_v7.tex`

- Updated the abstract to summarize the blind discrimination result, comparable expert F1-scores, and the observed U-Net IoU improvement.
- Updated the conclusions to present the same findings with cautious wording: the synthetic images challenge expert discrimination, support comparable salt-body interpretation, and improve U-Net segmentation under the evaluated protocol.

## Overall Interpretation

The two analyses provide complementary evidence: expert segmentation performance was comparable for real and synthetic images, and adding synthetic image--mask pairs improved the observed U-Net IoU on real seismic images.
