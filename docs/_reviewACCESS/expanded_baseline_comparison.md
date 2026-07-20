# Expanded Baseline Comparison — R2.3

**Manuscrito:** Context-oriented Synthesis of Salt Domes in Labeled Seismic Images  
**Comentário:** Reviewer 2, Issue 3 — *"Expanded baseline comparison"*  
**Status atual no manuscrito:** DONE (seção IV + Tabela adicionadas na revisão atual)  
**Objetivo deste relatório:** Identificar artigos recentes (2022–2026) de GAN, cGAN, diffusion e conditional diffusion para síntese de imagens sísmicas e avaliar quais devem ser adicionados ou mencionados.

---

## 1. O que já está no manuscrito (`_v7.tex`)

### 1.1 Referências já citadas (R2.3)

| Chave | Artigo | Modelo | Alvo | Comparação direta |
|-------|--------|--------|------|-------------------|
| `Ferreira2020` | Ferreira et al., 2020 | cGAN (pix2pix) | Salt domes, falhas | **Sim** (F3, MSE/DSSIM/LBP) |
| `Henriques2021` | Henriques et al., 2021 | VAE + CNF | Salt domes | Não (dataset privado) |
| `Choi2025` | Choi et al., 2025 | cGAN (pix2pix) + Diffusion condicional | Detecção de falhas | Não (dataset privado, métricas downstream) |
| `Wang2021` | Wang et al., 2021 (SeismoGen) | GAN | Waveforms sísmicos | Não (nível de waveform) |
| `pix2pix2017` | Isola et al., 2017 | pix2pix (base) | Imagem-a-imagem genérico | Não aplicável |

### 1.2 Estrutura existente no manuscrito

- **Sec. II (Related Work):** Parágrafo expandido cobrindo os 4 métodos acima + síntese de posicionamento.
- **Sec. IV (subsubsection):** *"Contextual Comparison with GAN-based and Diffusion-based Methods"* — justifica por que apenas Ferreira et al. permite comparação numérica direta.
- **Tabela `comparison_overview`:** 5 linhas (Ferreira, Henriques, Choi, Wang, Proposto).

---

## 2. Artigos candidatos encontrados na pesquisa

### 2.1 GAN-based

#### SeisGAN (2024) — Mathematical Geosciences
- **Referência:** Li et al. (2024). "SeisGAN: …". *Mathematical Geosciences*, doi: 10.1007/s11004-023-10103-8
- **Tarefa:** Denoising e super-resolução de imagens sísmicas (não síntese para augmentação)
- **Acesso:** Paywalled — **conteúdo não verificado**
- **Relevância:** Baixa-média. Tarefa diferente do paper (enhancement vs. síntese rotulada). Pode ser citado como contexto de GAN-based em geofísica, mas não como baseline comparável.
- **Ação recomendada:** Verificar via acesso institucional. Se confirmar task de enhancement/denoising, citar apenas como referência contextual no parágrafo sobre limitações de GANs (Sec. III-A ou Related Work).

#### Dutta et al. (2019) — 3D cGAN para seismic image enhancement
- **Referência:** Dutta, P. et al. "3D Conditional Generative Adversarial Networks to enable large-scale seismic image enhancement." arXiv:1911.06932, NeurIPS 2019 Workshop.
- **Tarefa:** Frequency enhancement e denoising de imagens sísmicas 3D, com conditioning por classe litológica
- **Acesso:** Verificado ✓ (arXiv)
- **Relevância:** **Baixa** — Artigo de 2019 (não recente), foca em enhancement e não em síntese de dados rotulados para augmentação. Não adiciona valor diferencial frente ao Choi 2025 já citado.
- **Ação recomendada:** **Não incluir.** Muito antigo e tarefa diferente.

---

### 2.2 Conditional GAN-based

#### Choi et al. (2025) — já citado ✓
Ver Tabela 1.1 acima.

#### Oliveira et al. (2018/2019) — cGAN para interpolação e super-resolução
- Citados de forma indireta via Wang et al. 2024. Focam em interpolação de dados sísmicos (não síntese rotulada).
- **Ação recomendada:** Não incluir diretamente.

---

### 2.3 Diffusion-based (sem condicionamento explícito)

#### Wei et al. (2023) — Diffusion para interpolação sísmica
- **Referência:** Wei, X. et al. "Seismic data interpolation based on denoising diffusion implicit models with resampling." arXiv:2307.04226, 2023.
- **Tarefa:** Interpolação de traços sísmicos faltantes usando DDIM
- **Relevância:** Baixa — tarefa de reconstrução, não síntese generativa de imagens rotuladas.
- **Ação recomendada:** Não incluir.

#### ScienceDirect 2023 — "Deep diffusion models for seismic processing"
- **Referência:** doi: 10.1016/j.cageo.2023.00081X (ou similar)
- **Tarefa:** Denoising, demultiple, interpolação
- **Acesso:** ❌ HTTP 403 — conteúdo não verificado
- **Relevância:** Provavelmente baixa (processamento, não síntese para augmentação).
- **Ação recomendada:** Verificar acesso institucional; se confirmar tarefa de processamento, não incluir.

---

### 2.4 Conditional Diffusion-based

#### Wang, Huang & Alkhalifah (2024) — Controllable seismic velocity synthesis ⭐ RECOMENDADO
- **Referência:** Wang, F., Huang, X., & Alkhalifah, T. A. "Controllable seismic velocity synthesis using generative diffusion models." *arXiv:2402.06277*, Feb. 2024. KAUST.
- **Tarefa:** Síntese de modelos de velocidade subsuperficial condicionada a class labels, well logs e imagens de refletividade, usando conditional DDPM com classifier-free guidance e cross-attention.
- **Dataset:** OpenFWI (8 classes de modelos de velocidade, 336k amostras, 64×64)
- **Acesso:** Verificado ✓ (arXiv HTML completo)
- **Relevância:** **Média-alta.** Trata de síntese condicional de dados sísmicos para augmentação de modelos de deep learning — objetivo alinhado. A distinção-chave é o domínio-alvo: modelos de velocidade (subsuperfície física) vs. imagens de amplitude sísmica (o que o paper proposto gera). Esta distinção é facilmente explicitável.
- **Ação recomendada:** ✅ **Adicionar ao manuscrito** como novo bibitem e citar no parágrafo contextual da Sec. IV.

#### ConSeisDiff (2025) — ScienceDirect ⭐ POTENCIALMENTE MUITO RELEVANTE
- **Referência:** doi: 10.1016/j.jappgeo.2025.003374 (ou similar)
- **Tarefa:** Diffusion condicional para síntese de dados sísmicos — título indica síntese de imagens sísmicas com condicionamento
- **Acesso:** ❌ HTTP 403 — **conteúdo não verificado**
- **Relevância:** Potencialmente alta — se confirmar síntese de imagens sísmicas (não waveforms nem velocidade) com conditioning, seria o baseline de diffusion condicional mais próximo do paper proposto.
- **Ação recomendada:** ⚠️ **Verificar via acesso institucional antes de citar.** Se confirmar síntese de imagens amplitude + conditioning, adicionar como bibitem e atualizar a tabela `comparison_overview`.

#### Nature 2026 — Multiconditional diffusion for seismic wavefields
- **Tarefa:** Síntese de ground motion (waveforms), não imagens de amplitude
- **Relevância:** Baixa para o paper proposto.
- **Ação recomendada:** Não incluir.

---

## 3. Plano de ação recomendado

### Ação imediata (pode ser feita agora)

**Adicionar Wang et al. (2024)** ao manuscrito:

1. Novo bibitem em `\thebibliography{}`:
```latex
\bibitem{Wang2024diff}
F.~Wang, X.~Huang, and T.~A. Alkhalifah, ``Controllable seismic velocity
synthesis using generative diffusion models,'' \emph{arXiv preprint
arXiv:2402.06277}, Feb. 2024.
```

2. Linha adicional na **Tabela `comparison_overview`** (Sec. IV):
```latex
Wang et al.~\cite{Wang2024diff} & Cond.\ Diffusion (DDPM) & Velocity models & No (velocity domain, OpenFWI metrics) \\
```

3. Frase adicional no parágrafo *"Contextual Comparison"* (Sec. IV):
> *"Wang et al.~\cite{Wang2024diff} propose a conditional diffusion model for seismic velocity synthesis, using classifier-free guidance and cross-attention to incorporate well logs, class labels, and reflectivity images as multi-modal conditions. While their methodology is closely related in spirit — using conditional generation to produce diverse seismic-domain training data — their target domain (subsurface velocity models) differs from the seismic amplitude images synthesized in the present work, precluding direct metric comparison."*

### Ação pendente (requer verificação manual)

| Artigo | O que verificar | Fonte |
|--------|-----------------|-------|
| **SeisGAN** (Math. Geosci. 2024) | Task exata: synthesis vs. enhancement? Que tipo de imagem? | https://link.springer.com/article/10.1007/s11004-023-10103-8 |
| **ConSeisDiff** (ScienceDirect 2025) | Task: síntese de imagens amplitude? Conditioning? Dataset? | https://www.sciencedirect.com/science/article/pii/S0926985125003374 |

---

## 4. Avaliação de suficiência da resposta atual ao R2.3

O manuscrito revisado já responde adequadamente ao R2.3 ao:
- ✅ Expandir o Related Work com 4 métodos (Ferreira, Henriques, Choi, Wang)
- ✅ Cobrir todas as categorias pedidas: cGAN (Ferreira + Choi), diffusion condicional (Choi), GAN puro (Wang)
- ✅ Criar subsubsection explícita + Tabela comparativa
- ✅ Justificar por que comparação numérica direta é impossível para os outros métodos

**Lacuna potencial:** Ausência de um artigo de diffusion para síntese de *imagens de amplitude* sísmica (não velocity, não waveforms). Wang et al. (2024) preenche parcialmente essa lacuna. ConSeisDiff (2025) pode preencher completamente, se verificado.

**Impacto esperado da adição de Wang et al. 2024:** Fortalece a cobertura da categoria *conditional diffusion* com uma referência de 2024, publicada por grupo reconhecido (KAUST), com arXiv público.

---

*Relatório gerado em 2026-07-19. Baseado em pesquisa de artigos acessíveis via arXiv e web.*
Próximos passos sugeridos:

(A) Posso adicionar Wang et al. (2024) ao _v7.tex agora — novo bibitem + linha na tabela + frase no parágrafo contextual
(B) Para SeisGAN e ConSeisDiff: verificar via acesso institucional (Springer/ScienceDirect) antes de citar