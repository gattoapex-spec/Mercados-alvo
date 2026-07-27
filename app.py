import streamlit as st
import pandas as pd

# Configuração da página para um layout limpo e amplo
st.set_page_config(page_title="Seleção de Mercados - Exportação", layout="wide")

st.title("🌍 Seleção de Mercados-Alvo para Exportação")
st.markdown("""
Este aplicativo ajuda empresas brasileiras a priorizarem mercados estratégicos para exportação. 
Selecione as variáveis que sejam mais importantes para a sua empresa, defina a relevância de cada uma e atribua notas para cada país - você pode preencher com as informações de que dispõe nesse momento, e refazer esta priorização quando achar necessário.
""")

# ==========================================
# BANCO DE VARIÁVEIS COM EXPLICAÇÕES BREVES
# ==========================================
BANCO_VARIAVEIS = {
    "Mercado e Potencial": {
        "Tamanho do Mercado Potencial": "Volume estimado de vendas ou número de consumidores para seu produto no país.",
        "Crescimento do Mercado": "Tendência de expansão ou retração do setor nos últimos anos.",
        "Renda e Poder de Compra": "Nível de renda per capita e capacidade financeira do público-alvo local.",
        "Proximidade Cultural": "Grau de similaridade nos hábitos, idioma ou laços históricos que facilitam aceitação.",
        "Perfil e Hábitos de Compra": "Comportamento do consumidor local (ex: exigência por qualidade, canais digitais)."
    },
    "Acesso e Regulatório": {
        "Tarifas e Impostos de Importação": "Alíquotas de impostos na entrada (verificar se há acordos comerciais favoráveis).",
        "Barreiras Não Tarifárias": "Exigências técnicas, sanitárias, ambientais ou cotas de importação no destino.",
        "Complexidade Aduaneira": "Nível de burocracia e tempo médio de liberação de carga nos portos/aeroportos.",
        "Segurança Jurídica": "Estabilidade das leis comerciais e proteção à propriedade intelectual (marcas/patentes)."
    },
    "Logística": {
        "Custo Logístico de Envio": "Gastos com frete internacional, seguros e armazenagem até o destino.",
        "Tempo de Trânsito (Lead Time)": "Dias necessários para que a mercadoria saia do Brasil e chegue ao destino.",
        "Canais de Distribuição Locais": "Disponibilidade e maturidade de parceiros, distribuidores ou redes de varejo.",
        "Infraestrutura Logística Interna": "Qualidade da malha de distribuição rodoviária/ferroviária dentro do país alvo."
    },
    "Ambiente Competitivo": {
        "Intensidade da Concorrência Local": "Presença e força de fabricantes nacionais instalados no país de destino.",
        "Presença de Concorrentes Internacionais": "Nível de atuação de marcas de outros países que também exportam para lá.",
        "Saturação do Mercado": "Avaliação se o mercado já está maduro e lotado ou se ainda há lacunas.",
        "Barreiras de Entrada de Concorrentes": "Dificuldade de se posicionar frente aos players já estabelecidos."
    },
    "Produto e Operação": {
        "Necessidade de Adaptação do Produto": "Alterações exigidas em embalagem, rótulo ou fórmula para atender normas locais.",
        "Grau de Conhecimento Interno": "Nível de domínio que sua empresa já possui sobre as regras e cultura daquele mercado.",
        "Preço Competitivo": "Capacidade de manter margem saudável após somar todos os custos de exportação."
    }
}

LISTA_30_PAISES = [
    "Estados Unidos", "China", "Argentina", "México", "Chile", "Paraguai", "Uruguai", "Colômbia", "Peru", "Portugal",
    "Alemanha", "Espanha", "França", "Reino Unido", "Itália", "Países Baixos", "Japão", "Índia", "Canadá", "Emirados Árabes Unidos",
    "Arábia Saudita", "África do Sul", "Angola", "Bolívia", "Equador", "Panamá", "Suíça", "Bélgica", "Coreia do Sul", "Austrália"
]

# ==========================================
# PASSO 1: DEFINE PAÍSES-ALVO
# ==========================================
st.header("1. Definição dos Países-Alvo")

paises_selecionados = st.multiselect(
    "Selecione da lista ou digite os países para a comparação (Máximo de 5):",
    options=LISTA_30_PAISES,
    default=[],
    placeholder="Digite ou escolha até 5 países..."
)

if len(paises_selecionados) > 5:
    st.error("⚠️ Limite máximo de 5 países simultâneos atingido. Remova um para prosseguir.")
    st.stop()

if not paises_selecionados:
    st.info("👆 Por favor, selecione ou digite pelo menos 1 país acima para começar a montar sua matriz.")
    st.stop()

# ==========================================
# PASSO 2: SELEÇÃO DE VARIÁVEIS
# ==========================================
st.header("2. Seleção de Variáveis Estratégicas")
st.caption("Escolha até 10 critérios, entre os listados abaixo, para comparar os países que você escolheu. Passe o mouse sobre as interrogações para ver o significado de cada critério.")

variaveis_finais = {}
for categoria, sub_vars in BANCO_VARIAVEIS.items():
    with st.expander(f"📂 Categoria: {categoria}"):
        for var_nome, var_desc in sub_vars.items():
            padrao = var_nome in ["Tamanho do Mercado Potencial", "Crescimento do Mercado", "Tarifas e Impostos de Importação", "Custo Logístico de Envio", "Preço Competitivo"]
            if st.checkbox(var_nome, value=padrao, help=var_desc, key=f"chk_{var_nome}"):
                variaveis_finais[var_nome] = categoria

total_selecionado = len(variaveis_finais)
st.info(f"Fatores estratégicos ativos: **{total_selecionado}**")

# ==========================================
# PASSO 3: AVALIAÇÃO DOS CRITÉRIOS
# ==========================================
st.header("3. Avaliação dos Critérios")

pesos = {}
notas = {pais: {} for pais in paises_selecionados}

if total_selecionado > 0:
    st.markdown("### ⚖️ Defina a relevância de cada variável")
    st.markdown("Alguns dos critérios que você selecionou acima são mais importantes para sua empresa que outros. Defina a relevância de cada um deles atribuindo uma nota de 1 a 5 - 1 para os que têm menos importância, 5 para os mais relevantes.")
    
    cols_pesos = st.columns(min(total_selecionado, 3))
    for idx, var in enumerate(variaveis_finais.keys()):
        col_atual = cols_pesos[idx % min(total_selecionado, 3)]
        pesos[var] = col_atual.slider(f"Importância: {var}", 1.0, 5.0, 3.0, step=0.5, key=f"peso_{var}")

    st.markdown("---")
    st.markdown("### 📝 Atribua notas para cada país")
    st.markdown("Agora, considerando o que você já sabe sobre cada um dos países que está comparando, atribua notas de 1 a 5 para cada critério, considerando a realidade de cada país - quando terminar o primeiro, basta clicar no país seguinte, e assim por diante. **Importante:** lembre-se que as notas mais altas significam que aquele país oferece mais vantagens para você. Então, por exemplo, quanto maior o tamanho de um mercado para sua empresa, mais alta a nota; por outro lado, quanto maior o custo logístico para sua empresa, mais baixa a nota.")
    
    abas_paises = st.tabs([f"📍 {pais}" for pais in paises_selecionados])
    
    for idx_pais, pais in enumerate(paises_selecionados):
        with abas_paises[idx_pais]:
            st.subheader(f"Notas para {pais}")
            for var in variaveis_finais.keys():
                notas[pais][var] = st.slider(f"Nota para '{var}' em {pais}", 1.0, 5.0, 3.0, step=0.5, key=f"nota_{pais}_{var}")

    # ==========================================
    # PASSO 4: DASHBOARD DE RESULTADOS
    # ==========================================
    st.header("4. Dashboard Consolidado de Decisão")
    
    pontuacao_final = {}
    soma_pesos = sum(pesos.values())

    for pais in paises_selecionados:
        total_ponderado = sum(notas[pais][var] * pesos[var] for var in variaveis_finais.keys())
        pontuacao_final[pais] = round(total_ponderado / (soma_pesos if soma_pesos > 0 else 1), 2)

    series_pontos = pd.Series(pontuacao_final)
    
    # Exibição dos Cartões (KPIs)
    st.subheader("🏆 Principais Destinos")
    kpi_cols = st.columns(len(paises_selecionados))
    paises_ordenados = series_pontos.sort_values(ascending=False)
    
    for idx, (pais, nota) in enumerate(paises_ordenados.items()):
        with kpi_cols[idx]:
            if idx == 0:
                st.metric(label="🥇 Recomendado", value=pais, delta=f"Nota: {nota}")
            elif idx == 1:
                st.metric(label="🥈 2º Lugar", value=pais, delta=f"Nota: {nota}", delta_color="off")
            else:
                st.metric(label=f"🥉 {idx+1}º Lugar", value=pais, delta=f"Nota: {nota}", delta_color="off")

    # Gráfico de barras azuis nativo
    st.subheader("📊 Ranking Geral (Pontuação Ponderada)")
    st.bar_chart(paises_ordenados, horizontal=True)

    # ==========================================
    # RELATÓRIO COMPLETO PARA DOWNLOAD
    # ==========================================
    st.subheader("💾 Exportar Relatório de Priorização")
    st.caption("Baixe o relatório consolidado com o ranking final e o detalhamento de todas as notas e pesos atribuídos.")

    df_ranking = pd.DataFrame({
        "Posição": [f"{i+1}º Lugar" for i in range(len(paises_ordenados))],
        "País": paises_ordenados.index,
        "Pontuação Final Ponderada (1 a 5)": paises_ordenados.values
    })

    linhas_detalhadas = []
    for var, cat in variaveis_finais.items():
        linha = {
            "Categoria": cat,
            "Variável Estratégica": var,
            "Peso de Relevância": pesos[var]
        }
        for pais in paises_selecionados:
            linha[f"Nota ({pais})"] = notas[pais][var]
            linha[f"Pontuação Ponderada ({pais})"] = round(notas[pais][var] * pesos[var], 2)
            
        linhas_detalhadas.append(linha)
        
    df_detalhado = pd.DataFrame(linhas_detalhadas)

    conteudo_csv = "=== RELATÓRIO DE PRIORIZAÇÃO DE MERCADOS-ALVO ===\n\n"
    conteudo_csv += "--- RANKING FINAL ---\n"
    conteudo_csv += df_ranking.to_csv(index=False, sep=";") + "\n\n"
    conteudo_csv += "--- MATRIZ DETALHADA DE NOTAS E PESOS ---\n"
    conteudo_csv += df_detalhado.to_csv(index=False, sep=";")

    st.download_button(
        label="📥 Baixar Relatório Completo (Excel / CSV)",
        data=conteudo_csv.encode('utf-8-sig'),
        file_name="relatorio_priorizacao_mercados.csv",
        mime="text/csv",
        help="Baixa um arquivo compatível com o Excel contendo o ranking final e a matriz completa de cálculo."
    )
else:
    st.info("Ative pelo menos uma variável estratégica para iniciar.")
