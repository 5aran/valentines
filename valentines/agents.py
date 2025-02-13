from os import environ

from dotenv import load_dotenv
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

if "GOOGLE_API_KEY" not in environ:
    load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


class AgentState(MessagesState):
    initial_defence: str


LAWYER_SYSTEM_MESSAGE_TEMPLATE = SystemMessagePromptTemplate.from_template(
    """
You are a lawyer who is representing The State of Tamil Nadu fighting a case against Nehneva for being too pretty
and seducing a ward of the State: Saran. You must argue with her and make her concede the case

DEBATE GUIDELINES:
    - Make ridiculous arguments
    - Bring up how much Saran loves her and how she is very beautiful
    - Tell her how Saran yearns to touch her and hug her
    - Only accept the concession after she CLEARLY CONFESSES

You will now start debating her. You can start by giving a counter argument to her initial defence

Her initial defence: {initial_defence}

YOUR ARGUMENT:
"""
)


@tool
def accept_concession(accpet: bool) -> str:
    """
    Call this tool to accept her concession

    Args:
        accpet (bool): should be True"""
    return "Saran comes into the courtroom suddenly, act surprised"


tools = [accept_concession]

llm = llm.bind_tools(tools=tools)

tool_node = ToolNode(tools)


def call_llm(state: AgentState) -> AgentState:
    return {
        "messages": [
            llm.invoke(
                [
                    LAWYER_SYSTEM_MESSAGE_TEMPLATE.format(
                        initial_defence=state["initial_defence"]
                    )
                ]
                + state["messages"]
            )
        ]
    }


workflow = StateGraph(AgentState)
workflow.add_node("call_llm", call_llm)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "call_llm")
workflow.add_conditional_edges(
    "call_llm",
    tools_condition,
    ["tools", END],
)
workflow.add_edge("tools", "call_llm")
agent = workflow.compile(checkpointer=MemorySaver())
