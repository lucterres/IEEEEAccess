Reviewers' Comments to Author:

Reviewer: 1

Comments:
  This paper presents a practical and effective method for synthesizing
realistic seismic images of salt domes using a VAE for mask generation and
context‑aware texture synthesis. The expert evaluation and quantitative
comparisons are convincing. However, a few important points need
clarification
or minor revision.

Major Required Revisions
 1. Comparison with Henriques et al. – The related work mentions their
approach but does not clearly articulate the technical novelty of your
method.
Please explicitly state the key differences in architecture and why your
texture‑synthesis strategy is advantageous over their generative model.

  2. VAE implementation details – The architecture is described only as
stacked dense layers. Please specify the number of neurons per layer, latent
dimension d, training hyperparameters, and whether convolutional layers were
used (and why).

 3. Expert evaluation design – It is unclear whether experts were blinded to
the real/synthetic distinction. If not, please acknowledge this as a
limitation.
Also clarify whether real and synthetic images were mixed during the
assessment.

 4. Statistical significance for DSSIM – The improvement in DSSIM is small
(~2.2%). Please add a statistical test (e.g., Wilcoxon) to confirm
significance,
or otherwise discuss the result candidly while highlighting gains in MSE and
LBP.

Additional Questions:
Please confirm that you have reviewed all relevant files, including
supplementary files and any author response files, which can be found in the
"View Author's Response" link above (author responses will only appear for
resubmissions): Yes, all files have been reviewed

1) Does the paper contribute to the body of knowledge?: Yes.

2) Is the paper technically sound?: Yes.

3) Is the subject matter presented in a comprehensive manner?: Yes

4) Are the references provided applicable and sufficient?: Yes.

5) Are there references that are not appropriate for the topic being
discussed?:
No

5a) If yes, then please indicate which references should be removed.:

Reviewer: 2

Comments:
The manuscript proposes a context-oriented seismic image synthesis framework
for
generating labeled salt dome images. The idea of combining VAE-generated salt
masks with zone-specific texture synthesis is relevant and potentially
valuable
for seismic interpretation and data augmentation. The paper is generally well
motivated, and the use of expert evaluation together with quantitative image
similarity metrics is a useful starting point.

However, several important issues should be addressed before the work can be
considered mature enough for publication.

First, the manuscript should include a downstream segmentation experiment.
Since
the central motivation is to generate synthetic labeled data for training
machine learning models, it is necessary to demonstrate that the proposed
synthetic data improves segmentation performance on real seismic test data. A
comparison between training with real data only and training with real plus
synthetic data would significantly strengthen the paper.

Second, the claim that synthetic images are “virtually indistinguishable”
from real images should be moderated or supported by a proper blind
discrimination experiment. The current expert evaluation measures how experts
identify salt regions, but it does not directly test whether experts can
distinguish real images from generated ones.

Third, the comparison with existing methods should be expanded. The
manuscript
mainly compares with Ferreira et al., but stronger or more recent generative
baselines, such as GAN-based, conditional GAN-based, diffusion-based, or
conditional diffusion-based seismic image synthesis methods, should be
considered.

Fourth, the experimental setting needs clearer explanation. In particular,
the
quantitative results in Table 3 and the ablation study appear to use
different
numerical ranges and possibly different datasets or protocols. The authors
should clarify the datasets, sample sizes, preprocessing, normalization, and
evaluation procedures used in each experiment.

Fifth, the paper should improve reproducibility. Important implementation
details are missing, including VAE latent dimension, training epochs,
optimizer,
learning rate, loss settings, patch size, boundary dilation width, texture
database construction, and sampling parameters. These details are essential
for
readers who wish to reproduce or extend the work.

Overall, the manuscript has a promising idea and addresses a meaningful
application problem, but substantial revisions are needed to strengthen the
experimental validation, improve the rigor of the claims, and clarify the
methodology.

Additional Questions:
Please confirm that you have reviewed all relevant files, including
supplementary files and any author response files, which can be found in the
"View Author's Response" link above (author responses will only appear for
resubmissions): Yes, all files have been reviewed

1) Does the paper contribute to the body of knowledge?: Yes, the paper makes
a
moderate contribution by proposing a context-oriented seismic image synthesis
method combining VAE-based salt mask generation and zone-specific texture
synthesis. However, the contribution should be strengthened by demonstrating
the
usefulness of the generated images in downstream segmentation tasks.

2) Is the paper technically sound?: Partially. The proposed framework is
technically reasonable, but the manuscript lacks important implementation
details, stronger baseline comparisons, and downstream task validation. Some
experimental results also require clearer explanation.

3) Is the subject matter presented in a comprehensive manner?: Partially. The
paper presents the motivation, method, and experiments in a generally clear
way,
but the coverage of recent generative methods and the discussion of practical
data augmentation effectiveness are insufficient.

4) Are the references provided applicable and sufficient?: Partially. The
references are applicable to the topic, especially those related to seismic
image synthesis, data augmentation, VAE, texture synthesis, and image
similarity
evaluation. However, they are not fully sufficient. The manuscript should
include more recent and stronger references on GAN-based and diffusion-based
seismic image generation, and the comparison with prior work should be
expanded
beyond one main baseline.

5) Are there references that are not appropriate for the topic being
discussed?:
No

5a) If yes, then please indicate which references should be removed.:

If you have any questions, please contact article administrator: Mrs. Sweta
Satapathy s.satapathy@ieee.org

Links:
------
[1] https://ieee.atyponrex.com/journal/ieee-access