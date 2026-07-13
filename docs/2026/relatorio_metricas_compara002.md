# Relatorio de Resultados - Execucao compara002 (24-04-2026)

## 1) Objetivo
Este relatorio consolida os resultados do log atual de execucao, agrega as metricas encontradas nos diretorios de saida e apresenta uma consolidacao final com a totalidade das amostras processadas.

## 2) Fontes utilizadas
- Log principal da execucao:
  - D:/0Code/_phdSeismic/textureSSD/comparaBaseFerreira.log
- Resumos por amostra (20 arquivos):
  - D:/0Code/_phdSeismic/textureSSD/result/compara002/stats_*.csv
- Metricas detalhadas por iteracao e amostra (20 arquivos):
  - D:/0Code/_phdSeismic/textureSSD/result/abl_nz_*/data/metrics_*.csv
- Valores quantitativos citados no texto do artigo:
  - D:/0Code/_phdSeismic/textureSSD/documentation/_v6.tex

## 3) Resumo do log atual
- Inicio: 2026-04-24 17:54:48
- Fim: 2026-04-24 17:57:03
- Duracao total: 0:02:14.978610
- Total de amostras: 20
- Sucesso: 20
- Falhas: 0
- Parametros principais observados no log:
  - window_height=40
  - window_width=40
  - kernel_size=11
  - iterations=10
  - selection_method=weighted
  - seed_mode=center
- Diretorio de resultados da rodada:
  - D:/0Code/_phdSeismic/textureSSD/result/compara002

## 4) Metricas por amostra (resumo dos stats_*.csv)
Tabela com media e mediana por amostra.

| sample | mse_mean | mse_median | dssim_mean | dssim_median | lbp_mean | lbp_median |
|---|---:|---:|---:|---:|---:|---:|
| in_100_00000512 | 1054.48 | 1079.97 | 0.12 | 0.12 | 0.04 | 0.04 |
| in_100_00001729 | 1710.69 | 1690.74 | 0.16 | 0.16 | 0.03 | 0.03 |
| in_100_00002209 | 3132.18 | 3128.49 | 0.18 | 0.18 | 0.04 | 0.04 |
| in_100_00002359 | 775.30 | 789.72 | 0.17 | 0.17 | 0.02 | 0.02 |
| in_100_00004387 | 3031.46 | 3135.84 | 0.18 | 0.18 | 0.05 | 0.05 |
| in_100_00004787 | 2328.84 | 2344.21 | 0.11 | 0.11 | 0.04 | 0.04 |
| in_100_00005257 | 1008.60 | 1012.00 | 0.16 | 0.16 | 0.02 | 0.02 |
| in_100_00005642 | 722.48 | 733.13 | 0.15 | 0.15 | 0.03 | 0.03 |
| in_100_00006111 | 2283.47 | 2265.26 | 0.14 | 0.14 | 0.03 | 0.03 |
| in_100_00006263 | 2366.94 | 2387.95 | 0.18 | 0.18 | 0.02 | 0.02 |
| in_100_00006675 | 2213.02 | 2226.59 | 0.13 | 0.12 | 0.02 | 0.02 |
| in_100_00007021 | 2057.66 | 2037.88 | 0.16 | 0.17 | 0.01 | 0.01 |
| in_100_00007882 | 1527.24 | 1504.11 | 0.27 | 0.27 | 0.06 | 0.06 |
| in_100_00009225 | 3126.19 | 3096.04 | 0.14 | 0.15 | 0.03 | 0.03 |
| in_100_00009271 | 856.01 | 862.39 | 0.14 | 0.14 | 0.03 | 0.03 |
| in_100_00011244 | 1938.63 | 1925.77 | 0.11 | 0.11 | 0.04 | 0.04 |
| in_100_00011996 | 2259.30 | 2224.79 | 0.17 | 0.17 | 0.03 | 0.03 |
| in_100_00012077 | 2131.25 | 2154.14 | 0.13 | 0.13 | 0.02 | 0.02 |
| in_100_00012534 | 2841.99 | 2818.42 | 0.18 | 0.18 | 0.02 | 0.02 |
| in_100_00012538 | 1230.81 | 1213.20 | 0.11 | 0.11 | 0.03 | 0.03 |

## 5) Consolidacao final - totalidade das amostras
Consolidacao calculada sobre todos os arquivos metrics_*.csv da rodada atual.

- Total de amostras: 20
- Iteracoes por amostra: 10
- Total de observacoes consolidadas: 200

| metrica | n | min | media | mediana | max | desvio_padrao |
|---|---:|---:|---:|---:|---:|---:|
| mse | 200 | 587.086875 | 1929.826450 | 2037.879688 | 3468.479375 | 789.824672 |
| dssim | 200 | 0.094812 | 0.155116 | 0.153682 | 0.298429 | 0.036463 |
| lbp_distance | 200 | 0.010155 | 0.030653 | 0.028298 | 0.074833 | 0.012801 |
| time_sec | 200 | 0.491328 | 0.522821 | 0.522540 | 0.561117 | 0.013082 |

## 6) Metricas citadas nos diretorios (texto do artigo)
Valores quantitativos explicitamente citados em D:/0Code/_phdSeismic/textureSSD/documentation/_v6.tex:

### 6.1 Comparacao com baseline (Ferreira et al.)
- Baseline (melhor):
  - MSE mediano: 4712.1
  - DSSIM mediano: 0.39
  - LBP Distance mediano: 0.17
- Metodo proposto (citado no texto):
  - MSE mediano: 542.87
  - DSSIM mediano (Group 2): 0.2424
  - LBP Distance mediano (Group 3): 0.0800
- Ganhos reportados no texto:
  - Aproximadamente 8.7x menor MSE
  - Mais de 50% de melhoria em LBP Distance

### 6.2 Avaliacao de especialistas (citada no texto)
- F1 em imagens sinteticas: 0.86901
- F1 em imagens reais: 0.88159
- Diferenca reportada: menor que 2%

## 7) Observacoes para uso no IEEE Access
- Este relatorio separa claramente:
  - resultados da rodada atual (compara002), e
  - valores citados no texto consolidado do artigo (_v6.tex).
- Para evitar ambiguidade na versao final do manuscrito, recomenda-se identificar no texto:
  - qual tabela/figura usa os valores da rodada compara002,
  - e quais valores sao do comparativo historico ja citado no _v6.tex.

## 8) Reprodutibilidade
A consolidacao global deste relatorio foi obtida a partir de:
- 20 arquivos stats_*.csv (resumo por amostra)
- 20 arquivos metrics_*.csv (10 iteracoes por amostra)

Total consolidado: 200 observacoes.