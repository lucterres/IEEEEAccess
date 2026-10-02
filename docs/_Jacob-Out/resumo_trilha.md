# Resumo da Trilha de Discussão

## 1. Objetivo geral

O trabalho avalia se imagens sísmicas sintéticas de domos de sal são suficientemente realistas para:

- apresentar características semelhantes às imagens reais;
- produzir respostas semelhantes nas segmentações manuais feitas por especialistas;
- enriquecer o conjunto de treinamento de modelos de segmentação automatizada.

A discussão foi organizada em três avaliações complementares:

1. discriminação visual entre imagens reais e sintéticas;
2. segmentação manual das regiões de sal por especialistas;
3. desempenho de um modelo automatizado treinado com a inclusão de imagens sintéticas.

---

## 2. Discriminação entre imagens reais e sintéticas

### 2.1 Questão inicial

A primeira dúvida foi se os especialistas conseguiam distinguir imagens reais de sintéticas e se a taxa de aproximadamente 64% indicava que as imagens sintéticas eram facilmente identificáveis.

Uma acurácia de 50% representaria classificação aleatória. Portanto, o resultado observado mostra desempenho acima do acaso, mas não discriminação perfeita.

### 2.2 Protocolo e hipótese estatística

No experimento cego, os especialistas classificaram imagens embaralhadas como reais ou sintéticas, sem conhecer previamente a origem das imagens.

As hipóteses foram:

- **H0:** os especialistas classificam as imagens ao acaso, com acurácia esperada de 50%;
- **H1:** a acurácia dos especialistas é superior a 50%.

Resultado observado:

- 172 acertos em 270 classificações;
- acurácia global de **63,7%**;
- teste binomial com **p = 0,000004**.

Como o valor de p é inferior a 0,05, rejeita-se H0. Assim, os especialistas distinguiram as imagens reais e sintéticas melhor do que seria esperado pelo acaso.

Esse resultado não demonstra que exista um padrão oculto geral nos dados. Ele mostra especificamente que a classificação real/sintética teve desempenho estatisticamente superior a 50%.

### 2.3 Interpretação adequada

A afirmação original de que as imagens eram “virtually indistinguishable” foi considerada forte demais diante do resultado do experimento cego.

A interpretação mais adequada é que as imagens sintéticas foram **suficientemente realistas para desafiar a discriminação dos especialistas**, embora não tenham sido completamente indistinguíveis das imagens reais.

A taxa de erro também é relevante:

- erro em imagens reais: **37,0%**;
- erro em imagens sintéticas: **35,6%**;
- diferença entre as taxas: **1,4 ponto percentual**.

A proximidade entre essas taxas sugere ausência de forte viés em favor de uma das classes. Entretanto, essa observação descritiva não equivale, por si só, à aceitação formal da hipótese nula de igualdade entre as taxas de erro.

---

## 3. Segmentação manual pelos especialistas

### 3.1 O que é medido

O experimento de segmentação manual é diferente do experimento de discriminação real/sintético.

Na segmentação manual, os especialistas identificam os pixels pertencentes às regiões de sal. As máscaras produzidas são comparadas com as máscaras de referência (*ground truth*).

### 3.2 F1-score

O F1-score é calculado a partir da comparação, pixel a pixel, entre a máscara produzida pelo especialista e a máscara de referência.

A métrica combina precisão e recall e pode ser expressa por:

$$
F1 = 2 \cdot \frac{\mathrm{precision} \cdot \mathrm{recall}}
{\mathrm{precision} + \mathrm{recall}}
$$

Na segmentação de imagens, o F1-score é equivalente ao coeficiente de similaridade de Dice. Seu valor varia de 0 a 1:

- 1 representa sobreposição perfeita entre as máscaras;
- 0 representa ausência de sobreposição.

### 3.3 Análise desejada

A análise deve verificar se os acertos e erros da segmentação manual são distribuídos de forma semelhante entre imagens reais e sintéticas.

Essa comparação ajudaria a mostrar que as imagens sintéticas contêm variações de casos suficientemente similares às imagens reais do ponto de vista da interpretação dos especialistas.

É importante separar dois tipos de erro:

1. erro ao classificar a origem da imagem como real ou sintética;
2. erro ao marcar os pixels pertencentes à região de sal.

Os valores de 37,0% e 35,6% referem-se ao primeiro tipo de erro e não diretamente à segmentação dos pixels.

---

## 4. Melhoria do treinamento automatizado

### 4.1 Hipótese aplicada

O objetivo final da síntese é enriquecer o conjunto de dados para treinar modelos capazes de segmentar imagens reais.

O resultado mais aplicado do trabalho é verificar se a inclusão de imagens sintéticas melhora o treinamento do sistema de segmentação.

### 4.2 Resultado observado

A inclusão das imagens sintéticas produziu os seguintes resultados de IoU:

- treinamento sem a contribuição sintética: **0,4081**;
- treinamento com imagens sintéticas: **0,4276**;
- ganho absoluto: **+0,0195**;
- ganho relativo aproximado: **+4,8%**.

A melhoria foi observada nos três *seeds* avaliados.

Esse resultado sustenta um argumento mais forte e aplicado do que a alegação de indistinguibilidade visual: as imagens sintéticas não apenas parecem plausíveis, mas também podem contribuir para o treinamento de modelos de segmentação.

---

## 5. Esclarecimento sobre a Tabela 1

As colunas da tabela representam acertos separados por tipo de imagem:

- **Evaluator Acc. real (%):** percentual de imagens reais classificadas corretamente;
- **Acc. synth. (%):** percentual de imagens sintéticas classificadas corretamente;
- **Overall acc. (%):** acurácia geral do avaliador.

Esses valores não são probabilidades complementares da mesma amostra. Por isso, a soma das colunas de acurácia para imagens reais e sintéticas não precisa resultar em 100%.

A finalidade dessa separação é verificar se havia desbalanceamento na capacidade de classificação entre as duas classes. Os resultados ficaram próximos da média geral de aproximadamente 64%.

---

## 6. Conclusões principais

- O experimento cego mostrou discriminação real/sintético acima do acaso.
- A acurácia de 63,7% indica que as imagens não são totalmente indistinguíveis, mas ainda confundem os especialistas em uma parcela relevante dos casos.
- As taxas de erro para imagens reais e sintéticas foram próximas, sem evidência descritiva de forte viés entre as classes.
- O F1-score da segmentação manual deve ser explicado explicitamente como comparação pixel a pixel entre a máscara do especialista e a *ground truth*.
- A inclusão de imagens sintéticas melhorou o IoU do modelo automatizado nos três *seeds* avaliados.
- O argumento central deve enfatizar a utilidade das imagens sintéticas para ampliar a diversidade do treinamento e melhorar a segmentação de imagens reais.

---

## 7. Pendências para a revisão do manuscrito

1. Manter a formulação moderada sobre realismo visual e retirar ou substituir “virtually indistinguishable”.
2. Explicar claramente o protocolo do experimento cego e o teste binomial.
3. Explicar o cálculo do F1-score na seção de métricas de avaliação.
4. Esclarecer na Tabela 1 que as acurácias são calculadas separadamente por classe de imagem.
5. Apresentar, quando possível, uma matriz de confusão da discriminação real/sintético.
6. Comparar explicitamente os resultados de segmentação manual entre imagens reais e sintéticas.
7. Destacar o ganho de IoU obtido com a inclusão das imagens sintéticas.
8. Evitar afirmar que a hipótese nula foi aceita apenas porque as taxas de erro são próximas; usar uma formulação compatível com o poder estatístico do experimento.
