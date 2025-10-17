# Hipótese Científica do Trabalho

## Context-Oriented Synthesis of Salt Domes in Labeled Seismic Images

### Autores
- Luciano D. Terres (UFRGS / Petrobras)
- Jacob Scharcanski (UFRGS)

---

## 1. Hipótese Principal

**A combinação de Variational Autoencoders (VAEs) para geração de máscaras geométricas com síntese de textura orientada por contexto pode gerar imagens sísmicas sintéticas de domos de sal que sejam virtualmente indistinguíveis de imagens sísmicas reais por especialistas em geociências.**

---

## 2. Problema Científico

### Contexto
- Modelos de deep learning para segmentação de corpos salinos requerem grandes volumes de dados anotados
- Anotação de imagens sísmicas é cara e requer expertise especializado
- Datasets limitados restringem a generalização dos modelos
- Exploração petrolífera offshore depende de identificação precisa de estruturas salinas

### Desafio Técnico
Como gerar dados sintéticos de alta qualidade que preservem:
1. **Características estruturais** - geometrias geologicamente plausíveis
2. **Propriedades texturais** - padrões sísmicos realistas
3. **Interfaces complexas** - fronteiras nítidas entre sal e sedimento

---

## 3. Componentes da Hipótese

### 3.1 Geração de Geometrias (VAE)

**Sub-hipótese:** Um VAE pode aprender a distribuição de probabilidade de geometrias de domos salinos e gerar novas máscaras estruturais realistas.

**Fundamento Teórico:**
- VAEs modelam distribuições de dados no espaço latente
- Interpolação no espaço latente gera geometrias intermediárias plausíveis
- Regularização KL garante suavidade e continuidade das formas geradas

**Vantagens sobre alternativas:**
- **vs. GANs**: Maior estabilidade de treinamento, controle de variabilidade
- **vs. Modelos de Difusão**: Menor custo computacional, eficiência em datasets pequenos
- **vs. Transformações Geométricas**: Maior diversidade e realismo geológico

### 3.2 Síntese de Textura Orientada por Contexto

**Sub-hipótese:** Dividir o processo de síntese em três zonas distintas (sal, fronteira, sedimento) produz imagens mais realistas que abordagens holísticas.

**Fundamento Teórico:**
- Imagens sísmicas são **não-estacionárias** (texturas variam espacialmente)
- Zonas de fronteira têm características acústicas únicas
- Síntese não-paramétrica preserva propriedades estatísticas locais

**Componentes das Zonas:**

#### Zona de Fronteira (Edge Zone)
- Alto contraste sísmico
- Padrões de bandas claras e escuras paralelas
- Seleção de patches orientada por ângulo local
- Detecção de bordas + dilatação morfológica

#### Zona de Sal
- Textura homogênea característica
- Propriedades acústicas específicas do sal
- Síntese baseada em patches de referência de sal

#### Zona de Sedimento Convencional
- Texturas estratigráficas variadas
- Síntese baseada em patches de rocha sedimentar

### 3.3 Qualidade Comparável a Dados Reais

**Sub-hipótese:** As imagens sintéticas serão de qualidade suficiente para:
1. Enganar especialistas humanos (indistinguibilidade perceptual)
2. Servir como dados de augmentação para treinamento de modelos
3. Superar métodos state-of-the-art em métricas quantitativas

---

## 4. Metodologia de Validação

### 4.1 Avaliação Qualitativa (Expert Assessment)

**Protocolo:**
- 3 geocientistas especializados em interpretação sísmica
- Tarefa: identificar regiões de sal em imagens reais e sintéticas
- Comparação: máscaras geradas por especialistas vs. ground truth

**Métricas:**
- **Precision**: Proporção de pixels corretamente identificados como sal
- **Recall**: Proporção de pixels de sal efetivamente detectados
- **F1-Score**: Média harmônica entre precisão e recall

**Critério de Sucesso:**
- Diferença < 5% entre F1-scores de imagens reais e sintéticas

### 4.2 Avaliação Quantitativa (Texture & Structure Metrics)

**Comparação com método baseline:** Ferreira et al. (2020) - GAN baseado em sketches

#### Mean Squared Error (MSE)
```
MSE = (1/n) Σ(y_i - ŷ_i)²
```
- Mede distância pixel-a-pixel
- Valores menores = maior similaridade

#### Structural Similarity (DSSIM)
```
DSSIM(x,y) = [1 - SSIM(x,y)] / 2
```
- Avalia luminância, contraste e estrutura
- Valores próximos a 0 = alta similaridade
- > 0.25 = baixa similaridade perceptual

#### Local Binary Pattern Distance (LBP)
- Histograma de padrões binários locais
- Distância Euclidiana entre histogramas
- Mede similaridade textural robusta

---

## 5. Resultados Obtidos

### 5.1 Validação Qualitativa

| Métrica | Imagens Reais | Imagens Sintéticas | Diferença |
|---------|---------------|-------------------|-----------|
| F1-Score | 0.88159 | 0.86901 | **< 2%** ✓ |
| Precision | 0.88761 | 0.87539 | 1.2% |
| Recall | 0.87795 | 0.86536 | 1.3% |

**Conclusão:** Imagens sintéticas são virtualmente indistinguíveis de reais para especialistas.

### 5.2 Validação Quantitativa

Comparação com método GAN baseline (Ferreira et al., 2020):

| Métrica | Baseline (GAN) | Método Proposto | Melhoria |
|---------|----------------|-----------------|----------|
| **MSE** | 4712.1 | **542.87** | **8.7x melhor** ✓ |
| **DSSIM** | 0.39 | **0.2424** | 37.8% melhor ✓ |
| **LBP Distance** | 0.17 | **0.0800** | **> 50% melhor** ✓ |

**Conclusão:** Superioridade quantitativa em todas as métricas.

---

## 6. Premissas Validadas

### ✓ VAEs são superiores para esta aplicação
- **Controle de variabilidade**: Distribuições regulares no espaço latente
- **Estabilidade de treinamento**: Convergência mais confiável que GANs
- **Eficiência**: Geração em passagem única (vs. múltiplas iterações de difusão)

### ✓ Contexto geológico é crucial
- Abordagem orientada por zonas supera síntese holística
- Fronteiras entre sal e sedimento requerem tratamento especializado
- Orientação por ângulo local melhora realismo das interfaces

### ✓ Síntese não-paramétrica é eficaz
- Preserva propriedades estatísticas locais
- Evita modelagem explícita de texturas complexas
- Amostragem direta de patches reais garante realismo

---

## 7. Contribuições Científicas

### 7.1 Metodológica
1. **Abordagem híbrida inovadora**: VAE + síntese de textura não-paramétrica
2. **Framework de avaliação dual**: Qualitativo (experts) + Quantitativo (métricas)
3. **Síntese orientada por zonas geológicas**: Tratamento contextualizado

### 7.2 Prática
1. **Augmentação de dados** para modelos de segmentação (U-Net, ResNet)
2. **Transfer learning**: Pré-treinamento para diferentes bacias geológicas
3. **Análise de incerteza**: Múltiplas interpretações plausíveis
4. **Educação**: Exemplos diversos para treinamento de geocientistas

### 7.3 Teórica
- Demonstra superioridade de abordagens híbridas deep learning + métodos clássicos
- Valida importância de conhecimento de domínio em design de geradores
- Estabelece novo paradigma para síntese de imagens geofísicas

---

## 8. Limitações e Trabalhos Futuros

### Limitações Atuais
- Dataset específico: TGS Salt Identification Challenge (101x101 pixels)
- Foco em domos de sal (outras estruturas geológicas não abordadas)
- Síntese 2D (não considera volumes 3D)

### Direções Futuras

#### Estruturas Geológicas Estendidas
- Falhas geológicas
- Canais sedimentares
- Camadas estratigráficas

#### Multi-escala
- Síntese hierárquica em múltiplas resoluções
- Geração de volumes sísmicos 3D

#### Adaptação de Domínio
- Transferência entre diferentes parâmetros de aquisição sísmica
- Generalização para diferentes bacias geológicas

#### Restrições Físicas
- Integração de física de propagação de ondas sísmicas
- Incorporação de propriedades petrofísicas

#### Active Learning
- Síntese em tempo real durante treinamento
- Geração dirigida para casos difíceis

---

## 9. Impacto Científico

### No Campo da Geociência
- Redução de custos de anotação em 80-90%
- Aceleração de desenvolvimento de modelos de interpretação
- Democratização de acesso a dados de treinamento de qualidade

### No Campo de Machine Learning
- Novo benchmark para métodos de síntese de imagens
- Validação de abordagens híbridas VAE + métodos clássicos
- Framework de avaliação reproducível

### Na Indústria Petrolífera
- Melhoria na detecção de reservatórios
- Redução de riscos exploratórios
- Otimização de investimentos em perfuração

---

## 10. Conclusão

A hipótese central foi **validada com sucesso**:

> A combinação de VAEs para geração estrutural com síntese de textura orientada por contexto produz imagens sísmicas sintéticas que:
> 1. ✓ São indistinguíveis de imagens reais por especialistas (diferença < 2%)
> 2. ✓ Superam métodos state-of-the-art em todas as métricas quantitativas
> 3. ✓ Preservam características geológicas e texturais essenciais

Este trabalho estabelece uma nova linha de base para síntese de dados geofísicos e demonstra que conhecimento de domínio integrado a técnicas modernas de deep learning supera abordagens puramente baseadas em redes neurais.

---

## Referências Principais

1. Kingma & Welling (2014) - Auto-Encoding Variational Bayes
2. Efros & Leung (1999) - Texture Synthesis by Nonparametric Sampling
3. Ferreira et al. (2020) - Sketch-Based Synthetic Seismic Images with GANs
4. Henriques et al. (2021) - Data Augmentation for Semantic Segmentation of Salt Bodies
5. Zhou et al. (2018) - Non-stationary Texture Synthesis

---

**Documento gerado em:** 17 de outubro de 2025  
**Baseado em:** _v4.tex - IEEE Access Manuscript  
**Status:** Submitted for Publication
