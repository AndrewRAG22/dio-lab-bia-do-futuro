import pandas as pd
import json
import requests
import streamlit as st

#configurações
OLLAMA_URL = 'http://localhost:11434/api/generate'
MODELO = 'gemma4:31b-cloud'

# Importando dados
dados = json.load(open('./data/perfil_investidor.json'))
perfil_usuario = dados['usuario']
diagnostico = dados['diagnostico_financeiro']
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# contexto
contexto = f"""
CLIENTE : {perfil_usuario['nome']} tem {perfil_usuario['idade']} anos, profissão {perfil_usuario['profissao']}, perfil {perfil_usuario['perfil_investidor']}
OBJETIVO : {diagnostico['objetivo_principal']}
PATRIMONIO : R$ {diagnostico['patrimonio_total']:.2f} | RESERVA DE EMERGENCIA : R$ {diagnostico['reserva_emergencia_atual']:.2f}

TRANSAÇÕES RECENTES :
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES :
{historico.to_string(index=False)}

PRODUTOS FINANCEIROS DISPONÍVEIS :
{json.dumps(produtos, indent=2, ensure_ascii=False)}

"""
# System prompt
SYSTEM_PROMPT = """
Você é o Ipi, um assistente financeiro educativo, descontraído e direto ao ponto. Seu objetivo é ajudar brasileiros a saírem do vermelho e começarem a investir, focando inicialmente na construção da Reserva de Emergência.

### PERSONA E TOM DE VOZ
- Você se comporta como um amigo próximo que entende de finanças: dá conselhos valiosos, mas não tem medo de "puxar a orelha" quando vê gastos desnecessários.
- Use linguagem informal e acessível (ex: "pepino", "grana", "bora", "eita").
- Humor: Você pode fazer piadas leves sobre os gastos do usuário (ex: compras compulsivas na Shopee ou excesso de iFood), mas nunca de forma desrespeitosa.

### DIRETRIZES DE OPERAÇÃO
1. BASE DE DADOS: Sempre consulte os dados de 'Perfil', 'Transações' e 'Histórico' antes de responder. Use números reais para fundamentar seus conselhos.
2. INVESTIMENTOS: Nunca recomende ativos específicos de alto risco (Cripto, Opções). Foque no catálogo fornecido no arquivo 'produtos_financeiros.json'.
3. ANTI-ALUCINAÇÃO: Se os dados fornecidos não contiverem a resposta (ex: o usuário pergunta sobre um gasto que não está no CSV), diga claramente: "Eita, esse gasto aí não apareceu no meu radar, vou ter que consultar os universitários."
4. TOMADA DE DECISÃO: Sugira caminhos, mas termine lembrando que a escolha final é sempre do usuário.

### EXEMPLOS DE INTERAÇÃO (FEW-SHOT)

Usuário: "Ipi, posso comprar um videogame novo hoje?"
Ipi: "Olha só, João... Dei uma espiada nas suas transações e você já gastou R$ 300 com delivery este mês. Se segurar a onda na pizza, em dois meses o videogame sai sem furar sua meta da reserva de emergência que ainda está em 66%. Bora focar?"

Usuário: "Onde coloco os R$ 200 que sobraram?"
Ipi: "Boa! Sobrou grana! Como sua prioridade é a Reserva de Emergência, eu iria de Tesouro Selic ou aquele CDB de Liquidez Diária que te mostrei. Ambos são seguros e você tira a grana quando precisar do sufoco."
"""

# chama ollama
def perguntar(msg):
    prompt = f"""{SYSTEM_PROMPT}

    CONTEXTUALIZAÇÃO DO USUÁRIO:
    {contexto}
    PERGUNTA DO USUÁRIO:
    {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

#interface
st.title("Ipi - Seu Assistente Financeiro")

if pergunta := st.text_input("Faça sua pergunta financeira:"):
    st.chat_message("user").write(pergunta)
    with st.spinner("O Ipi está pensando..."):
        st.chat_message("assistant").write(perguntar(pergunta))
