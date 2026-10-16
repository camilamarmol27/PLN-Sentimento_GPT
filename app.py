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
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT naturally UNLESS REQUIRED BY LAW.

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

```toml
AZURE_OPENAI_API_KEY = "6t2pTNsmNafDyo53MDAFIrvvQRBZXP7dLcr5j3TLxMS34LQVq3ZUJQQJ99CHACHYHv6XJ3w3AAAAACOGT7os"
AZURE_OPENAI_ENDPOINT = "[https://marcelomaffeis-05082026-resource.services.ai.azure.com/](https://marcelomaffeis-05082026-resource.services.ai.azure.com/)"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4.1-mini"
AZURE_OPENAI_API_VERSION = "2024-08-01-preview"
