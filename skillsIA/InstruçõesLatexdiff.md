# Instruções: Geração do PDF de Review com Latexdiff

## Objetivo
Gerar um PDF com markup visual de mudanças (deletções em vermelho strikethrough, adições em azul underline) comparando duas versões do manuscrito `_v6.tex` usando `latexdiff` e `pdflatex`.

## Receita Completa (Passo a Passo)

### 1. Preparação

```powershell
cd "d:\0Code\_phdSeismic\IEEE_Access"
```

Certifique-se de que:
- `_v6.tex` (versão atual) está na raiz do repositório
- Git está configurado e o repositório está atualizado
- `latexdiff` está instalado (geralmente via `latexmk` ou MiKTeX)
- `pdflatex` está disponível no PATH

### 2. Identificar Commits para Comparação

Para escolher qual versão anterior usar como base, verifique o histórico:

```powershell
git log --oneline --decorate -10
```

Exemplo de saída esperada:
```
dabf4d5 (HEAD -> fb-compareF3base) resultados
463b2ca (origin/fb-compareF3base) Atualizar a descrição metodológica...
419c68f (origin/main, origin/HEAD, main) versão portugues best performing
...
```

**Recomendação**: Use o commit mais antigo relevante (neste projeto, `419c68f...`) como base para capturar o máximo de mudanças.

### 3. Exportar Versões para Comparação

```powershell
# Exporta a versão do commit base para um arquivo temporário
git show 419c68f3773d0e976da103ded42749a86a520491:_v6.tex > _v6_base.tex

# Copia a versão atual (HEAD) para referência
Copy-Item _v6.tex _v6_current.tex
```

### 4. Gerar o Arquivo de Diff com Latexdiff

```powershell
# Gera review.tex com markup de diff
latexdiff --math-markup=0 --append-textcmd="PARstart" _v6_base.tex _v6.tex > review.tex
```

**Flags explicadas**:
- `--math-markup=0`: Desabilita marcação em ambientes math para evitar conflicts
- `--append-textcmd="PARstart"`: Trata `\PARstart` como comando texto seguro

### 5. Identificar e Corrigir Erros Estruturais

Execute a primeira compilação para identificar problemas:

```powershell
pdflatex -interaction=nonstopmode review.tex > review_build1.log 2>&1

# Verifique os erros
Select-String "^!" review_build1.log | Select-Object -First 20
```

#### Erros Comuns Encontrados:

**Erro 1: DIFdel em listas fragmentadas**
```
! Argument of \DIFdel has an extra }.
! Paragraph ended before \DIFdel was complete.
```

**Causa**: O latexdiff marca cada `\item` individualmente em listas deletadas:
```latex
\begin{itemize}%DIFAUXCMD
\item%DIFAUXCMD
\textbf{\DIFdel{Type A}}%DIFAUXCMD
\DIFdel{: Basic contour...}
...
```

**Workaround**: Substitua toda a lista por um comentário consolidado:
```latex
% Sketch types A-E (deleted in this revision)
```

**Erro 2: DIFdelFL em tabelas multicoluna**
```
! Argument of \DIFdelFL has an extra }.
! Missing } inserted.
! Extra }, or forgotten \endgroup.
```

**Causa**: Tabelas com muitas colunas deletadas geram DIFdelFL fragmentados e mal aninhados.

**Workaround**: Reescreva a tabela inteira de forma limpa removendo todas as marcações latexdiff:
```latex
\begin{table}[htbp]
    \centering
    \caption{Quantitative comparison on the F3 dataset (median values; lower is better).}
    \label{tab:metricsSummary}
    \begin{tabular}{lccc}
        \toprule
        \textbf{Method} & \textbf{MSE} & \textbf{DSSIM} & \textbf{LBP Distance} \\
        \midrule
        Ferreira \emph{et al.}~\cite{Ferreira2020} & 4712.1 & 0.39 & 0.17 \\
        Proposed method & 2037.88 & 0.1537 & 0.0283 \\
        \bottomrule
    \end{tabular}
\end{table}
```

### 6. Aplicar Correções Estruturais

Identifique as linhas problemáticas nos logs e corrija manualmente no `review.tex` usando `replace_string_in_file` ou editores de texto.

**Checklist de áreas críticas a revisar**:
- [ ] Listas deletadas (`\begin{itemize}` e `\begin{enumerate}`)
- [ ] Parágrafos deletados que envolvem quebras de linha
- [ ] Tabelas com muitas colunas (> 4 colunas)
- [ ] Múltiplos `\DIFdel{` aninhados consecutivos

### 7. Compilar com Dois Passes

A compilação em dois passes garante que referências cruzadas e citações sejam resolvidas corretamente:

```powershell
# Primeira passagem
pdflatex -interaction=nonstopmode review.tex > review_build1.log 2>&1

# Segunda passagem (importante!)
pdflatex -interaction=nonstopmode review.tex > review_build2.log 2>&1

# Verifica se o PDF foi gerado
if (Test-Path review.pdf) {
    Write-Host "✓ review.pdf gerado com sucesso"
    Get-Item review.pdf | Select-Object Name,Length,LastWriteTime
} else {
    Write-Host "✗ Falha na geração do PDF"
    Select-String "^!" review_build2.log | Select-Object -First 10
}
```

### 8. Validar o PDF

Abra o `review.pdf` em um visualizador de PDF e verifique:
- [ ] Deletções aparecem em **vermelho com strikethrough**
- [ ] Adições aparecem em **azul com underline**
- [ ] Não há páginas em branco ou truncadas
- [ ] Citações e referências estão resolvidas (não aparecem `??`)
- [ ] Tabelas e figuras estão renderizadas corretamente

### 9. Limpeza

Remova arquivos temporários:

```powershell
Remove-Item _v6_base.tex, _v6_current.tex -ErrorAction SilentlyContinue
```

## Script Completo (Copy-Paste Ready)

```powershell
# 1. Navegar para o diretório
cd "d:\0Code\_phdSeismic\IEEE_Access"

# 2. Exportar versões
git show 419c68f3773d0e976da103ded42749a86a520491:_v6.tex > _v6_base.tex

# 3. Gerar diff
latexdiff --math-markup=0 --append-textcmd="PARstart" _v6_base.tex _v6.tex > review.tex

# 4. IMPORTANTE: Inspecionar erros ANTES da compilação (veja seção 5 acima)
pdflatex -interaction=nonstopmode review.tex > review_build1_check.log 2>&1
Select-String "^!" review_build1_check.log | Select-Object -First 20

# 5. Após CORRIGIR erros manualmente no review.tex, compilar
pdflatex -interaction=nonstopmode review.tex > review_build1.log 2>&1
pdflatex -interaction=nonstopmode review.tex > review_build2.log 2>&1

# 6. Validar
if (Test-Path review.pdf) {
    Write-Host "✓ Sucesso!"
    Get-Item review.pdf | Select-Object Length,LastWriteTime
}

# 7. Limpar
Remove-Item _v6_base.tex -ErrorAction SilentlyContinue
```

## Troubleshooting

### P: Ainda tenho erros "Argument of \DIFdel" após as correções?

**R**: Procure por padrões dentro do `review.tex`:
```
\DIFdel{\begin{
\DIFdel{\\
```

Substitua-os por comentários consolidados.

### P: O PDF foi gerado mas está truncado (menos páginas que esperado)?

**R**: Geralmente indica que a compilação parou em erro silencioso. Verifique:
```powershell
Get-Content review_build2.log | Select-String "^!" | Measure-Object -Line
```

Se houver erros, corrija-os e recompile.

### P: Citações aparecem como "??" no PDF?

**R**: Isso é normal após a primeira passagem. A segunda passagem deve resolvê-las. Se persistir, verifique se `\bibitem` está correto no manuscrito.

### P: Quais flags latexdiff usar?

**Recomendado para este repositório**:
```
latexdiff --math-markup=0 --append-textcmd="PARstart" <old> <new>
```

**Alternativas**:
- `--disable-citation-markup`: Desabilita marcação em citações (pode ajudar com `\cite{}`)
- `-t PREAMBLE`: Usa template customizado (avançado)

### P: Como gerar diff entre dois commits diferentes?

```powershell
git show <COMMIT1>:_v6.tex > old.tex
git show <COMMIT2>:_v6.tex > new.tex
latexdiff --math-markup=0 --append-textcmd="PARstart" old.tex new.tex > review.tex
```

## Exemplo Real de Correção

Nesta sessão, a estrutura de lista deletada original era:

```latex
\begin{itemize}%DIFAUXCMD
%DIFDELCMD <     \item %%%
\item%DIFAUXCMD
\textbf{\DIFdel{Type A}}%DIFAUXCMD
\DIFdel{: Basic contour...}
...
```

Corrigida para:

```latex
% Sketch types A-E removed in this revision
```

**Impacto**: 
- Eliminado ~50 linhas de markup inválido
- Reduzido de ~20 erros para 0 erros de LaTeX

## Métricas de Sucesso

✅ **Esperado no PDF final**:
- 14+ páginas (dependendo do tamanho do documento)
- ~2.4 MB de tamanho
- Sem avisos "Undefined reference"
- Texto vermelho com strikethrough para deleções
- Texto azul com underline para adições

## Referências

- [Latexdiff Manual](http://www.ctan.org/pkg/latexdiff)
- [pdfTeX Documentation](https://www.tug.org/applications/pdftex/)
- [IEEE Access LaTeX Guidelines](../docs/IEEE_Access_Figure_Guidelines.md)
