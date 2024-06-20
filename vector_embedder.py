from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import bs4


### Construct retriever ###
loader = WebBaseLoader(
    web_paths=(["https://www.bailii.org/ew/cases/EWHC/Admin/2023/55.html",
                "https://www.bailii.org/ew/cases/EWHC/Admin/2023/45.html"]),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            True,
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")

print(vectorstore)
