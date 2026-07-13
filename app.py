import streamlit as st
import pandas as pd

# Configuração da página para um layout mais profissional e amplo
st.set_page_config(page_title="Seleção de Mercados - Exportação", layout="wide")

st.title("🌍 Inteligência Comercial: Seleção de Mercados-Alvo")
st.markdown("""
Este aplicativo ajuda empresas brasileiras a priorizarem mercados estratégicos para exportação. 
Selecione as variáveis, defina os países e atribua as notas para obter o ranking ponderado em tempo real.
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
    },
    "Estrutura Local (Opcionais)": {
        "Facilidade de Parcerias Estratégicas": "Disponibilidade de agentes para modelos de representação ou Joint Venture.",
        "Custo de Instalação Comercial": "Custos fixos para abertura de escritório ou filial de vendas local, se necessário."
    }
}

# Lista dos 30 países sugeridos para exportação brasileira
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
    st.error("⚠️ Para garantir uma análise estratégica focada, o limite máximo é de 5 países simultâneos. Por favor, remova os excedentes.")
    st.stop()

if not paises_selecionados:
    st.warning("Insira pelo menos 1 país para iniciar a análise.")
    st.stop()

# ==========================================
# PASSO 2: SELEÇÃO DE VARIÁVEIS
# ==========================================
st.header("2. Seleção de Variáveis Estratégicas")
st.caption("Passe o mouse sobre as interrogações para ler o significado de cada critério.")

variaveis_finais = {}
for categoria, sub_vars in BANCO_VARIAVEIS.items():
    with st.expander(f"📂 Categoria: {categoria}"):
        for var_nome, var_desc in sub_vars.items():
            selecionado = st.checkbox(var_nome, value=True if var_nome in ["Tamanho do Mercado Potencial", "Crescimento do Mercado", "Tarifas e Impostos de Importação", "Custo Logístico de Envio", "Preço Competitivo"] else False, help=var_desc, key=var_nome)
            if selecionado:
                variaveis_finais[var_nome] = categoria

nova_var = st.text_input("✍️ Quer adicionar alguma outra variável customizada? Digite o rótulo aqui:")
if nova_var:
    variaveis_finais[nova_var] = "Customizada"

total_selecionado = len(variaveis_finais)
st.info(f"Fatores selecionados até o momento: **{total_selecionado}**")

if total_selecionado < 5 or total_selecionado > 10:
    st.warning(f"💡 Dica de Metodologia: Recomendamos utilizar entre **5 e 10 variáveis** para um resultado robusto sem poluir o modelo.")

# ==========================================
# PASSO 3: MATRIZ DE INPUTS (PESOS E NOTAS)
# ==========================================
st.header("3. Matriz de Avaliação (Pesos e Notas)")

if total_selecionado > 0:
    dados_colunas = ["Variável", "Categoria", "Peso Relevância"] + paises_selecionados
    linhas = []
    for var, cat in variaveis_finais.items():
        linha_dict = {"Variável": var, "Categoria": cat, "Peso Relevância": 3.0}
        for pais in paises_selecionados:
            linha_dict[pais] = 3.0
        linhas.append(linha_dict)
        
    df_base = pd.DataFrame(linhas)
    
    df_editado = st.data_editor(
        df_base, 
        hide_index=True,
        column_config={
            "Peso Relevância": st.column_config.NumberColumn("Peso (1-5)", min_value=1.0, max_value=5.0, step=0.5),
            **{pais: st.column_config.NumberColumn(f"Nota {pais} (1-5)", min_value=1.0, max_value=5.0, step=0.5) for pais in paises_selecionados}
        }
    )
    
    # ==========================================
    # PASSO 4: DASHBOARD DE RESULTADOS
    # ==========================================
    st.header("4. Dashboard Consolidado de Decisão")
    
    df_calculado = df_editado.copy()
    for pais in paises_selecionados:
        df_calculado[pais] = df_calculado[pais] * df_calculado["Peso Relevância"]
        
    soma_pesos = df_calculado["Peso Relevância"].sum()
    pontuacao_final = df_calculado[paises_selecionados].sum() / (soma_pesos if soma_pesos > 0 else 1)
    pontuacao_final = pontuacao_final.round(2)
    
    st.subheader("🏆 Principais Destinos")
    kpi_cols = st.columns(len(paises_selecionados))
    paises_ordenados = pontuacao_final.sort_values(ascending=False)
    
    for idx, (pais, nota) in enumerate(paises_ordenados.items()):
        with kpi_cols[idx]:
            if idx == 0:
                st.metric(label="🥇 Recomendado", value=pais, delta=f"Nota: {nota}")
            elif idx == 1:
                st.metric(label="🥈 2º Lugar", value=pais, delta=f"Nota: {nota}", delta_color="off")
            else:
                st.metric(label=f"🥉 {idx+1}º Lugar", value=pais, delta=f"Nota: {nota}", delta_color="off")
                
    graf_col1, graf_col2 = st.columns(2)
    
    with graf_col1:
        st.subheader("📊 Ranking Geral (Pontuação Ponderada)")
        # Gráfico nativo do Streamlit: super rápido, interativo e imune a erros de memória
        st.bar_chart(pontuacao_final, horizontal=True)
        
    with graf_col2:
        st.subheader("📈 Comparativo por Macro-Categorias")
        # Como o radar dependia do Plotly, usamos um gráfico de área empilhada nativa que mostra 
        # o peso visual de cada categoria por país de forma fantástica
        df_radar_grouped = df_editado.groupby("Categoria")[paises_selecionados].mean()
        st.area_chart(df_radar_grouped)

    st.subheader("💾 Exportar Relatório")
    df_export = df_editado.copy()
    for pais in paises_selecionados:
        df_export[f"Ponderado {pais}"] = df_export[pais] * df_export["Peso Relevância"]
        
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados da Simulação (CSV)",
        data=csv_data,
        file_name="priorizacao_mercados_exportacao.csv",
        mime="text/csv"
    )
else:
    st.info("Por favor, ative pelo menos uma variável estratégica para realizar os cálculos da matriz.")
