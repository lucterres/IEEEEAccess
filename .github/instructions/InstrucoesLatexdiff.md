# Instruções: Gerar PDF com Diferenças entre Versões (latexdiff)

> Atualizado: 2026-07-14  
> Contexto: diff entre `_v6.tex` (submetido) e `_v7.tex` (revisado)  
> Requisito IEEE Access: submeter "Highlighted PDF" com mudanças marcadas em amarelo  
> **Status: ✅ Processo testado e funcional — gera `latex_build/review_clean.pdf`**

---

## 📚 Documentação Integrada

Este processo está documentado de forma integrada em dois locais:

| Local | Conteúdo |
|-------|----------|
| **`.github/skills/latexdiff-review-pdf/SKILL.md`** | Skill para VS Code — invoca este workflow automaticamente |
| **`.github/skills/latexdiff-review-pdf/references/fix-errors.md`** | Catálogo completo: 9 erros comuns + fixes de latexdiff |
| **`.github/instructions/InstrucoesLatexdiff.md`** (este arquivo) | Workflow completo com passo-a-passo e detalhes técnicos |
| **`.github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py`** | Implementação Python (9+ passos de limpeza) |

> **Para resolver erros latexdiff não-óbvios**, consulte `.github/skills/latexdiff-review-pdf/references/fix-errors.md`

---

## Arquivos de Referência

| Papel | Arquivo |
|-------|---------|
| Versão OLD (submetida) | `docs/reviewPacote-submetido-jun/_v6.tex` |
| Versão NEW (revisada)  | `_v7.tex` |
| Script de limpeza      | `.github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py` |
| PDF diff (saída final) | `latex_build/review_clean.pdf` |

---

## Passo a Passo (Processo Completo)

Execute os 3 comandos abaixo a partir da raiz do repositório:

### 1. Gerar o `.tex` de diferenças

```powershell
latexdiff --allow-spaces --math-markup=0 `
  "docs/reviewPacote-submetido-jun/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex
```

### 2. Limpar o arquivo gerado

```powershell
python .github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py latex_build/review_raw.tex latex_build/review_clean.tex
```

O script deve reportar:
```
\DIFadd{} markers preserved: <N>
\DIFdel{} markers preserved: <N>
FL markers left (should be 0): 0
providecommand{} empty left:  0
```

### 3. Compilar para PDF (duas passagens)

```powershell
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex
```

Verificar ausência de erros fatais:
```powershell
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex 2>&1 | Select-String "^!"
```

---

## Resultado Esperado no PDF

| Marcação | Significado |
|----------|-------------|
| Texto com **fundo amarelo** | Conteúdo adicionado na versão `_v7` |
| Texto ~~riscado~~ (sem cor) | Conteúdo removido da versão `_v6` |
| Texto em **azul** (equações) | Inserção em modo matemático (fallback — `soul` não funciona em math) |

> ⚠️ A classe `ieeeaccess` usa o pacote `color` básico. O script injeta `xcolor` antes do `soul` para garantir compatibilidade.

---

## O que o Script de Limpeza Faz

O `latexdiff_cleanup.py` aplica as seguintes transformações em ordem:

| Passo | Ação |
|-------|------|
| 0  | Remove blocos `\DIFdelbegin...\DIFdelend` estruturais (que contêm `%DIFDELCMD`) |
| 1  | Remove linhas de comentários `%DIFDELCMD`, `%DIFAUXCMD`, `%DIF </>` |
| 2  | Remove marcadores `\DIFaddFL{}`/`\DIFdelFL{}` de tabelas (loop até estabilizar) |
| 3  | Remove marcadores FL de ambiente (`\DIFaddbeginFL` etc.) fora do preâmbulo |
| 4  | Remove `\providecommand{}{}` vazios deixados pela remoção FL |
| 5  | Corrige `\lstset{extendedchars=\true}` → `extendedchars=true` |
| 6  | Corrige desbalanceamento de `\begin{enumerate}` / `\end{enumerate}` |
| 7  | Remove `\end{comment}` órfãos (quando `\begin{comment}` estava em bloco deletado) |
| 8b | Remove `\textcolor{}{}`wrappers dentro de `\DIFadd{}` (incompatíveis com `soul`) |
| 8  | Injeta no preâmbulo: `soul` + `xcolor` + `\renewcommand{\DIFadd}` (amarelo) + `\renewcommand{\DIFdel}` (riscado) |

### Por que `soul` + `xcolor` e não `\colorbox`?

`\colorbox{yellow}{texto}` é um `\hbox` — **não quebra linha**, transborda a margem em parágrafos longos.  
`\hl{}` do pacote `soul` quebra linha corretamente, mas exige:
1. `xcolor` carregado **antes** do `soul` (a classe `ieeeaccess` carrega apenas o `color` básico)
2. Que o argumento de `\hl{}` **não contenha `\textcolor`** — por isso o passo 8b remove esses wrappers

---

## Problemas Conhecidos (Resolvidos)

| Problema | Causa | Solução no script |
|----------|-------|-------------------|
| `\providecommand{}{}` no preâmbulo | Remoção dos marcadores FL deixa providecommand vazio | `.replace()` literal em loop |
| `\lstset{extendedchars=\true}` | latexdiff gera `\true` inválido | substituição direta |
| `\textbf{}` vazios | conteúdo deletado dentro de `\textbf{}` | bloco DIFdelbegin removido pelo passo 0 |
| `\end{comment}` órfão | `\begin{comment}` estava dentro de bloco deletado | contagem e remoção do excesso |
| `\begin{enumerate}` sem `\end` | latexdiff truncou o bloco | inserção do `\end{enumerate}` faltando |
| `soul` trava com `\textcolor` em `\DIFadd{}` | `soul` tokeniza o argumento e não consegue processar `\textcolor` | strip `\textcolor{}{}` no passo 8b |
| Texto amarelo transborda margem | `\colorbox` não quebra linha | substituído por `soul`/`\hl` + `xcolor` |
| `Undefined color '\let'` | `soul` conflita com `color` (básico) já carregado pela classe | `\PassOptionsToPackage{dvipsnames,table}{xcolor}` antes do `soul` |

---

## Lições Aprendidas

- `\DIFdelbegin` pode aparecer tanto no início de linha (blocos de parágrafo) quanto inline no meio de frases
- `\providecommand{}{}` é causado pelos marcadores `\DIFaddbegin`/`\DIFdelbegin` sendo removidos do argumento de `\providecommand`
- Regex `\\DIF...` com `.replace()` pode corromper `\providecommand{\DIFdelFL}` — usar remoção de linha inteira
- Remoção genérica de `}` é **perigosa** — pode corromper `\usepackage{inputenc}`
- Usar `utf-8-sig` para leitura (remove BOM) e `utf-8` sem BOM para escrita
- `\colorbox` não serve para destacar parágrafos longos — usar `soul`/`\hl` com `xcolor` pré-carregado
- `soul` + `\textcolor` dentro do mesmo argumento é incompatível — remover `\textcolor` primeiro

---

## Guia de Robustez Avançada

### Parâmetros Úteis

| Parâmetro | Quando usar |
|-----------|-------------|
| `--flatten` | Documento com `\input` ou `\include` — expande tudo em um único `.tex` |
| `--math-markup=0` | Evita erros em ambientes matemáticos (`align`, `equation`, etc.) — **já usado** |
| `--allow-spaces` | Tolera espaços em nomes de ambientes — **já usado** |
| `--packages=none` | Erros misteriosos ligados a pacotes — desativa análise automática do preâmbulo |

### Erros Comuns e Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Caracteres invisíveis (`^M`) | CRLF vs LF — arquivo gerado com terminadores Windows | Converter para LF: `dos2unix arquivo.tex` |
| Erros em ambientes matemáticos | latexdiff insere marcações dentro de `align`, `equation`, etc. | Usar `--math-markup=0` |
| Erros em ambientes de figura/tabela | latexdiff insere macros em local "proibido" | Substituir bloco inteiro pela versão final limpa (ver fix-errors.md) |
| Erros misteriosos de pacote | Análise automática do preâmbulo falhou | Usar `--packages=none` |

---

### Fluxo à Prova de Erros (Recomendado)

```powershell
# 1. Limpeza de encoding (se necessário)
dos2unix _v7.tex
dos2unix "docs/reviewPacote-submetido-jun/_v6.tex"

# 2. Expansão (se documento multi-arquivo)
# latexpand _v7.tex > _v7_flat.tex

# 3. Diff (comando padrão deste projeto)
latexdiff --allow-spaces --math-markup=0 `
  "docs/reviewPacote-submetido-jun/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex

# 4. Limpeza do markup
python .github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py latex_build/review_raw.tex latex_build/review_clean.tex

# 5. Compilar (2 passes)
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex

# 6. Verificar erros fatais
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex 2>&1 | Select-String "^\!"
```

> **Projetos complexos (muitos pacotes ou comandos próprios):** `git-latexdiff` costuma ser mais estável que o `latexdiff` puro, pois gerencia melhor caminhos de arquivos e dependências temporárias.

---

### Diagnóstico Visual no VS Code

Se o `review_clean.tex` não compilar após a limpeza:

1. Abra `latex_build/review_clean.tex` no VS Code
2. Localize a linha do erro no log (`^! LaTeX Error: ...`)
3. Use **View → Editor Layout → Split Right** para comparar lado a lado com `_v7.tex`
4. Identifique onde o `latexdiff` inseriu macros em local "proibido" (ex: dentro de argumento obrigatório de comando customizado)
5. Consulte `.github/skills/latexdiff-review-pdf/references/fix-errors.md` para o fix correspondente
