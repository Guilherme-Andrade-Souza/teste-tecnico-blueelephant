# Importa as bibliotecas necessárias para manipulação de arquivos, carregamento de documentos,
# divisão de texto, banco de dados vetorial Chroma e embeddings do Google Generative AI
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define o diretório de persistência para o ChromaDB
PERSIST_DIRECTORY = "./chroma_db"
# Define o nome da coleção no ChromaDB
COLLECTION_NAME = "country_history"

def inicializacao_vector_store():
    """Inicializa e carrega dados na Vector Store (ChromaDB)."""

    # Inicializa a função de embedding usando o modelo do Google
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # Inicializa o ChromaDB com o nome da coleção, função de embedding e diretório de persistência
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    
    # Verifica se a coleção está vazia para carregar os dados iniciais
    dados_existentes = vector_store.get()
    if len(dados_existentes['ids']) == 0:
        print("ChromaDB está vazia, carregando dados iniciais.")
        load_initial_data(vector_store, embedding_function)
    else:
        print(f"ChromaDB já populada com {len(dados_existentes['ids'])} documentos.")

    return vector_store

def load_initial_data(vector_store: Chroma, embedding_function):
    '''Carrega dados do arquivo de contexto e popula a Vector Store'''

    # Define o caminho para o arquivo de contexto
    file_path = "vectorStore/history_context.txt"
    
    # Verifica se o arquivo de contexto existe
    if not os.path.exists(file_path): 
        print(f"ERRO CRÍTICO: Arquivo não encontrado em {file_path}")
        return

    # Carrega os documentos do arquivo de texto
    loader = TextLoader(file_path, encoding='utf-8')
    documents = loader.load()

    # Valida se o arquivo de contexto não está vazio
    if not documents or not documents[0].page_content.strip():
        print("ERRO CRÍTICO: O arquivo history_context.txt está VAZIO. Adicione texto nele.")
        return

    # Inicializa o divisor de texto para dividir os documentos em chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    texts = text_splitter.split_documents(documents)

    # Valida se foram gerados chunks de texto
    if len(texts) == 0:
        print("AVISO: Nenhum chunk de texto foi gerado. Verifique o conteúdo do arquivo.")
        return

    print(f"Indexando {len(texts)} chunks na Vector Store.")

    # Adiciona os textos ao ChromaDB
    vector_store.add_documents(texts)
    print("Dados indexados com sucesso.")

def get_retriever():
    """Inicializa a Vector Store e a retorna como um retriever."""
    vector_store = inicializacao_vector_store()
    # Retorna um retriever que busca os 3 documentos mais similares
    return vector_store.as_retriever(search_kwargs={"k": 3})

# Bloco para executar a inicialização do retriever quando o script é executado diretamente
if __name__ == "__main__":
    get_retriever()