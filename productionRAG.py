from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import pymupdf4llm
from langchain_core.documents import Document
from langchain_chroma import Chroma


embedding = OllamaEmbeddings(model="llama3.2")

vector_store = Chroma(
    collection_name= "my_docs",
    embedding_function=embedding,
    persist_directory="./chroma_db"
)

def additional_recursive_chunker(markdown_chunks : list[Document], chunk_size = 600, chunk_overlap = 100):
    good_chunk = []
    chunk_count = 0
    recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, 
                                                             chunk_overlap = chunk_overlap, 
                                                             separators=["\n\n", "\n", ". ", " ", ""])
    for chunk in markdown_chunks:
        if(len(chunk.page_content) > chunk_size):
            meta_data = chunk.metadata
            chunks = recursive_text_splitter.split_documents([chunk])
            for i in chunks:
                chunk_count = chunk_count + 1
                i.metadata["chunk_id"] = chunk_count
                good_chunk.append(i)
            chunk_count = 0
        else:
            good_chunk.append(chunk)
    return good_chunk


def ingest_document(file_path : str) -> list[Document]:
    file_path = "Attention.pdf"
    markdown = pymupdf4llm.to_markdown(file_path)
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4")
    ]
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on = headers_to_split_on)
    markdown_chunks = splitter.split_text(markdown)

    # this is the final chunk and metadata which is to be stores and embedded
    final_chunks = additional_recursive_chunker(markdown_chunks)

    # embedding
    embeddings = vector_store.add_documents(documents = final_chunks)
    return final_chunks


def search_documenta(query : str, filter : dict[str, str] = None):

    print(query)
    retriever = vector_store.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            'k' : 3,
            'fetch_k' : 10,
            'lambda_mult' : 0.7
        },
        filter = filter if filter else { 'Header 1': '**Attention Is All You Need**', 'Header 2': '**Abstract**'})

    # 1. embed the query
    # 2. bm25 search
    # 3. rrf
    # 4. re-ranker


def generation(chunks : str):
    # metadata and chunks to the llm for generation
    pass    x