# Instruções: Gerar PDF com Diferenças entre Versões (latexdiff)

> Atualizado: 2026-07-13  
> Contexto: diff entre `_v6.tex` (submetido) e `_v7.tex` (revisado)  
> Requisito IEEE Access: submeter "Highlighted PDF" com mudanças marcadas  
> **Status: ✅ Processo testado e funcional — gera `latex_build/review_clean.pdf`**

---

## 📚 Documentação Integrada

Este processo está documentado de forma integrada em dois locais:

| Local | Conteúdo |
|-------|----------|
| **`.github/skills/latexdiff-review-pdf/SKILL.md`** | Skill para VS Code — invoca este workflow automaticamente |
| **`.github/skills/latexdiff-review-pdf/references/fix-errors.md`** | Catálogo completo: 9 erros comuns + fixes de latexdiff |
| **`docs/InstrucoesLatexdiff.md`** (este arquivo) | Workflow completo com passo-a-passo e detalhes técnicos |
| **`docs/latexdiff_cleanup.py`** | Implementação Python (9 passos de limpeza) |

> **Para resolver erros latexdiff não-óbvios**, consulte `.github/skills/latexdiff-review-pdf/references/fix-errors.md`

---

## Arquivos de Referência

| Papel | Arquivo |
|-------|---------|
| Versão OLD (submetida) | `docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex` |
| Versão NEW (revisada)  | `_v7.tex` |
| Script de limpeza      | `docs/latexdiff_cleanup.py` |
| PDF diff (saída final) | `latex_build/review_clean.pdf` |

---

## Passo a Passo (Processo Completo)

Execute os 3 comandos abaixo a partir da raiz do repositório:

### 1. Gerar o `.tex` de diferenças

```powershell
latexdiff --allow-spaces --math-markup=0 `
  "docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex
```

### 2. Limpar o arquivo gerado

```powershell
python docs/latexdiff_cleanup.py latex_build/review_raw.tex latex_build/review_clean.tex
```

O script deve reportar:
```
DIFdelbegin left (start-of-line): 0
textbf{} empty left:  0
providecommand{} empty: 0
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

## O que o Script de Limpeza Faz

O `latexdiff_cleanup.py` aplica as seguintes transformações em ordem:

| Passo | Ação |
|-------|------|
| 1a | Remove blocos `\DIFdelbegin ... \DIFdelend` completos (início de linha) |
| 1b | Remove `\DIFdelbegin...\DIFdelend` inline (mid-paragraph) |
| 1c | Remove marcadores DIF standalone (`\DIFdelend`, `\DIFaddbegin`, etc.) |
| 2  | Remove linhas `\DIFaddbegin` / `\DIFaddend` (mantém conteúdo) |
| 3  | Desembrulha `\DIFadd{texto}` → `texto` (até 3 níveis de aninhamento) |
| 4  | Remove `\DIFdel{...}` remanescentes |
| 5  | Remove `\providecommand{}{}` do preâmbulo |
| 6  | Corrige `\lstset{extendedchars=\true}` → `extendedchars=true` |
| 7  | Remove linhas de comentários `%DIFDELCMD`, `%DIFAUXCMD`, `%DIF ...` |
| 8  | Remove linhas `\providecommand{\DIFxxxFL}` completas; limpa `\DIFxxxFL` |
| 8b | Segunda passagem de remoção de `\providecommand{}{}` |
| 8c | Remove `\end{comment}` órfãos |
| 8d | Correção cirúrgica: texto do _v6 que ficou com `}` sobrando |
| 8e | Adiciona `\end{enumerate}` faltando quando detecta desbalanceamento |
| 9  | Remove comandos com argumento vazio (`\textbf{}`, `\emph{}`, etc.) |

---

## Resultado Esperado no PDF

| Marcação | Significado |
|----------|-------------|
| Texto em **azul ondulado** | Conteúdo adicionado na versão `_v7` |
| Texto tachado em **vermelho** | Conteúdo removido da versão `_v6` |

> ⚠️ A classe `ieeeaccess` redefine algumas cores internamente — se as cores não aparecerem, o conteúdo do diff ainda está correto estruturalmente.

---

## Problemas Conhecidos (Resolvidos)

| Problema | Causa | Solução no script |
|----------|-------|-------------------|
| `\providecommand{}{}` no preâmbulo | latexdiff insere definições de DIFaddbegin/end que ficam vazias | `.replace()` literal em loop |
| `\lstset{extendedchars=\true}` | latexdiff gera `\true` inválido | substituição direta |
| `\textbf{}` vazios | conteúdo deletado dentro de `\textbf{}` | regex de comandos com `{}` vazio |
| `\end{comment}` órfão | `\begin{comment}` estava dentro de bloco deletado | contagem e remoção do excesso |
| `}` sobrando + texto do _v6 | bloco DIFdelbegin não fechado corretamente pela marcação inline | correção cirúrgica por string literal |
| `\begin{enumerate}` sem `\end` | latexdiff truncou o bloco | inserção do `\end{enumerate}` faltando |
| DIFdelbegin inline (mid-paragraph) | latexdiff insere marcadores dentro de parágrafos | regex DOTALL para remover blocos inline |

---

## Lições Aprendidas (2026-07-13)

- O `latexdiff` processa `\begin{comment}` como LaTeX normal — os blocos dentro são marcados como deletados
- `\DIFdelbegin` pode aparecer tanto no início de linha (blocos de parágrafo) quanto inline no meio de frases
- `\providecommand{}{}` é causado pelos marcadores `\DIFaddbegin`/`\DIFdelbegin` sendo removidos do argumento de `\providecommand`
- Regex `\\DIF...` com `.replace()` pode corromper `\providecommand{\DIFdelFL}` — usar remoção de linha inteira
- Remoção genérica de `}` é **perigosa** — pode corromper `\usepackage{inputenc}`
- Usar `utf-8-sig` para leitura (remove BOM) e `utf-8` sem BOM para escrita

---

## Guia de Robustez Avançada

> O `latexdiff` insere comandos LaTeX (`\DIFadd`, `\DIFdel`) diretamente no código-fonte, o que o torna sensível a estruturas complexas. Quando o arquivo resultante não compila, geralmente é porque o latexdiff "quebrou" um ambiente ou comando delicado.

### Parâmetros Úteis

| Parâmetro | Quando usar |
|-----------|-------------|
| `--flatten` | Documento com `\input` ou `\include` — expande tudo em um único `.tex` |
| `--math-markup=0` | Evita erros em ambientes matemáticos (`align`, `equation`, etc.) — **já usado neste projeto** |
| `--allow-spaces` | Tolera espaços em nomes de ambientes — **já usado neste projeto** |
| `--packages=none` | Erros misteriosos ligados a pacotes — desativa análise automática do preâmbulo |
| `--config` / `-c` | Comandos customizados que o latexdiff está "quebrando" — define como ignorar blocos específicos |

> **Nota sobre `--flatten`:** Se falhar em encontrar imagens ou arquivos em subdiretórios, rode o `latexdiff` dentro da pasta raiz do projeto, ou use `latexpand` para expandir o documento antes de rodar o diff.

---

### Estratégias para Documentos Complexos

**Simplificação do Preâmbulo**
O `latexdiff` tenta ler o preâmbulo. Comandos muito complexos ou condicionais (`\ifx`, etc.) podem confundi-lo. Mantenha o preâmbulo o mais limpo possível nos dois arquivos comparados.

**Divida e Conquiste**
Se o arquivo completo não compila, compare apenas capítulos ou seções individuais. Rode o `latexdiff` em arquivos menores, depois una os resultados ou revise as partes críticas separadamente.

**Use `latexrevise`**
Após gerar o arquivo de diff, use `latexrevise` para remover as marcações de `\DIFdel` e aceitar as mudanças. Útil para "limpar" o arquivo e verificar se a estrutura final está correta.

---

### Erros Comuns e Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Caracteres invisíveis (`^M`) | CRLF vs LF — arquivo gerado com terminadores Windows | Converter para LF: `dos2unix arquivo.tex` |
| Erros em ambientes matemáticos | `latexdiff` insere marcações dentro de `align`, `equation`, etc. | Usar `--math-markup=0` |
| Erros em ambientes de figura/tabela | `latexdiff` insere macros em local "proibido" | Substituir bloco inteiro pela versão final limpa (ver fix-errors.md) |
| Erros misteriosos de pacote | Análise automática do preâmbulo falhou | Usar `--packages=none` |
| Parser confuso por comentários | Mudanças em blocos de comentários grandes | Remover comentários desnecessários antes de comparar |

---

### Fluxo à Prova de Erros (Recomendado)

```powershell
# 1. Limpeza de encoding (se necessário)
dos2unix _v7.tex
dos2unix "docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex"

# 2. Expansão (se documento multi-arquivo)
# latexpand _v7.tex > _v7_flat.tex

# 3. Diff (comando padrão deste projeto)
latexdiff --allow-spaces --math-markup=0 `
  "docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex

# 4. Limpeza do markup
python docs/latexdiff_cleanup.py latex_build/review_raw.tex latex_build/review_clean.tex

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
