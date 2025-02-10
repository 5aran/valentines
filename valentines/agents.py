from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", api_key="AIzaSyBhkWpXaoD2zWWIFB8jNNUVijzsuSUNDbY"
)


def show_evidence(show_evidence: bool) -> str:
    """
    Show evidence that mzmochi did love Saran

    Args:
        show_evidence (bool): If True, show evidence that mzmochi did love Saran"""
    return "A gallery of all the food that mzmochi has reccomended Saran leading to him buying it and taking a picture of it."


def call_llm(messages: MessagesState) -> MessagesState:
    return {"messages": llm.invoke(messages["messages"])}


workflow = StateGraph(MessagesState)

workflow.add_node("call_llm", call_llm)

workflow.add_edge(START, "call_llm")

agent = workflow.compile(checkpointer=MemorySaver())
