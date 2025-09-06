# 1.1. Módulo Design Sprint

Usando a lista de projetos indicados por grupo para o período letivo vigente, realizar Design Sprint para levantamento dos requisitos.

## Estrutura do Design Sprint

### Compreender (Unpack)
No contexto de desenvolvimento de uma nova solução ou projeto, faz-se necessário executar um planejamento, tal como a compreensão do domínio em que esse projeto está inserido, suas possíveis problemáticas, hipóteses e certezas. Dentre diversas propostas de metodologia para executar essa etapa, pode-se destacar a Design Sprint — desenvolvida pela Google Ventures — mais especificamente a etapa Unpack, ou traduzido, “Desempacotar“. Assim, este documento tem como objetivo apresentar o artefato documental resultante da fase Unpack da Design Sprint. Nesta etapa, a equipe mergulha no problema central do projeto, buscando compreender o contexto, as causas e os desafios relacionados ao universo ao qual o projeto está inserido. A motivação para a elaboração deste artefato reside na necessidade de formalizar e centralizar as descobertas, servindo como uma base de conhecimento acessível para toda a equipe e futuras consultas. Além disso, justifica-se a utilização de tal etapa, composta ao contexto da Design Sprint, por sua agilidade; isto é, em um contexto em que tempo e recursos são escassos, metodologias que priorizem a entrega rápida e aloquem seus esforços às expectativas dos stakeholders tendem a ter melhor desempenho e resultados em relação a perspectivas mais orientadas a planos. Portanto, dados tais aspectos alinhados ao contexto do presente projeto, justifica-se a utilização da prática da Design Sprint e, por conseguinte, a fase de abertura da sprint: Unpack.

### Metodologia

A fase Unpack foi conduzida utilizando uma combinação de técnicas de elicitação e análise, adaptadas para a dinâmica da Design Sprint. A técnica central de elicitação foi o Brainstorming, permitindo a geração de uma diversidade de ideias e informações de forma colaborativa. Para documentar e guiar a análise dos problemas identificados, foram empregados alguns artefatos, com destaque para a adaptação da técnica Rose, Thorn, Bud, o Diagrama de Causa-Efeito (Diagrama de Ishikawa) e a metodologia 5W2H. Nesse interim, o Brainstorming ocorreu de forma presencial durante uma aula de dinâmica de grupos proposta na disciplina de Arquitetura e Desenho de software, compondo-se dos integrantes da equipe e da professora Dr.ª Milene Serrano para a dinâmica de geração de ideias. Em mérito material, utilizou-se um Mapa de Ideias (whiteboard e post-its) virtuais utilizando o Miro para organizar e visualizar as informações.

---

#### Rose, Thorn, Bud (Adaptada) {#rose-thorn-bud-execucao}

Adaptamos a técnica Rose, Thorn, Bud para avaliar o contexto inicial. Os elementos originais que compõem essa técnica, são:

- **Rose (Pontos Positivos):** Foram identificados os aspectos que estão funcionando bem e que devem ser mantidos (Nome utilizado).
- **Thorn (Espinhos):** Mapeamos os pontos de fricção, problemas e obstáculos.
- **Bud (Brotos):** Exploramos as oportunidades de crescimento e as ideias promissoras.

Para o contexto da adaptação, foi utilizado o seguintes:

- **Certezas:** No lugar de Rose, foi alocado os aspectos de certezas vinculados ao domínio do projeto, isto é, processos e aspectos de regra de negócio, tal como fatores adjacentes.
- **Brotos:** Se manteve alinhado à proposta de Bud.
- **Problemas:** Apesar de ligeiramente distinto, a ideia ainda é mapear problemas no contexto do projeto.
- **Stakeholders:** Esse foi adicionado, para distinguir dos demais, pois são uma intersecção da classificação certezas e brotos, em mérito de potenciais stakeholders para o desenvolvimento do projeto.

---

### Execução e Resultados
A aplicação das metodologias resultou na identificação de pontos-chave e na obtenção de um entendimento compartilhado sobre o desafio. Abaixo, segue a implementação propriamente das técnicas, seguindo de seus resultados.


### Brainstorming {#brainstorming}

O Brainstorming ocorreu de forma presencial, em uma dinâmica proposta durante a aula de Arquitetura e Desenho de Software. A sessão envolveu a equipe do projeto e a professora para uma sessão de geração de ideias. As ideias foram organizadas e visualizadas em um Mapa de Ideias no Miro, usando um whiteboard virtual e post-its, vinculado ao artefato Rose, Thorn, Bud (técnica Unpack da Google Ventures). Segue abaixo algumas definições do processo, assim como o BPMN dessa parte.

Anexar BPMN do Brainstorming: a ser adicionado.

#### Pré-condições do Brainstorming

1. **Definir Objetivos de Brainstorming:** alinhado à técnica Rose, Thorn, Bud detalhada [acima](#rose-thorn-bud-execucao).

2. **Selecionar participantes:** A partir da lista de Stakeholders, é selecionado os participantes para a dinâmica. Depois, envia-se o pedido de participação para os selecionados que, confirmados, estão aptos à ingressarem na dinâmica. Segue abaixo a lista de participantes presentes nessa etapa:

| Nome                | Papel         |
|---------------------|-------------------------|
| Mateus Villela      | Facilitador/Mediador    |
| Milene Serrano      | Contribuidor  |
|   Paulo Henrique       | Contribuidor           |
| Letícia da Silva        | Contribuidor |
| Henrique Martins     | Contribuidor                |
| Eduardo            | Contribuidor             |
| Daniel Ferreira      | Contribuidor          |
| Breno Alexandre       | Contribuidor           |
| Víctor Moreira      | Contribuidor           |


3. **Seleção do mediador:**  
    [Mateus Villela](https://github.com/MVConsorte) (representante do módulo Base).

4. **Preparação do meio material:** Antes de iniciar, é necessário preparar os materiais para realizar o brainstorming. Nesse contexto, os seguintes materiais foram selecionados:
    - Notebook ou celular para utilização do whiteboard e post-its da ferramenta Miro.
    - Internet: utilizou-se a disponibilizada pela UnB.
    - Seleção da sala para ocorrer a reunião: S7 (UAC - UnB).

### Dinâmica e Resultado

- **Duração da dinâmica:** 30-40 min aproximadamente.
- **"Vez de falar"**: bate-papo intermediado por facilitador, visando equilibrar as vozes de contribuição.
- **Resultado do Whiteboard de mapa de ideias:** 

Imagem do whiteboard do brainstorming: a ser adicionada.

[Melhor visualização](#miro-iframe)

---
### Refinamento do Brainstorming

Com o intuito de agragar na etapa 1 da design sprint, foi utilizado alguns artefatos generalistas, pra melhor desmembrar o universo vinculado ao projeto. Assim, segue abaixo tais artefatos que foram inspirados nos resultados do [Brainstorming](#brainstorming). 

### Diagrama de Causa-Efeito (Diagrama de Ishikawa) {#ancora-ishikawa}

Utilizamos o Diagrama de Causa-Efeito para analisar e identificar as causas-raiz de um dos principais problemas do projeto. A análise revelou diversas categorias de causas, como recursos, pessoas, processos e ferramentas.

![Diagrama de Ishikawa](../../assets/imgs/EspinhadePeixe.jpeg)

---

### Metodologia 5W2H {#ancora-5w2h}

A técnica 5W2H foi aplicada para detalhar as ações e plano de solução, ajudando a esclarecer: What (O quê), Why (Por quê), Where (Onde), When (Quando), Who (Quem), How (Como) e How much (Quanto).

Artefato 5W2H: a ser adicionado.

---

#### Visualização de artefatos no Miro {#miro-iframe}

### Conclusão

A fase Unpack foi fundamental para alinhar a equipe em torno do problema central e construir uma base sólida de conhecimento. A aplicação das técnicas mencionadas, especialmente a adaptação do Rose, Thorn, Bud e a utilização do Diagrama de Ishikawa, permitiu uma visão holística e aprofundada das complexidades do projeto. O uso do Mapa de Ideias se mostrou crucial para a visualização das conexões entre os conceitos, facilitando a identificação de padrões. De um ponto de vista crítico, a riqueza de detalhes e a clareza obtidas nesta fase são proporcionais à qualidade dos insights gerados, o que é um bom indício para o sucesso das próximas etapas da Design Sprint.

### Conclusão

A utilização do Brainstorming, aliada aos artefatos Ishikawa e 5W2H, proporcionou uma análise abrangente e colaborativa do problema. Essa abordagem permitiu identificar pontos críticos e definir ações concretas para o desenvolvimento de soluções eficazes nas etapas seguintes do Design Sprint.

### Referencias Bibliograficas

- KNAPP, Jake; ZERATSKY, John; KOWITZ, Braden. Sprint: O método usado no Google para testar e aplicar novas ideias em apenas cinco dias. Editora Intrínseca, 2016. Acessado em: 03/09. Disponível em: [<vídeo>](https://youtu.be/AuktI4lBj6M?si=Udc8e2jYimjKcQnq).

- PMBOK® Guide – Sexta Edição. Project Management Institute, 2017.

- ISHIKAWA, Kaoru. Introduction to Quality Control. Productivity Press, 1990.

- [GOOGLE. Rose, Thorn, Bud (Adaptado) . Disponível em: https://designsprintkit.withgoogle.com/methodology/phase1-understand/rose-thorn-bud. Acesso em: 5 set. 2025.](https://designsprintkit.withgoogle.com/methodology/phase1-understand/rose-thorn-bud)

- [MINITAB. Diagrama de Causa e Efeito: Visão Geral. Disponível em: https://support.minitab.com/pt-br/minitab/18/help-and-how-to/quality-and-process-improvement/quality-tools/how-to/cause-and-effect-diagram/before-you-start/overview/. Acesso em: 5 set. 2025.](https://support.minitab.com/pt-br/minitab/18/help-and-how-to/quality-and-process-improvement/quality-tools/how-to/cause-and-effect-diagram/before-you-start/overview/)

- [5W2H e Gamificação. . Disponível em: https://github.com/user-attachments/files/22179617/5W2H.e.Gamificacao.pdf. Acesso em: 5 set. 2025.](https://github.com/user-attachments/files/22179617/5W2H.e.Gamificacao.pdf)

- [GV. Sprint. Disponível em: https://www.gv.com/sprint/. Acesso em: 5 set. 2025.](https://www.gv.com/sprint/)

### Histórico de Versão

| Id  | Descrição                                   | Autor         | Revisor      | Data       |
|-----|---------------------------------------------|---------------|--------------|------------|
| 1.0 | Criação inicial do documento                | [Mateus](https://github.com/MVConsorte)     | - | 05/09/2025 |
| 1.1 | Adição de metodologia e artefatos           | [Mateus](https://github.com/MVConsorte)      | - | 05/09/2025 |


## 2. Esboçar (Sketch)

### **Introdução**

Na etapa de esboço (sketch) do Design Sprint, a atenção se volta para converter ideias em representações visuais palpáveis. Depois de compreender o problema, investigar o desafio e buscar referências na fase anterior (entender), avançamos para dar forma gráfica às propostas, mesmo que de maneira simples ou conceitual. O propósito é materializar o pensamento, possibilitando a comparação de diferentes alternativas antes de escolher o caminho definitivo.

### Objetivo da Etapa
O esboço funciona como elo entre conceito e prática. É o momento em que as ideias deixam o campo abstrato e passam a ser visualizadas no papel. Essa representação inicial é essencial para validar suposições, detectar pontos fracos e incentivar a colaboração do time na busca pela solução mais adequada ao desafio.

### Processo
Ao longo do Design Sprint, lidamos com limitações de tempo, o que exigiu dividir as atividades entre os integrantes do grupo, de acordo com as fases do método. Dessa forma, cada participante assumiu responsabilidades específicas, alinhadas às suas competências e ao tempo disponível.

Na fase de esboçar, realizamos uma distribuição planejada das tarefas, garantindo que os aspectos visuais e conceituais mais relevantes do projeto fossem contemplados, sendo parte dessa etapa feita no ambiente da sala de aula, conforme descrito na tabela 1.

<p align="center"><strong>Tabela 1: Distribuição das tarefas durante a etapa de esboçar do Design Sprint</strong></p>

<table style="margin: auto; width: 60%; border-collapse: collapse;" border="1" cellpadding="8">
  <thead>
    <tr>
      <th style="text-align: center;">Membro(s) da Equipe</th>
      <th style="text-align: center;">Tarefa Realizada</th>
      <th style="text-align: center;">Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">Luiz</td>
  <td style="text-align: center;"><a href="../../assets/imgs/MapaMental.png">Mapa mental</a></td>
      <td style="text-align: center;">Estruturou as ideias principais e secundárias do projeto(Feito presencialmente).</td>
    </tr>
    <tr>
      <td style="text-align: center;">Henrique</td>
  <td style="text-align: center;"><a href="../../assets/imgs/RichPicture.jpg">Rich Picture</a></td>
      <td style="text-align: center;">Representou visualmente o fluxo da solução proposta, passo a passo(Feito em reunião).</td>
    </tr>
    <tr>
      <td style="text-align: center;">Paulo, Daniel e Eduardo</td>
  <td style="text-align: center;"><a href="../../assets/imgs/G5_ARQDSW_1.jpg">Diagrama de Causa e Efeito</a></td>
      <td style="text-align: center;">Identificou os principais problemas e suas causas relacionadas(Feito em reunião).</td>
    </tr>
  </tbody>
</table>

<p align="center"><em>Autor: Paulo Cerqueira, 2025.</em></p>

### Histórico de Versão

<div align="center">
    <table>
        <tr>
            <th>Data</th>
            <th>Versão</th>
            <th>Descrição</th>
            <th>Autor</th>
            <th>Data da Revisão</th>
            <th>Revisor</th>
        </tr>
        <tr>
            <td>04/09/2025</td>
            <td>1.0</td>
            <td>Adicionado o esboçar</td>
            <td><a href="https://github.com/paulocerqr">Paulo Cerqueira</a></td>
            <td>05/09/2025</td>
            <td><a href="https://github.com/MVConsorte">Mateus Vilela</a></td>
        </tr>
    </table>
</div>


## 3. Decidir (Decide)

### __Introdução__

A fase de decisão no Design Sprint é crucial, pois marca o momento em que, após reunir informações, definir requisitos e consolidar os artefatos anteriores, é preciso escolher com clareza os próximos passos do projeto. Essa definição evita bloqueios no processo e garante que a metodologia ágil siga em fluxo contínuo, sem interrupções ou retrabalhos desnecessários.

### Objetivo

O propósito desta etapa é registrar como ocorreu a priorização e a escolha dos requisitos mais importantes, bem como indicar quem foram os responsáveis por cada decisão e em qual parte do projeto os documentos resultantes estão armazenados. Dessa forma, cria-se uma visão organizada e transparente sobre as escolhas realizadas.

### Processo

Técnica Utilizada: Rumble or All-In-One

Nesta etapa, aplicamos a técnica Rumble or All-In-One, uma prática comum no Design Sprint para decidir qual solução deve avançar. Essa técnica funciona de duas maneiras:

Rumble: cada equipe ou participante cria uma versão própria da solução, permitindo a comparação entre alternativas diferentes. Depois, avalia-se qual delas tem maior potencial para atender ao desafio.

All-In-One: ao invés de dividir, combina-se as melhores partes das ideias em uma única proposta unificada, que concentra os pontos fortes identificados nas alternativas.

A escolha entre “Rumble” ou “All-In-One” depende do contexto do desafio: se a equipe deseja testar soluções radicalmente distintas, opta-se pelo Rumble; se o objetivo é consolidar forças em uma proposta mais robusta, recorre-se ao All-In-One. Essa abordagem garante decisões mais conscientes e alinhadas às metas do projeto.

### Histórico de Versão

<div align="center">
    <table>
        <tr>
            <th>Data</th>
            <th>Versão</th>
            <th>Descrição</th>
            <th>Autor</th>
            <th>Data da Revisão</th>
            <th>Revisor</th>
        </tr>
        <tr>
            <td>05/09/2025</td>
            <td>1.0</td>
            <td>Criação do documento</td>
            <td><a href="https://github.com/paulocerqr">Paulo Cerqueira</a></td>
            <td>05/09/2025</td>
            <td><a href="https://github.com/MVConsorte">Mateus Vilela</a></td>
        </tr>
    </table>
</div>

## 4. Prototipar (Prototype)

### __Introdução__

A prototipação é uma etapa essencial no desenvolvimento de produtos, especialmente em projetos de software. Consiste na criação de __modelos iniciais__ que simulam funcionalidades e interfaces, permitindo a validação de ideias, identificação de falhas e refinamento de requisitos antes do investimento em desenvolvimento completo. Essa abordagem reduz custos, melhora a comunicação entre equipes e garante maior alinhamento com as expectativas dos usuários.

### __Metodologia__

Optamos por desenvolver um protótipo de alta fidelidade utilizando a plataforma [Figma](https://figma.com), visando proporcionar uma visão clara e interativa do produto final.

Os membros envolvidos na elaboração do protótipo foram:

- Letícia da Silva Monteiro
- Breno Alexandre
- Daniel Ferreira
- Paulo Cerqueira

### __Resultados__

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://embed.figma.com/design/lB8oMh7D1uVZTKp1AudwF0/GRUPO-5--ARQUITETURA?node-id=7-17&embed-host=share" allowfullscreen></iframe>

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://embed.figma.com/design/lB8oMh7D1uVZTKp1AudwF0/GRUPO-5--ARQUITETURA?node-id=92-31&embed-host=share" allowfullscreen></iframe>



# 5. Validação - Design Sprint: Dicas de Estágio

## 1. **Objetivos de Validação**

O objetivo principal da validação é testar o protótipo de alta fidelidade com usuários reais para aprender o que funciona, o que não funciona e como melhorar o produto antes de qualquer desenvolvimento dispendioso.

*   **Objetivos de Aprendizado:**
    *   Validar se a proposta de valor (conectar estudantes a dicas de estágio valiosas) é clara e atraente.
    *   Identificar pontos de atrito no fluxo de navegação e usabilidade da interface.
    *   Coletar feedback sobre a clareza e utilidade.

*   **Métricas de Sucesso Qualitativas:**
    *   **Reação Emocional:** Entusiasmo, confusão ou frustração durante a apresentação do protótipo.
    *   **Intenção de Uso:** Se o usuário expressa desejo de usar o produto no futuro.
    *   **Compreensibilidade:** Se o usuário entende o propósito do app sem explicações prévias.

## 2. **Preparação para a Validação**

### a) Participantes
*   **Perfil Alvo:** Estudantes universitários de qualquer semestre, que estejam ativamente buscando ou realizando estágios.
*   **Quantidade:** Pelo menos 1 usuário.

### b) Protótipo e Ambiente de Teste
*   **Ferramenta de Prototipagem:** Figma.
*   **Estado do Protótipo:** Estático e de alta fidelidade, simulando o visual desejado do produto.
*   **Configuração do Teste:** O teste será realizado presencialmente. A sessão será gravada (com consentimento) para análise posterior.
*   **Checklist de Preparação:**
    *   [X] Link do protótipo.
    *   [X] Guia de roteiro de entrevista revisado.
    *   [X] Termo de consentimento preparado para os participantes.

### c) Termo de consentimento
```
Eu autorizo o uso das respostas fornecidas por mim na entrevista realizada para a matéria Arquitetura e Desenho de Software.
Declaro estar ciente de que:
Minhas respostas poderão ser utilizadas parcial ou integralmente, respeitando o contexto original.
O uso será exclusivamente para os fins informados acima, sem qualquer finalidade comercial indevida.
Tenho direito de solicitar a retirada de minha identificação, caso não queira ser citado(a) nominalmente.
Esta autorização é concedida de forma gratuita e por tempo indeterminado, salvo manifestação em contrário.
Por ser expressão da verdade, firmo o presente termo.

Assinado _____________________________________________

______/_____/_______.
```

## 3. **Roteiro da Sessão de Validação (Script)**

**Duração Total:** 37 minutos por sessão.

| Tempo | Fase | Objetivo | Perguntas/Tarefas Chave | Importância |
| :--- | :--- | :--- | :--- | :--- |
| **2 min** | **Introdução** | Explicar o formato. | "Agradeço por participar. Hoje vamos testar um protótipo de um novo app." | Baixa |
| **5 min** | **Contexto & Hábitos** | Entender o background do usuário. | "Você já buscou informações sobre estágios? Se sim, onde? E como foi sua experiência?"  | Alta |
| **25 min** | **Teste do Protótipo** | Coletar feedback. | **Tarefa 1:** "Com base no protótipo, qual sua opinião sobre o design escolhido?" <br> **Tarefa 2:** "Sobre as funções, quais você acha mais importantes e quais você acha que estão faltando?" | Alta |
| **5 min** | **Debriefing & Encerramento** | Coletar impressões gerais e agradecer. | "No geral, o que você achou? Você usaria um app como esse? Algo que poderia mudar?" | Alta |

## 4. **Papéis e Responsabilidades da Equipe**

*   **Facilitador/Interviewer (1 pessoa):** Conduz a sessão, faz as perguntas e guia o participante. Deve criar um ambiente confortável e neutro.
*   **Reporter/Anotador (1 pessoa):** Responsável por tomar notas detalhadas em tempo real, focando em citações literais e comportamentos observados. Pode usar uma planilha compartilhada.

## 5. **Técnica de Análise de Dados: Mapeamento de Padrões**

Após a sessão, os dados serão revisados pela equipe e usados para ver se os resultados são esperados ou não.

1.  **Compilação de Notas:** A gravação será publicada e adicionada ao Pages.
2.  **Identificação de Padrões:** A equipe busca por:
    *   **Problemas de Usabilidade:** Onde o usuário se frustrou.
    *   **Reações Positivas:** O que os usuários amaram e elogiaram.
    *   **Insights Surpreendentes:** Comportamentos ou feedbacks não antecipados.
3.  **Priorização:** Os problemas são categorizados por **Gravidade** (Bloqueador, Major, Minor).

## 6. **Resultados e Próximos Passos**

[Vídeo da validação com usuário](https://youtu.be/soIByeI9JI4)

Com base na análise, o resultado da validação se enquadrará em uma de três categorias:

| Resultado | Descrição | Ação Recomendada para o Projeto |
| :--- | :--- | :--- |
| **Sucesso** | A maioria das ideias funcionou; o conceito central foi validado. | **Iterar no protótipo:** Ajustar os problemas de usabilidade identificados e prosseguir para o desenvolvimento. |
| **Misto** | Algumas coisas funcionaram, outras falharam criticamente. | **Iterar profundamente:** Manter as soluções que funcionaram e refazer as que falharam. Realizar um novo ciclo de teste focado nas partes problemáticas. |
| **Falha** | O conceito central não foi compreendido ou foi rejeitado pelos usuários. | **Refazer:** Reavaliar a premissa do problema e as suposições iniciais. É um ótimo aprendizado que evitou um grande desperdício de recursos. |

**Decisão Final do Decider:**
*   [X] Prosseguir para desenvolvimento
*   [X] Realizar uma segunda sprint de iteração
*   [ ] Redefinir o escopo e a direção do projeto

**Extras**:
O entrevistado aprovou e gostou da ideia do projeto e deu o aval para prosseguir com a maioria das coisas. Algumas ideias chave já foram implementadas no planejamento de produto final e os elementos de design que foram classificados como "quebrados" já foram comunicados para a modificação, e por isso está marcada a opção de uma segunda sprint, para poder ajustar esses problemas e dialogar sobre possíveis melhorias.


## 7. **Checklist de Validação**

*   [X] Protótipo estático de alta fidelidade finalizado.
*   [X] Roteiro de entrevista aprovado pela equipe.
*   [X] Tecnologia (gravação) testada e funcionando.
*   [X] Sessão realizada e notas detalhadas tomadas.
*   [ ] Reunião de síntese e análise realizada com a equipe de validação.
*   [ ] Relatório de insights e plano de próximos passos definido e acordado com toda a equipe.


---

## **Referências**

*   [GV Design Sprint Guide](https://www.gv.com/sprint/) 
*   [The Product Design Sprint: Validate (Day 5) - GV Library](https://library.gv.com/the-product-design-sprint-validate-day-5-761292b20d05) 
*   [Interaction Design Foundation - Design Sprints](https://www.interaction-design.org/literature/topics/design-sprints) 

## __Histórico de Versão__

| Versão | Alteração                 | Autor(es)      | Revisor(es)   |
| ------ | ------------------------- | -------------- | ------------- |
| 1.0    | Criação do documento      | Paulo Cerqueira    | Daniel Ferreira |
| 1.1    | Adição da etapa Sketch    | [Henrique Martins Alencar](https://github.com/henryqma)    |  |