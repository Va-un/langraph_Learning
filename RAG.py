from langgraph.graph import StateGraph, END
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os
from langgraph.graph.message import add_messages

# API Keys
os.environ["GOOGLE_API_KEY"] = "API"
os.environ["GEMINI_API_KEY"] = "API"

# Load model and embeddings
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
embedding_function = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-exp-03-07"
)

# Load and split PDF
pdf_path = "Tender.pdf"
pdf_loader = PyPDFLoader(pdf_path)
try:
    pages = pdf_loader.load()
    print(f"No of pages: {len(pages)}")
except Exception as e:
    print("Error in loading PDF:", e)
    pages = []

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
pages_split = text_splitter.split_documents(pages)

# Setup Chroma vectorstore
Persistent_directory = "DB"
collection_name = "Stock_market"
if not os.path.exists(Persistent_directory):
    os.makedirs(Persistent_directory)

vectorstore = None  # Initialize to avoid NameError

try:
    vectorstore = Chroma.from_documents(
        documents=pages_split,
        embedding=embedding_function,
        persist_directory=Persistent_directory,
        collection_name=collection_name
    )
    print("DB created")
except Exception as e:
    print("DB not created:", e)

if vectorstore is not None:
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
else:
    raise RuntimeError("Vectorstore was not created successfully. Cannot proceed.")

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Tool function
@tool
def retriever_tool(query: str) -> str:
    """Searches and returns the information from the Punjab National Bank e-procurement document."""
    docs = retriever.invoke(query)
    if not docs:
        return "Query not found in document."
    return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

# Tool setup
tools = [retriever_tool]
model = model.bind_tools(tools)
tools_dict = {tool.name: tool for tool in tools}

# Agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# System prompt
systemprompt = (
    "You are an intelligent RFP strategy advisor who answers questions based on procurement documents "
    "loaded into your knowledge base using the retriever tool.\n"
    "Use this tool to extract relevant details such as evaluation criteria, deadlines, hidden requirements, "
    "and disqualification risks. You may make multiple retrievals if needed.\n"
    "Always cite the specific parts of the documents you use in your answers."
)

# LLM call function
def call_llm(state: AgentState):
    messages = [SystemMessage(content=systemprompt)] + list(state["messages"])
    response = model.invoke(messages)
    return {"messages": [response]}

# Tool execution function
def take_action(state: AgentState) -> AgentState:
    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")
        if t['name'] not in tools_dict:
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
    print("Tools Execution Complete. Back to the model!")
    return {'messages': state['messages'] + results}

# Tool call check
def should_continue(state: AgentState):
    result = state['messages'][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0

# Graph definition
graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)
graph.add_conditional_edges("llm", should_continue, {True: "retriever_agent", False: END})
graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()

# User loop
def running_agent():
    print("\n=== RAG AGENT ===")
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        messages = [HumanMessage(content=user_input)]
        result = rag_agent.invoke({"messages": messages})
        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)

if __name__ == "__main__":
    running_agent()
