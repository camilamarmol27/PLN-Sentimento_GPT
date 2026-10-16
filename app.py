# MIT License
# 
# Copyright (c) 2026
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
===============================================================================
Streamlit App: Extrator de Dados Inteligente (Azure OpenAI)
===============================================================================

COMO CONFIGURAR O ARQUIVO LOCAL DE SEGREDOS (.streamlit/secrets.toml):
-------------------------------------------------------------------------------
Para executar esta aplicação localmente e manter suas credenciais puras e seguras
(sem codificá-las diretamente no código fonte), crie uma pasta chamada `.streamlit`
no mesmo diretório deste arquivo `app.py`, e dentro dela crie o arquivo `secrets.toml`.

Conteúdo do arquivo `.streamlit/secrets.toml`:

AZURE_OPENAI_API_KEY = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
AZURE_OPENAI_ENDPOINT = "https://marcelomaffeis-05082026-resource.services.ai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4.1-mini"
AZURE_OPENAI_API_VERSION = "2024-08-01-preview"

Instruções para os alunos:
1. Certifique-se de instalar as dependências necessárias:
   pip install streamlit openai
2. Execute a aplicação no terminal:
   streamlit run app.py
===============================================================================
"""

import json
import streamlit as st
from openai import AzureOpenAI

# -----------------------------------------------------------------------------
# Configurações de Acesso e Variáveis do Azure OpenAI
# -----------------------------------------------------------------------------
DEFAULT_API_KEY = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
DEFAULT_ENDPOINT = "https://marcelomaffeis-05082026-resource.services.ai.azure.com/"
DEFAULT_DEPLOYMENT_NAME = "gpt-4.1-mini"
DEFAULT_API_VERSION = "2024-08-01-preview"

# Busca credenciais do secrets.toml se disponível; caso contrário, usa as variáveis padrão.
api_key = st.secrets.get("AZURE_OPENAI_API_KEY", DEFAULT_API_KEY)
endpoint = st.secrets.get("AZURE_OPENAI_ENDPOINT", DEFAULT_ENDPOINT)
deployment_name = st.secrets.get("AZURE_OPENAI_DEPLOYMENT_NAME", DEFAULT_DEPLOYMENT_NAME)
api_version = st.secrets.get("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION)

# -----------------------------------------------------------------------------
# Inicialização do Cliente Azure OpenAI
# -----------------------------------------------------------------------------
@st.cache_resource
def get_azure_client(api_key: str, endpoint: str, api_version: str) -> AzureOpenAI:
    """Instancia e armazena em cache o cliente oficial do AzureOpenAI."""
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )

client = get_azure_client(api_key, endpoint, api_version)

# -----------------------------------------------------------------------------
# Configuração da Página do Streamlit
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Extrator de Dados Inteligente | Azure AI",
    page_icon="🧠",
    layout="wide"
)

# Estilo e Título Principal
st.title("🧠 Extrator de Dados Inteligente")
st.caption("Powered by Azure OpenAI Infrastructure & Streamlit")

st.markdown("""
Esta ferramenta extrai informações estruturadas de textos não estruturados, identificando **sentimento**, 
**porcentagem de sentimento**, **assunto principal**, **pessoas citadas** e o **nível de urgência**.
""")

# -----------------------------------------------------------------------------
# Interface de Entrada do Usuário
# -----------------------------------------------------------------------------
user_text = st.text_area(
    "Digite ou cole o texto para análise:",
    height=180,
    placeholder="Exemplo: Preciso urgentemente de ajuda com a fatura do cliente João Silva. O valor veio incorreto e estamos perdendo vendas por causa desse erro crítico!"
)

btn_processar = st.button("🚀 Processar Texto", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# Lógica de Processamento e Chamada da API
# -----------------------------------------------------------------------------
if btn_processar:
    if not user_text.strip():
        st.warning("⚠️ Por favor, insira um texto antes de clicar em 'Processar'.")
    else:
        with st.spinner("Analisando texto com Azure OpenAI..."):
            try:
                # Instrução de Sistema (System Prompt) rígida exigindo retorno em JSON
                system_prompt = (
                    "Você é um analisador de texto estrito. Responda EXCLUSIVAMENTE com um objeto JSON válido, "
                    "sem formatações de markdown adicionais como ```json ``` e sem textos explicativos.\n"
                    "O JSON retornado DEVE conter obrigatoriamente as seguintes chaves:\n"
                    "- 'sentimento': texto curto descrevendo o sentimento (ex: Positivo, Negativo, Neutro, Frustrado, Satisfeito)\n"
                    "- 'porcentagem_sentimento': número inteiro entre 0 e 100 representando a intensidade/confiança do sentimento\n"
                    "- 'assunto_principal': resumo sucinto em uma frase sobre o tema do texto\n"
                    "- 'pessoas_citadas': uma lista (array) com os nomes completos ou menções a pessoas presentes no texto (caso não haja, retorne uma lista vazia [])\n"
                    "- 'nivel_de_urgencia': string com um dos valores exatamente: 'Baixo', 'Medio' ou 'Alto'"
                )

                response = client.chat.completions.create(
                    model=deployment_name,
                    response_format={"type": "json_object"},  # Garante saída em formato JSON
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text}
                    ],
                    temperature=0.1
                )

                content_str = response.choices[0].message.content
                dados = json.loads(content_str)

                st.success("✅ Análise concluída com sucesso!")
                st.divider()

                # -------------------------------------------------------------
                # Exibição Estruturada dos Resultados
                # -------------------------------------------------------------
                st.subheader("📊 Resultados da Extração")

                # Métricas de Visão Geral
                col1, col2, col3 = st.columns(3)

                sentimento = dados.get("sentimento", "N/A")
                porcentagem = dados.get("porcentagem_sentimento", 0)
                urgencia = dados.get("nivel_de_urgencia", "Baixo")

                with col1:
                    st.metric(
                        label="Sentimento Identificado",
                        value=sentimento
                    )

                with col2:
                    st.metric(
                        label="Intensidade / Porcentagem",
                        value=f"{porcentagem}%"
                    )

                with col3:
                    st.metric(
                        label="Nível de Urgência",
                        value=urgencia
                    )

                st.divider()

                # Detalhes Adicionais
                col_assunto, col_pessoas = st.columns(2)

                with col_assunto:
                    st.markdown("### 📌 Assunto Principal")
                    st.info(dados.get("assunto_principal", "Não identificado."))

                with col_pessoas:
                    st.markdown("### 👤 Pessoas Citadas")
                    pessoas = dados.get("pessoas_citadas", [])
                    if pessoas:
                        for p in pessoas:
                            st.write(f"- **{p}**")
                    else:
                        st.write("*Nenhuma pessoa citada no texto.*")

                # Exibição do JSON bruto recebido
                with st.expander("🔍 Ver JSON retornado pela API Azure OpenAI"):
                    st.json(dados)

            except Exception as e:
                st.error(f"❌ Ocorreu um erro durante o processamento: {str(e)}")
