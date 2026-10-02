# 1. Jacob 
De imediato, me chamou a atenção que a discriminação entre real e sintético
foi 67%, ou seja, isto signifca que os experts conseguem 'ver' que as imagens
são sintéticas ? Ou trata-se do contrário, e os experts confundem imagens
sintéticas como reais na maioria das vezes ?


# 2. Luciano
sim,conseguem ver em algumas amostras, overall discrimination accuracy was 63.7%
se fosse 50% seria totalmente aleatório e indistinguível. Tipo em 10 acertam 5. No experimento de 10 acertam 6,3 se era real ou se era sintético, numa proporção semelhante de acerto para real e sintético.
No experimento cego houve essa capacidade de discriminação um pouco maior que o aleatorio, que não permite dizer totalmente indistinguiveis, então 
The original claim of "virtually indistinguishable" was moderated to "sufficiently realistic to challenge expert discrimination"

# 3. Jacob
Vamos ver se eu estou entendendo direitinho :
Tu usou teste de hipóteses para saber se os dados são muito distantes da
aleatoriedade. O objetivo principal é calcular um p-valor: se ele for muito
baixo (geralmente menor que 0,05), tu rejeita a hipótese de que os dados são
aleatórios, provando que existe um padrão, tendência ou agrupamento oculto.
É isto ?
Neste caso, como o p-valor << 0.05 existe um padrão, e os dados
real/sintético tem tendência a serem discriminados.
É isto ?
Se for isto, em ponto forte argumentaríamos a favor do método como apoio ao
treinamento de sistemas ?
Outro ponto, na Table 1 a soma das probabilidades nas linhas > 100%; mas se
uma amostra não for real será sintética, e a soma das classificações deve ser
100% ...
Também não entendi, pois não ficou claro no texto, como foi medido o F1 score
na segmentação.
O que seria legal mostrar : 1) que os erros de discriminação entre real e
sintético são quase aleatórios (se for possível testar, aceita a hipótese
nula de que os erros de discriminação ocorrem da mesma forma em ambas as
direções : sint -> real, real -> sint); 2) que os erros de classificação
manual de pixels pelos experts ocorrem  da mesma forma em ambas as classes
(não tem viés de classificação entre imagens reais e sintéticas, ocorrem
indistintamente nas duas classes, aceita a hipótese nula de erros
indistinguíveis); 3) que o método de síntese ajuda a treinar um classificador
simples (ex: nearest neighbor) de pixels pois leva a um erro de classificação
menor estatisticamente se comparado a classificação sem adição de imagens
sintéticas (rejeita a hipótese nula de erros indistinguíveis).
Seria viável fazer estes testes ?

# 4. Luciano
segue uma parte de minhas anotações do experimento:
a questão do revisor sinaliza que — "The claim that synthetic images are "virtually indistinguishable" from real images should be moderated or supported by a proper blind discrimination experiment. The current expert evaluation measures how experts identify salt regions, but it does not directly test whether experts can distinguish real images from generated ones,"

O experimento anterior com os especialistas media apenas a capacidade dos especialistas identificar regiões de sal;concordância com a ground truth por meio de precisão, recall e F1-score.Não equivale a um experimento de discriminação cega entre imagens reais e sintéticas.
Portanto, a observação do revisor é válida: a frase de que as imagens sintéticas são “virtually indistinguishable” fica forte demais se não houver um protocolo específico em que os especialistas: recebam imagens reais e sintéticas misturadas; não saibam a origem de cada imagem;classifiquem cada imagem como real ou sintética;tenham seus acertos analisados contra nível de chance.
Expectativa principal
Em um experimento cego balanceado entre imagens reais e sintéticas:
o avaliador não deveria distinguir consistentemente os dois grupos;
a acurácia esperada deveria ficar próxima de 50%;
sensibilidade e especificidade também tenderiam a valores próximos de 50%.
Interpretação prática
Isso significa:
quando vê uma imagem real, o especialista marca “real” aproximadamente metade das vezes;
Quando vê uma imagem sintética, o especialista marca “synthetic” aproximadamente metade das vezes.
Ou seja, o julgamento fica semelhante a cara ou coroa, o que sustenta a ideia de indistinguibilidade perceptual.
Faixa plausível
Na prática, para dados finitos, não precisa dar exatamente 50%. Um resultado compatível seria algo como:
45%–55%: muito consistente com indistinguibilidade;
40%–60%: ainda pode ser aceitável, dependendo de teste estatístico e tamanho amostral;
acima disso, começa a sugerir discriminação real.
O ponto central não é só a porcentagem bruta, mas se ela é estatisticamente diferente de 50%.
A questão é que o teste reportou 64%, 
Nesta faixa eles estão distinguindo real vs. sintético melhor que o acaso;
a afirmação “virtually indistinguishable” fica inválida ou incosistente;

Dito isso, vamos ao experimento atual

    Jacob "Tu usou teste de hipóteses para saber se os dados são muito distantes da
    aleatoriedade. O objetivo principal é calcular um p-valor: se ele for muito
    baixo (geralmente menor que 0,05), tu rejeita a hipótese de que os dados são
    aleatórios, provando que existe um padrão, tendência ou agrupamento oculto.
    É isto ?"

sim, praticamente é isso.
No blind experiment, o teste era:
H₀: os especialistas classificam real/sintético ao acaso, com acurácia esperada de 50%.
H₁: a acurácia é maior que 50%.
Resultado: 172/270 = 63,7%, resultado do teste p = 0,000004 < 0,05
Como p < 0,05, rejeita-se H₀ de classificação ao acaso .
Portanto, os especialistas distinguiram as imagens melhor que o acaso.
Entretanto,só isso não prova que os dados “não são aleatórios” em sentido geral, nem prova um padrão oculto; apenas mostra que a classificação apresentou desempenho acima de 50%.Também é importante que a ordem das imagens foi embaralhada para evitar efeitos de ordem.E que o teste binomial de p-valor verifica se a acurácia observada é compatível com classificação ao acaso.
Assim, o resultado indica que as imagens sintéticas desafiaram os especialistas, mas não foram totalmente indistinguíveis. O texto agora afirma de forma moderada que "realistic sufficiently to challenge expert discrimination”

    Jacob "Neste caso, como o p-valor << 0.05 existe um padrão, e os dados
    real/sintético tem tendência a serem discriminados."
R: Exato, discriminados acima do acaso. Também não é uma discriminação tão forte a ponto de anular o trabalho. 64% significa que a discriminação está acima do acaso, mas longe de ser perfeita — os especialistas cometem 1 erro a cada 3 imagens.
Isso é favorável ao argumento do paper: as imagens sintéticas de sal são suficientemente realistas para confundir especialistas uma parcela relevante do tempo (35,6% de erro).

    Jacob "Se for isto, em ponto forte argumentaríamos a favor do método como apoio ao treinamento de sistemas ?"

Sim, exatamente, concordo. Esse é provavelmente um argumento mais forte e aplicado do que afirmar que as imagens são indistinguíveis.
O resultado do experimento downstream mostra que as imagens sintéticas não servem apenas para parecer realistas: quando usadas junto às imagens reais, elas melhoraram o treinamento do sistema de segmentação:
IoU: 0,4081 para 0,4276;
ganho absoluto: +0,0195;
ganho relativo: aproximadamente +4,8%;
melhoria observada nos três seeds testados.

# 5. Jacob
Parcialmente ok, Luciano.
Além do problema da table 1, não ficou claro no texto como foi medido o F1
score na segmentação. Mas este experimento que relatas está indicando viés. Veja meu segundo email. Os experts confundem imagens reais com sintéticas ? Se sim, o ponto forte a destacar não pode ser este ... Temos que destacar algo em que o método é bom

# 6. Luciano
    Jacob "Outro ponto, na Table 1 a soma das probabilidades nas linhas > 100%; mas se uma amostra não for real será sintética, e a soma das classificações deve ser
    100% ... "

Na table 1 ,Evaluator Acc. real (%)  Acc. synth. (%) Overall acc. (%), são os acertos de cada avaliador divididos por tipo de amostras reais e amostra sintéticas para ver se haveria um desbalanceamento, mas não houve. Ambos os tipos ficaram próximos à média de 64% de acerto . Então, a soma não seria 100% mesmo, é o valor de acerto no tipo real e sintético.

    O F1-score é calculado a partir da comparação entre a máscara marcada pelo especialista e a máscara de referência.a definição detalhada está na seção Evaluation Measures (o parágrafo cita {Powers2011}) considerando cada pixel  

    Jacob:""O que seria legal mostrar : 1) que os erros de discriminação entre real e
    sintético são quase aleatórios (se for possível testar, aceita a hipótese
    nula de que os erros de discriminação ocorrem da mesma forma em ambas as
    direções : sint -> real, real -> sint); 2) que os erros de classificação
    manual de pixels pelos experts ocorrem  da mesma forma em ambas as classes
    (não tem viés de classificação entre imagens reais e sintéticas, ocorrem
    indistintamente nas duas classes, aceita a hipótese nula de erros
    indistinguíveis); 3) que o método de síntese ajuda a treinar um classificador
    simples (ex: nearest neighbor) de pixels pois leva a um erro de classificação
    menor estatisticamente se comparado a classificação sem adição de imagens
    sintéticas (rejeita a hipótese nula de erros indistinguíveis).
    Seria viável fazer estes testes ?"

    Luciano: 1) é que os erros de classificação foram aproximadamente simétricos entre imagens reais e sintéticas, indicando ausência de forte viés de classe; contudo, a acurácia acima do acaso mostra que a discriminação não foi aleatória.
    2) Os dados mostram:
    Erros em imagens reais: 37,0%;
    Erros em imagens sintéticas: 35,6%;
    Diferença: apenas 1,4 ponto percentual.
    Isso sugere simetria, sem evidência aparente de viés em favor de uma classe. Porém, não é a mesma coisa que  aceitar a hipótese nula. Talvez seja mais adequado dizer que não rejeitamos a hipótese nula de que as taxas de erro são iguais, dentro do poder estatístico deste experimento.
    Há dois fenômenos: Classificação da imagem: o especialista errou ao dizer se a imagem era real ou sintética.
    Segmentação manual de pixels: o especialista errou ao marcar os pixels pertencentes ao sal, avaliada pelo F1-score.
    Os percentuais 37,0% e 35,6% referem-se à classificação real/sintética, não diretamente aos erros de segmentação dos pixels.
    3) seria necessário um novo experimento com os especialistas, pois o experimento blind atual não permite concluir isso, porque ele mede a capacidade dos especialistas de distinguir imagens, não o desempenho de um classificador treinado com imagens sintéticas.Acho pouco viável repetir novo experimento pela agenda disponível dos especialistas. Precisaria mais um mês para convencer e reunir eles um a um. Mas podemos conversar 

# 7. Jacob
Temos um trabalho interessante, só precisamos ajustar a apresentação para que
seja clara e convincente.
Acho que estou entendendo melhor os teus argumentos. São de fato très tipos
de avaliações: 1) discriminação visual sintético/real para mostrar que as
sintéticas tem conteúdo similar com as reais; 2) acerto nas segmentações
visuais em imgs sintéticas e reais para mostrar que do ponto de vista do
expert as sintéticas mostram variações de casos similares o suficiente com as
imgs reais; e 3) melhoria da segmentação automatizada com a inclusão das imgs
sintéticas no dataset. O objetivo final é enriquecer o dataset para treinar
métodos para segmentar imgs reais.
no sumario simplesmente soma-se as avaliações. A partir daí pode-se estimar
taxa de acerto global (sintetico/sintetivo e real/real), taxa de erro global
(sintetico/real e real/sintetico), e verificar o viés de interpretação. Acho
que tem teste estatístico para avaliar se o viés é muito relevante ...
Sobre a segmentação manual, F1-score ajuda :
Em segmentação de imagens, o F1-score indica o grau de sobreposição e
alinhamento exato entre a máscara prevista pelo modelo e a máscara real
(ground truth), calculada a nível de pixel. Ele é matematicamente equivalente
ao Coeficiente de Similaridade de Dice (DSC), que é uma das métricas mais
importantes na visão computacional. O F1-score varia de 0 a 1 (ou 0% a 100%),
onde 1 representa uma segmentação perfeita e 0 indica que não há nenhuma
sobreposição entre o que o modelo previu e a realidade.
Acho que não precisa reunir os experts de novo, basta usar os dados que eles
já geraram. Tu tens os positivos, falsos positivos, negativos e falsos
negativos; tens as máscaras geradas pelos experts e as reais; é possível
construir uma análise similar por tabelas como feito acima - objetivo:
mostrar que os acertos e erros da segmentação visual manual são distribuídos
de forma similar nas sintéticas e nas reais, pois isto suporta a tese de
enriquecer o treino com dados úteis de casos realistas, como uma forma de
ajudar o treino a ver mais casos.
Mas se tiveres outra sugestão, estou disposto a ouvir ... O importante é
montarmos bem o caso pois só temos direito a 1 único review.
Sobre a melhoria na taxa de acerto da segmentação após enriquecer a base de
treino, o que podemos dizer ? É viável dizer algo ?

# 8. Luciano
ótimo, de acordo
tenho um gráfico de matriz de confusão, vou trabalhar nisso já 
grafico ajustado e enviado

# 9. Jacob
Muito bom, Luciano !
Como respondemos as outras questões abaixo ?
2) acerto nas segmentações visuais em imgs sintéticas e reais para mostrar que do ponto de vista do expert as sintéticas mostram variações de casos similares o suficiente com as imgs reais; e
3) melhoria da segmentação automatizada com a inclusão das imgs sintéticas no dataset.

Jacob

# 10. Luciano
 estou terminando as questões 2 e 3. Essas foram ótimas sugestões, mas um pouco mais delicadas. Estou revisando a consistência do documento
