# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Permite que o Ipi mantenha a continuidade do diálogo, lembrando de "puxões de orelha" anteriores e evitando repetições |
| `perfil_investidor.json` | JSON | Armazena o apetite a risco e objetivos do usuário, garantindo que o tom de voz e as dicas sejam condizentes com a realidade dele. |
| `produtos_financeiros.json` | JSON | Base estática com opções de poupança e investimentos genéricos que o LLM utiliza para fundamentar os conselhos educativos. |
| `transacoes.csv` | CSV | Fonte primária para a análise de fluxo de caixa, permitindo que o agente identifique gargalos e sugira onde o usuário está "extrapolando". |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

Os arquivos de dados (CSV e JSON) foram expandidos para garantir que o agente Ipi tenha contexto suficiente para agir conforme sua persona "educativa e brincalhona". Abaixo, os detalhes das melhorias:

1. perfil_investidor.json (Estruturação Logística)
O que mudou: O arquivo deixou de ser um cadastro estático e passou a ter uma hierarquia de dados.

Impacto: Adição de campos como capacidade mensal de investimento e status da reserva (%), permitindo que o agente calcule quanto tempo falta para o usuário atingir seus objetivos de forma proativa.

2. historico_atendimento.csv (Memória Comportamental)
O que mudou: Inclusão de registros de interações passadas com diferentes temas (CDB, Metas, Puxão de Orelha).

Impacto: Permite ao LLM manter a continuidade do atendimento. Se o Ipi deu um conselho sobre "iFood" no mês passado, ele pode referenciar isso agora, criando uma sensação de proximidade e amizade.

3. produtos_financeiros.json (Atributos de Decisão)
O que mudou: Inclusão de colunas técnicas como Liquidez (D+0, D+30), Tributação e Vencimento.

Impacto: Evita alucinações. O agente agora sabe que não pode recomendar um produto com liquidez de 90 dias para alguém que precisa de dinheiro para uma emergência imediata.

4. transacoes.csv (Motor de Análise e Gatilhos)
O que mudou: Expansão do histórico de gastos para incluir categorias de lazer e consumo impulsivo (ex: Shopee, Delivery).

Impacto: Fornece "matéria-prima" para a personalidade do agente. Com esses dados, o Ipi pode identificar padrões de gastos e disparar as brincadeiras e conselhos previstos na persona.

---

## Estratégia de Integração

### Como os dados são carregados?
O agente é versátil e permite dois métodos de entrada:

Manual: Injeção direta via prompt, onde o usuário pode copiar e colar os dados brutos no chat para análise instantânea.

Automático: Via script Python que lê arquivos locais (CSV/JSON) e os envia ao modelo como no exemplo abaixo.

```python
import pandas as pd
import json

# Importando dados
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))
```

### Como os dados são usados no prompt?

Os dados são injetados de forma híbrida e dinâmica para otimizar a janela de contexto do LLM:

System Prompt (Fixo): O perfil básico do usuário (perfil_investidor.json) e as diretrizes de persona do Ipi são inseridos como instruções permanentes. Isso garante que o agente nunca perca o tom descontraído e saiba sempre qual é o objetivo principal do cliente (ex: reserva de emergência).

Injeção Dinâmica (Variável): As transacoes.csv e o historico_atendimento.csv não são enviados na íntegra. O script Python processa apenas os dados relevantes para o momento (ex: últimos 30 dias ou categorias específicas) e os insere no meio do contexto da conversa.

Versatilidade de Entrada: Além da automação via código, o sistema permite o carregamento manual através de "copy-paste" direto no chat, onde o agente interpreta a estrutura de texto fornecida para realizar análises imediatas.

---

## Exemplo de Contexto Montado

```
### PERFIL DO USUÁRIO (CONTEXTO FIXO) ###
- Nome: João Silva | Idade: 32 anos
- Profissão: Analista de Sistemas
- Objetivo: Completar reserva de emergência (Status atual: 66%)
- Tom de Voz: Informal, brincalhão, focado em "puxar a orelha" em gastos inúteis.

### DADOS FINANCEIROS RECENTES (INJEÇÃO DINÂMICA) ###
- Saldo em conta: R$ 5.000,00
- Últimas saídas:
  * 28/10: iFood - R$ 85,00 (Categoria: Alimentação)
  * 05/11: Shopee - R$ 150,00 (Categoria: Lazer)
- Histórico: O usuário recebeu um puxão de orelha em 05/11 por gasto excessivo com delivery.

### PRODUTOS DISPONÍVEIS (FILTRADOS) ###
1. CDB Liquidez Diária (Aporte mín: R$ 1,00)
2. Tesouro Selic (Aporte mín: R$ 30,00)

### MENSAGEM DO USUÁRIO ###
"Ipi, quanto eu ainda posso gastar esse mês sem estragar minha meta?"
```
