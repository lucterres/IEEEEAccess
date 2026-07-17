# 📋 Comentários dos Revisores ao Autor

---

## 🔵 Revisor 1

### 💬 Comentários

> Este artigo apresenta um método prático e eficaz para sintetizar imagens sísmicas realistas de domos de sal usando um VAE para geração de máscaras e síntese de textura orientada ao contexto. A avaliação por especialistas e as comparações quantitativas são convincentes. No entanto, alguns pontos importantes precisam de esclarecimento ou revisão menor.

### ⚠️ Revisões Obrigatórias Principais

#### 1. 🔍 Comparação com Henriques et al.
O trabalho relacionado menciona a abordagem deles, mas não articula claramente a novidade técnica do seu método.
Por favor, declare explicitamente as principais diferenças de arquitetura e por que sua estratégia de síntese de textura é vantajosa em relação ao modelo generativo deles.

#### 2. 🧠 Detalhes de implementação do VAE
A arquitetura é descrita apenas como camadas densas empilhadas. Por favor, especifique o número de neurônios por camada, a dimensão latente d, os hiperparâmetros de treinamento e se camadas convolucionais foram utilizadas (e por quê).

#### 3. 👥 Design da avaliação por especialistas
Não está claro se os especialistas foram cegados quanto à distinção real/sintético. Se não, por favor reconheça isso como uma limitação.
Também esclareça se imagens reais e sintéticas foram misturadas durante a avaliação.

#### 4. 📊 Significância estatística para DSSIM
A melhoria no DSSIM é pequena (~2,2%). Por favor, adicione um teste estatístico (e.g., Wilcoxon) para confirmar a significância, ou discuta o resultado de forma transparente destacando os ganhos em MSE e LBP.

### ❓ Perguntas Adicionais

> Por favor, confirme que revisou todos os arquivos relevantes, incluindo arquivos suplementares e quaisquer arquivos de resposta do autor, que podem ser encontrados no link "Ver Resposta do Autor" acima (as respostas do autor só aparecerão para resubmissões): Sim, todos os arquivos foram revisados.

- **1) O artigo contribui para o corpo de conhecimento?:** Sim.
- **2) O artigo é tecnicamente sólido?:** Sim.
- **3) O assunto é apresentado de forma abrangente?:** Sim.
- **4) As referências fornecidas são aplicáveis e suficientes?:** Sim.
- **5) Há referências inadequadas para o tópico discutido?:** Não.
- **5a) Se sim, indique quais referências devem ser removidas.:**

---

## 🟠 Revisor 2

### 💬 Comentários

> O manuscrito propõe um framework de síntese de imagens sísmicas orientado ao contexto para geração de imagens rotuladas de domos de sal. A ideia de combinar máscaras de sal geradas por VAE com síntese de textura específica por zona é relevante e potencialmente valiosa para interpretação sísmica e aumento de dados. O artigo é geralmente bem motivado, e o uso de avaliação por especialistas juntamente com métricas quantitativas de similaridade de imagem é um ponto de partida útil.
>
> No entanto, vários problemas importantes devem ser abordados antes que o trabalho possa ser considerado maduro o suficiente para publicação.

### ⚠️ Problemas a Resolver

- 🔬 **Experimento de segmentação downstream** — O manuscrito deve incluir um experimento de segmentação downstream. Como a motivação central é gerar dados rotulados sintéticos para treinar modelos de aprendizado de máquina, é necessário demonstrar que os dados sintéticos propostos melhoram o desempenho de segmentação em dados sísmicos reais de teste. Uma comparação entre treinamento apenas com dados reais e treinamento com dados reais mais sintéticos fortaleceria significativamente o artigo.

- 🧪 **Experimento de discriminação cega** — A afirmação de que imagens sintéticas são "virtualmente indistinguíveis" de imagens reais deve ser moderada ou suportada por um experimento de discriminação cega adequado. A avaliação atual por especialistas mede como os especialistas identificam regiões de sal, mas não testa diretamente se os especialistas conseguem distinguir imagens reais das geradas.

- 📚 **Comparação expandida com baselines** — A comparação com métodos existentes deve ser expandida. O manuscrito compara principalmente com Ferreira et al., mas baselines generativos mais fortes ou recentes, como métodos baseados em GAN, GAN condicional, difusão ou difusão condicional para síntese de imagens sísmicas, devem ser considerados.

- 🗂️ **Configuração experimental mais clara** — A configuração experimental precisa de explicação mais clara. Em particular, os resultados quantitativos na Tabela 3 e o estudo de ablação parecem usar faixas numéricas diferentes e possivelmente conjuntos de dados ou protocolos distintos. Os autores devem esclarecer os conjuntos de dados, tamanhos de amostra, pré-processamento, normalização e procedimentos de avaliação usados em cada experimento.

- 🔁 **Reprodutibilidade** — O artigo deve melhorar a reprodutibilidade. Detalhes importantes de implementação estão ausentes, incluindo dimensão latente do VAE, épocas de treinamento, otimizador, taxa de aprendizado, configurações de perda, tamanho do patch, largura de dilatação de bordas, construção do banco de texturas e parâmetros de amostragem. Esses detalhes são essenciais para leitores que desejam reproduzir ou estender o trabalho.

> No geral, o manuscrito tem uma ideia promissora e aborda um problema de aplicação significativo, mas revisões substanciais são necessárias para fortalecer a validação experimental, melhorar o rigor das afirmações e esclarecer a metodologia.

### ❓ Perguntas Adicionais

> Por favor, confirme que revisou todos os arquivos relevantes, incluindo arquivos suplementares e quaisquer arquivos de resposta do autor, que podem ser encontrados no link "Ver Resposta do Autor" acima (as respostas do autor só aparecerão para resubmissões): Sim, todos os arquivos foram revisados.

- **1) O artigo contribui para o corpo de conhecimento?:** Sim, o artigo faz uma contribuição moderada ao propor um método de síntese de imagens sísmicas orientado ao contexto combinando geração de máscaras de sal baseada em VAE e síntese de textura específica por zona. No entanto, a contribuição deve ser fortalecida demonstrando a utilidade das imagens geradas em tarefas de segmentação downstream.

- **2) O artigo é tecnicamente sólido?:** Parcialmente. O framework proposto é tecnicamente razoável, mas o manuscrito carece de detalhes importantes de implementação, comparações com baselines mais fortes e validação em tarefa downstream. Alguns resultados experimentais também requerem explicação mais clara.

- **3) O assunto é apresentado de forma abrangente?:** Parcialmente. O artigo apresenta a motivação, o método e os experimentos de forma geralmente clara, mas a cobertura de métodos generativos recentes e a discussão sobre a eficácia prática do aumento de dados são insuficientes.

- **4) As referências fornecidas são aplicáveis e suficientes?:** Parcialmente. As referências são aplicáveis ao tópico, especialmente aquelas relacionadas à síntese de imagens sísmicas, aumento de dados, VAE, síntese de textura e avaliação de similaridade de imagens. No entanto, não são totalmente suficientes. O manuscrito deve incluir referências mais recentes e mais fortes sobre geração de imagens sísmicas baseada em GAN e difusão, e a comparação com trabalhos anteriores deve ser expandida além de um único baseline principal.

- **5) Há referências inadequadas para o tópico discutido?:** Não.

- **5a) Se sim, indique quais referências devem ser removidas.:**

---

📧 Em caso de dúvidas, entre em contato com a administradora do artigo: Sra. Sweta Satapathy s.satapathy@ieee.org

### 🔗 Links

- [IEEE Access](https://ieee.atyponrex.com/journal/ieee-access)
