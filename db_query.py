from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import bs4


query = "Removal of asylum seekers to Rwanda"

db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
docs = db.similarity_search(query)


print(docs[0].page_content)
print(docs[0].metadata)

print(len(docs))

