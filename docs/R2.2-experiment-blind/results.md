
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

