from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
import bs4
import dotenv

dotenv.load_dotenv()

memory = SqliteSaver.from_conn_string(":memory:")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


### Construct retriever ###
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()


### Build retriever tool ###
tool = create_retriever_tool(
    retriever,
    "blog_post_retriever",
    "Searches and returns excerpts from the Autonomous Agents blog post.",
)
tools = [tool]


system_message = "You are a helpful assistant with access to a tool."
agent_executor = create_react_agent(llm, tools, checkpointer=memory, messages_modifier=system_message)


### Make the query ###
# query = "What does the potentiality of AI agents depend on?"
query = "What's the weather like today?"
config = {"configurable": {"thread_id": "abc124"}}

for s in agent_executor.stream(
    {"messages": [HumanMessage(content=query)]}, stream_mode="updates", config=config
):
    print(s)
    print("----")
