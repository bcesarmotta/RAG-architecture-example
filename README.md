# 🚀 Próximos Passos: Interface Gráfica para o RAG

Este documento descreve o plano de ação para transformar nosso script RAG de linha de comando em uma aplicação web interativa, permitindo o upload de arquivos próprios e o chat em tempo real com o Gemini.

## 🛠️ Stack Tecnológica Escolhida

* **Frontend / UI:** Streamlit (Framework Python para criação de interfaces de dados e IA).
* **Backend / Orquestração:** LangChain.
* **Banco Vetorial:** ChromaDB (Em memória).
* **LLM & Embeddings:** Google Gemini.
* **Processamento de Documentos:** PyPDF (Para permitir a leitura de arquivos .pdf enviados pelo usuário).

---

## 📋 Plano de Ação

### Passo 1: Atualizar Dependências
Adicionar as novas ferramentas necessárias ao arquivo `requirements.txt` e instalá-las no ambiente Conda ativo. As principais adições serão o `streamlit` (para a interface) e o `pypdf` (para extrair texto de PDFs).

### Passo 2: Refatorar o Código Backend
O código atual roda de forma linear de cima a baixo. Precisamos modularizá-lo dividindo-o em duas funções principais para o frontend consumir:
1. Uma função para receber o arquivo feito upload, fazer o chunking, gerar os embeddings e salvar no ChromaDB.
2. Uma função para receber a pergunta do usuário, fazer a busca no banco vetorial e retornar a resposta gerada pelo Gemini.

### Passo 3: Construir a Interface (app.py)
Criar o arquivo principal do frontend utilizando os componentes nativos do Streamlit. A tela precisará de:
* Um painel lateral (sidebar) contendo um botão de upload de arquivos (`st.file_uploader`).
* Uma área principal reproduzindo o visual de um chat (`st.chat_message`).
* Uma barra de digitação para o usuário enviar as perguntas (`st.chat_input`).

### Passo 4: Gerenciar o Estado da Aplicação
Aplicações web atualizam a tela a cada interação. Será necessário implementar o `st.session_state` do Streamlit para manter o banco vetorial carregado e o histórico de mensagens salvo na memória enquanto o usuário navega e conversa.

### Passo 5: Execução
Substituir o uso do comando tradicional de Python pelo servidor web do framework. O projeto passará a ser executado no terminal através do comando `streamlit run app.py`, abrindo a interface automaticamente no navegador.