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
# PASSO 1: LIMITADOR DINÂMICO DE PAÍSES
# ==========================================
st.header("1. Definição dos Países-Alvo")
paises_selecionados = st.multiselect(
    "Selecione ou digite os países para a comparação (Máximo de 5):",
    options=LISTA_30_PAISES,
    default=["Colômbia", "México", "Chile"]
)

if len(paises_selecionados) > 5:
    st.error("⚠️ Limite máximo de 5 países simultâneos atingido. Remova um para prosseguir.")
    st.stop()

if not paises_selecionados:
    st.warning("Insira pelo menos 1 país para iniciar a análise.")
    st.stop()

# ==========================================
# PASSO 2: SELEÇÃO DE VARIÁVEIS
# ==========================================
st.header("2. Seleção de Variáveis Estratégicas")
st.caption("Escolha quais critérios quer usar. Passe o mouse sobre as interrogações para ver o significado.")

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
# PASSO 3: PESOS E NOTAS VIA FORMULÁRIO SEGURO
# ==========================================
st.header("3. Avaliação de Pesos e Notas")

pesos = {}
notas = {pais: {} for pais in paises_selecionados}

if total_selecionado > 0:
    st.markdown("### ⚖️ Defina o Peso de Relevância de cada variável (1 a 5):")
    cols_pesos = st.columns(min(total_selecionado, 3))
    for idx, var in enumerate(variaveis_finais.keys()):
        col_atual = cols_pesos[idx % min(total_selecionado, 3)]
        pesos[var] = col_atual.slider(f"Importância: {var}", 1.0, 5.0, 3.0, step=0.5, key=f"peso_{var}")

    st.markdown("### 📝 Atribua as Notas para cada País (1 a 5):")
    # Organiza em abas (uma para cada país), ficando super elegante e leve para o navegador
    abas_paises = st.tabs([f"📍 {pais}" for pais in paises_selecionados])
    
    for idx_pais, pais in enumerate(paises_selecionados):
        with abas_paises[idx_pais]:
            st.subheader(f"Notas para {pais}")
            for var in variaveis_finais.keys():
                notas[pais][var] = st.slider(f"Nota para '{var}' em {pais}", 1.0, 5.0, 3.0, step=0.5, key=f"nota_{pais}_{var}")

    # ==========================================
    # PASSO 4: DASHBOARD DE RESULTADOS (SEGURO)
    # ==========================================
    st.header("4. Dashboard Consolidado de Decisão")
    
    # Processamento matemático simplificado e rápido
    pontuacao_final = {}
    soma_pesos = sum(pesos.values())
    
    # Criando estruturas para exibição final de relatórios
    linhas_relatorio = []
    
    for var, cat in variaveis_finais.items():
        item_dict = {"Variável": var, "Categoria": cat, "Peso": pesos[var]}
        for pais in paises_selecionados:
            item_dict[f"Nota {pais}"] = notas[pais][var]
        linhas_relatorio.append(item_dict)

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

    # Gráficos nativos ultraestáveis
    st.subheader("📊 Ranking Geral (Pontuação Ponderada)")
    st.bar_chart(series_pontos, horizontal=True)

    # Exportação estável em formato padrão
    st.subheader("💾 Exportar Relatório")
    df_export = pd.DataFrame(linhas_relatorio)
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados da Simulação (CSV)",
        data=csv_data,
        file_name="priorizacao_mercados_exportacao.csv",
        mime="text/csv"
    )
else:
    st.info("Ative pelo menos uma variável estratégica para iniciar.")
