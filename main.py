import os
from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


# ---------------------------
# 1. Configuração
# ---------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY não encontrada no .env")

os.environ["GOOGLE_API_KEY"] = api_key


# ---------------------------
# 2. Scraping
# ---------------------------
print("Fazendo o scraping do site...")

url = "https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial"
loader = WebBaseLoader(url)
docs = loader.load()


# ---------------------------
# 3. Chunking
# ---------------------------
print("Dividindo o texto em partes menores...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

splits = text_splitter.split_documents(docs)


# ---------------------------
# 4. Embeddings (LOCAL 🔥)
# ---------------------------
print("Criando embeddings (HuggingFace local)...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------------------
# 5. Vector Store
# ---------------------------
print("Criando banco vetorial...")

vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


# ---------------------------
# 6. LLM (Gemini)
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest",
    temperature=0.3,
    convert_system_message_to_human=True
)


# ---------------------------
# 7. Prompt
# ---------------------------
system_prompt = (
    "Você é um assistente prestativo. "
    "Use apenas o contexto abaixo para responder à pergunta. "
    "Se não souber, diga claramente que não encontrou no texto.\n\n"
    "Contexto:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])


# ---------------------------
# 8. RAG Chain
# ---------------------------
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# ---------------------------
# 9. Pergunta
# ---------------------------
pergunta = "Quais são os principais riscos da inteligência artificial mencionados no texto?"

print(f"\nPergunta: {pergunta}")
print("\nBuscando resposta...\n")

resposta = rag_chain.invoke({"input": pergunta})

print("Resposta:\n")
print(resposta["answer"])