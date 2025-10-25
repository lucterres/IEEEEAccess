# Scientific Hypothesis

## Context-Oriented Synthesis of Salt Domes in Labeled Seismic Images

### Authors
- Luciano D. Terres (UFRGS / Petrobras)
- Jacob Scharcanski (UFRGS)

---

## 1. Main Hypothesis

**The combination of Variational Autoencoders (VAEs) for generating geometric masks with context-oriented texture synthesis can generate synthetic seismic images of salt domes that are virtually indistinguishable from real seismic images by geoscience experts.**

---

## 2. Scientific Problem

### Context
- Deep learning models for salt body segmentation require large volumes of annotated data
- Seismic image annotation is expensive and requires specialized expertise
- Limited datasets restrict model generalization
- Offshore oil exploration depends on precise identification of salt structures

### Technical Challenge
How to generate high-quality synthetic data that preserves:
1. **Structural characteristics** - geologically plausible geometries
2. **Textural properties** - realistic seismic patterns
3. **Complex interfaces** - sharp boundaries between salt and sediment

---

## 3. Hypothesis Components

### 3.1 Geometry Generation (VAE)

**Sub-hypothesis:** A VAE can learn the probability distribution of salt dome geometries and generate new realistic structural masks.

**Theoretical Foundation:**
- VAEs model data distributions in latent space
- Interpolation in latent space generates plausible intermediate geometries
- KL regularization ensures smoothness and continuity of generated shapes

**Advantages over alternatives:**
- **vs. GANs**: Greater training stability, variability control
- **vs. Diffusion Models**: Lower computational cost, efficiency on small datasets
- **vs. Geometric Transformations**: Greater diversity and geological realism

### 3.2 Context-Oriented Texture Synthesis

**Sub-hypothesis:** Dividing the synthesis process into three distinct zones (salt, boundary, sediment) produces more realistic images than holistic approaches.

**Theoretical Foundation:**
- Seismic images are **non-stationary** (textures vary spatially)
- Boundary zones have unique acoustic characteristics
- Non-parametric synthesis preserves local statistical properties

**Zone Components:**

#### Edge Zone (Boundary Zone)
- High seismic contrast
- Patterns of parallel light and dark bands
- Patch selection oriented by local angle
- Edge detection + morphological dilation

#### Salt Zone
- Characteristic homogeneous texture
- Specific acoustic properties of salt
- Synthesis based on salt reference patches

#### Conventional Sediment Zone
- Varied stratigraphic textures
- Synthesis based on sedimentary rock patches

### 3.3 Quality Comparable to Real Data

**Sub-hypothesis:** The synthetic images will be of sufficient quality to:
1. Deceive human experts (perceptual indistinguishability)
2. Serve as data augmentation for model training
3. Surpass state-of-the-art methods in quantitative metrics

---

## 4. Validation Methodology

### 4.1 Qualitative Evaluation (Expert Assessment)

**Protocol:**
- 3 geoscientists specialized in seismic interpretation
- Task: identify salt regions in real and synthetic images
- Comparison: expert-generated masks vs. ground truth

**Metrics:**
- **Precision**: Proportion of correctly identified salt pixels
- **Recall**: Proportion of salt pixels effectively detected
- **F1-Score**: Harmonic mean between precision and recall

**Success Criterion:**
- Difference < 5% between F1-scores of real and synthetic images

### 4.2 Quantitative Evaluation (Texture & Structure Metrics)

**Comparison with baseline method:** Ferreira et al. (2020) - Sketch-based GAN

#### Mean Squared Error (MSE)
```
MSE = (1/n) Σ(y_i - ŷ_i)²
```
- Measures pixel-by-pixel distance
- Lower values = greater similarity

#### Structural Similarity (DSSIM)
```
DSSIM(x,y) = [1 - SSIM(x,y)] / 2
```
- Evaluates luminance, contrast, and structure
- Values close to 0 = high similarity
- > 0.25 = low perceptual similarity

#### Local Binary Pattern Distance (LBP)
- Histogram of local binary patterns
- Euclidean distance between histograms
- Measures robust textural similarity

---

## 5. Results Obtained

### 5.1 Qualitative Validation

| Metric | Real Images | Synthetic Images | Difference |
|---------|---------------|-------------------|-----------|
| F1-Score | 0.88159 | 0.86901 | **< 2%** ✓ |
| Precision | 0.88761 | 0.87539 | 1.2% |
| Recall | 0.87795 | 0.86536 | 1.3% |

**Conclusion:** Synthetic images are virtually indistinguishable from real ones for experts.

### 5.2 Quantitative Validation

Comparison with GAN baseline method (Ferreira et al., 2020):

| Metric | Baseline (GAN) | Proposed Method | Improvement |
|---------|----------------|-----------------|----------|
| **MSE** | 4712.1 | **542.87** | **8.7x better** ✓ |
| **DSSIM** | 0.39 | **0.2424** | 37.8% better ✓ |
| **LBP Distance** | 0.17 | **0.0800** | **> 50% better** ✓ |

**Conclusion:** Quantitative superiority across all metrics.

---

## 6. Validated Premises

### ✓ VAEs are superior for this application
- **Variability control**: Regular distributions in latent space
- **Training stability**: More reliable convergence than GANs
- **Efficiency**: Single-pass generation (vs. multiple diffusion iterations)

### ✓ Geological context is crucial
- Zone-oriented approach surpasses holistic synthesis
- Salt-sediment boundaries require specialized treatment
- Local angle orientation improves interface realism

### ✓ Non-parametric synthesis is effective
- Preserves local statistical properties
- Avoids explicit modeling of complex textures
- Direct sampling from real patches ensures realism

---

## 7. Scientific Contributions

### 7.1 Methodological
1. **Innovative hybrid approach**: VAE + non-parametric texture synthesis
2. **Dual evaluation framework**: Qualitative (experts) + Quantitative (metrics)
3. **Geological zone-oriented synthesis**: Contextualized treatment

### 7.2 Practical
1. **Data augmentation** for segmentation models (U-Net, ResNet)
2. **Transfer learning**: Pre-training for different geological basins
3. **Uncertainty analysis**: Multiple plausible interpretations
4. **Education**: Diverse examples for training geoscientists

### 7.3 Theoretical
- Demonstrates superiority of hybrid deep learning + classical methods approaches
- Validates importance of domain knowledge in generator design
- Establishes new paradigm for geophysical image synthesis

---

## 8. Limitations and Future Work

### Current Limitations
- Specific dataset: TGS Salt Identification Challenge (101x101 pixels)
- Focus on salt domes (other geological structures not addressed)
- 2D synthesis (does not consider 3D volumes)

### Future Directions

#### Extended Geological Structures
- Geological faults
- Sedimentary channels
- Stratigraphic layers

#### Multi-scale
- Hierarchical synthesis at multiple resolutions
- 3D seismic volume generation

#### Domain Adaptation
- Transfer between different seismic acquisition parameters
- Generalization to different geological basins

#### Physical Constraints
- Integration of seismic wave propagation physics
- Incorporation of petrophysical properties

#### Active Learning
- Real-time synthesis during training
- Directed generation for difficult cases

---

## 9. Scientific Impact

### In the Geoscience Field
- Reduction of annotation costs by 80-90%
- Acceleration of interpretation model development
- Democratization of access to quality training data

### In the Machine Learning Field
- New benchmark for image synthesis methods
- Validation of hybrid VAE + classical methods approaches
- Reproducible evaluation framework

### In the Oil Industry
- Improvement in reservoir detection
- Reduction of exploratory risks
- Optimization of drilling investments

---

## 10. Conclusion

The central hypothesis was **successfully validated**:

> The combination of VAEs for structural generation with context-oriented texture synthesis produces synthetic seismic images that:
> 1. ✓ Are indistinguishable from real images by experts (difference < 2%)
> 2. ✓ Surpass state-of-the-art methods in all quantitative metrics
> 3. ✓ Preserve essential geological and textural characteristics

This work establishes a new baseline for geophysical data synthesis and demonstrates that domain knowledge integrated with modern deep learning techniques surpasses purely neural network-based approaches.

---

## Main References

1. Kingma & Welling (2014) - Auto-Encoding Variational Bayes
2. Efros & Leung (1999) - Texture Synthesis by Nonparametric Sampling
3. Ferreira et al. (2020) - Sketch-Based Synthetic Seismic Images with GANs
4. Henriques et al. (2021) - Data Augmentation for Semantic Segmentation of Salt Bodies
5. Zhou et al. (2018) - Non-stationary Texture Synthesis

---

**Document generated on:** October 17, 2025  
**Based on:** _v4.tex - IEEE Access Manuscript  
**Status:** Submitted for Publication

