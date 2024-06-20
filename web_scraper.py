import requests
from bs4 import BeautifulSoup
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import bs4

# The URL of the parent page
url = "https://www.bailii.org/ew/cases/EWHC/Admin/2023/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://example.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


# Send a request to fetch the HTML content of the parent page
response = requests.get(url, headers=headers)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all <a> tags
a_tags = soup.find_all('a')

# Extract href attributes from the <a> tags
links = [tag.get('href') for tag in a_tags if tag.get('href')]

# Filter the links if needed (e.g., remove links to external sites, duplicates, etc.)
# Here we assume that subpages are relative URLs (not starting with http or https)
subpage_links = [link for link in links if link.startswith(('/ew/cases/EWHC/Admin/2023/'))]
unique_links = []
for link in subpage_links:
    if link not in unique_links:
        unique_links.append(link)
web_paths = [f"https://www.bailii.org/{link}" for link in unique_links]

# Count the number of subpages
num_subpages = len(unique_links)

print(f"Number of possible HTML subpages: {num_subpages}")

# Optionally, print the list of subpage links
for link in unique_links:
    print(link)




### Construct retriever ###
loader = WebBaseLoader(
    web_paths=(web_paths[:10]),
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
