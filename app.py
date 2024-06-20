#!/usr/bin/env python
from fastapi import FastAPI
from langserve import add_routes
from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
import dotenv
from langgraph.checkpoint import MemorySaver


dotenv.load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

### Build retriever tool ###
tool = create_retriever_tool(
    retriever,
    "case_law",
    "Searches and returns excerpts from 2023 UK case law.",
)
tools = [tool]

system_message = "You are a helpful assistant with access to a tool."
agent_executor = create_react_agent(llm, tools, checkpointer=MemorySaver(), messages_modifier=system_message)

### Make the query ###
# query = "What does the potentiality of AI agents depend on?"
query = "What's the weather like today?"
config = {"configurable": {"thread_id": "abc124"}}

for s in agent_executor.stream(
    {"messages": [HumanMessage(content=query)]}, stream_mode="updates", config=config
):
    print(s)
    print("----")
