
############################################################
  ESPECIALISTA: Expert_1
############################################################

  ========================================
  Tipo: REAL  (n=45)
  ========================================
      precision  recall  f1_score
mean     0.8729  0.8856    0.8735
std      0.0857  0.0857    0.0519

  ========================================
  Tipo: SYNTHETIC  (n=45)
  ========================================
      precision  recall  f1_score
mean     0.8661  0.8898    0.8741
std      0.0808  0.0668    0.0492

############################################################
  ESPECIALISTA: Expert_2
############################################################

  ========================================
  Tipo: REAL  (n=45)
  ========================================
      precision  recall  f1_score
mean     0.8875  0.8631    0.8719
std      0.0746  0.0766    0.0544

  ========================================
  Tipo: SYNTHETIC  (n=45)
  ========================================
      precision  recall  f1_score
mean     0.8914  0.8572    0.8699
std      0.0624  0.0806    0.0431

############################################################
  ESPECIALISTA: Expert_3
############################################################

  ========================================
  Tipo: REAL  (n=45)
  ========================================
      precision  recall  f1_score
mean     0.8220  0.7912    0.8009
std      0.0797  0.0965    0.0606

  ========================================
  Tipo: SYNTHETIC  (n=45)
  ========================================
      precision  recall  f1_score
mean     0.8058  0.7587    0.7770
std      0.0981  0.0675    0.0577

############################################################
  CONJUNTO COMPLETO (todos os especialistas)
############################################################

  ========================================
  Tipo: REAL  (n=135)
  ========================================
      precision  recall  f1_score
mean     0.8608  0.8466    0.8488
std      0.0844  0.0950    0.0649

  ========================================
  Tipo: SYNTHETIC  (n=135)
  ========================================
      precision  recall  f1_score
mean     0.8544  0.8352    0.8403
std      0.0888  0.0907    0.0673

======================================================================
  AVALIAÇÃO: Julgamento de Origem (real vs synthetic) por Especialista
  Excluídas imagens de controle
======================================================================
Especialista Ground Truth  Total  Acertos  Erros  Acurácia (%)
    Expert_1         real     45       28     17          62.2
    Expert_1    synthetic     45       30     15          66.7
    Expert_2         real     45       30     15          66.7
    Expert_2    synthetic     45       31     14          68.9
    Expert_3         real     45       27     18          60.0
    Expert_3    synthetic     45       26     19          57.8

=== Resumo Geral por Especialista ===
                Total  Acertos  Erros  Acuracia_pct
evaluator_name                                     
Expert_1           90       58     32          64.4
Expert_2           90       61     29          67.8
Expert_3           90       53     37          58.9


=================================================================
  ESTATÍSTICAS GERAIS — todos especialistas, todas imagens
  (excluindo controle)
=================================================================
  Total avaliações : 270
  Acertos          : 172  (63.7%)
  Erros            : 98  (36.3%)

  Detalhamento por tipo:
    real        : 85/135  (63.0% acurácia)
    synthetic   : 87/135  (64.4% acurácia)

  Matriz de Confusão (contagens):
Predito       real  synthetic
Ground Truth                 
real            85         50
synthetic       48         87

  Matriz de Confusão (% por linha — taxa por classe):
Predito       real  synthetic
Ground Truth                 
real          63.0       37.0
synthetic     35.6       64.4




=================================================================
  TESTE BINOMIAL — Discriminação acima do acaso?
  H0: p = 0.50  |  H1: p > 0.50  |  α = 0.05
=================================================================
  n (avaliações)   : 270
  k (acertos)      : 172
  p observado      : 0.6370  (63.7%)
  p-valor (exato)  : 0.000004
  IC 95% [low, –)  : [0.5861, 1.0)

  ✔ REJEITA H0  (p = 0.0000 < α = 0.05)
  → Os especialistas discriminam ACIMA do acaso (p > 0.50).
  → A acurácia de 63.7% é estatisticamente significativa.

  Detalhamento por tipo de imagem:
  Tipo             k     n    p_obs    p-valor  Conclusão
  -----------------------------------------------------------------
  real            85   135   0.6296   0.001640  ✔ sig.
  synthetic       87   135   0.6444   0.000500  ✔ sig.

  Nota: 'sig.' = significativo (p < 0.05), 'n.s.' = não significativo


Total de imagens de controle no dataset: 10
Especialistas: Expert_1, Expert_2, Expert_3

=== Contagem e Avaliação — Imagens de Controle ===
              Total controle  Corretos (∅)  Falso Positivo  Taxa FP (%)  Julgou: real  Julgou: synth  Julgou: ctrl
Especialista                                                                                                      
Expert_1                  10            10               0          0.0             0              0            10
Expert_2                  10            10               0          0.0             0              0            10
Expert_3                  10            10               0          0.0 



Se os avaliadores acertam 65%–70%, então:

eles estão distinguindo real vs. sintético melhor que o acaso;
a afirmação “virtually indistinguishable” fica fraca ou inválida;
omitir o experimento depois de tê-lo feito seria metodologicamente ruim perante o revisor.
O que fazer
1. Reformular a hipótese principal
Trocar algo como:

“virtually indistinguishable from real images”
por algo mais defensável, por exemplo:

“highly realistic and geologically plausible”
“comparable to real seismic images for salt-body interpretation”
“sufficiently realistic to support expert interpretation and downstream use”
2. Reportar o blind experiment com honestidade
Se deu 65%–70%, o resultado ainda pode ser útil. Ele permite dizer algo como:  as imagens sintéticas apresentam alto realismo perceptual;
porém não são completamente indistinguíveis das reais;
ainda assim preservam características relevantes para interpretação.
3. Ajustar a conclusão
Em vez de dizer que os especialistas não conseguem distinguir, dizer que:
a discriminação foi moderada;
apesar disso, a qualidade perceptual foi alta;
o experimento de interpretação de sal continua mostrando utilidade prática.

Formulação possível
The blind discrimination experiment showed that evaluators distinguished real from synthetic images with an accuracy of 65–70%, indicating that the generated images are highly realistic but not fully indistinguishable from real seismic images. Accordingly, we moderated this claim and now state that the proposed method produces geologically plausible and visually convincing synthetic images that are comparable to real ones for salt-body interpretation.

nova hipótese principal - > 


The main research hypothesis of this work is that the proposed combination of VAE-based mask generation and context-oriented texture synthesis can generate synthetic seismic images that are geologically plausible, visually realistic, and comparable to real seismic images for salt-body interpretation.


parágrafo do manuscrito,
resposta ao revisor.
