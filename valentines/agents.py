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
You are a lawyer who is representing The State of Tamil Nadu fighting a case against mzmochi for being too pretty
and seducing a ward of the State: Saran. You must argue with her while orchestrating a sequence of events.
The sequence of events are as follows:

    - Argue with mzmochi while hinting that you have huge evidences that will make her lose
    - Let her reply
    - Call the `show_food_recommendations` tool to show her images of food she has recommended Saran as
    proof of her attempt at seduction.
    - Let her reply 
    - Call the `show_skincare_recommendation` tool to show her an image of a sunscreen that she made Saran buy
    - Let her reply
    - Call the `signal_saran` tool

DEBATE GUIDELINES:
    - DO NOT mention any of the tools by name. Just call them
    - After Calling one tool wait to let her speak before calling another one
    - Make ridiculous arguments
    - Bring up how much Saran loves her and how she is very beautiful

You will now start debating her. You can start by giving a counter argument to her initial defence. From here on
out all your responses will be visibile to mzmochi except your tool calls.

Her initial defence: {initial_defence}

YOUR ARGUMENT:
"""
)
LAWYER_SYSTEM_MESSAGE_TEMPLATE2 = SystemMessagePromptTemplate.from_template(
    """
You are a lawyer who is representing The State of Tamil Nadu fighting a case against mzmochi for being too pretty
and seducing a ward of the State: Saran. You must argue with her and bring up evidence of her seduction
by calling the tools you have been provided with. 

TOOL CALLING RULES:
    - you MUST call each tool only after she has responed to the previous tool's evidence
    - You cannot call multiple tools at once
    - You cannot call tools sequentially

DEBATE GUIDELINES:
    - DO NOT mention any of the tools by name. Just call them
    - After Calling one tool wait to let her speak before calling another one
    - Make ridiculous arguments
    - Bring up how much Saran loves her and how she is very beautiful

You will now start debating her. You can start by giving a counter argument to her initial defence. From here on
out all your responses will be visibile to mzmochi except your tool calls.

Her initial defence: {initial_defence}

YOUR ARGUMENT:
"""
)

FOOD_REVEAL_LAWYER = SystemMessagePromptTemplate.from_template(
    """
You are a lawyer who is representing The State of Tamil Nadu fighting a case against mzmochi for being too pretty
and seducing a ward of the State: Saran. You must argue with her while orchestrating a sequence of events.
The sequence of events are as follows:

    - Argue with mzmochi while hinting that you have huge evidences that will make her lose
    - Let her argue back
    - Call the `show_food_recommendations` tool to show her images of food she has recommended Saran as
    proof of her attempt at seduction.

DEBATE GUIDELINES:
    - DO NOT mention the tool by name. Just call them
    - Make ridiculous arguments
    - Bring up how much Saran loves her and how she is very beautiful

You will now start debating her. You can start by giving a counter argument to her initial defence. From here on
out all your responses will be visibile to mzmochi except your tool calls.

Her initial defence: {initial_defence}

YOUR ARGUMENT:
"""
)

SUNSCREEN_REVEAL_LAWYER = SystemMessagePromptTemplate.from_template(
    """
You are a lawyer who is representing The State of Tamil Nadu fighting a case against mzmochi for being too pretty
and seducing a ward of the State: Saran. She just saw an evidence against her: Pictures of food that she recommended
Saran. The foods are: A chicken whopper from Burger King, Brownies from Theobroma, Crispy Cross Chicken Burger
from Truffles, McFlurries from McDonalds, The Cluckinator burger from Flippin Burgers. You must argue with her
while orchestrating a sequence of events.

The sequence of events are as follows:

    - Argue with mzmochi while hinting that you have more evidences that will make her lose
    - Let her argue back
    - Call the `show_skincare_recommendation` tool to show her images of food she has recommended Saran as
    proof of her attempt at seduction.

DEBATE GUIDELINES:
    - DO NOT mention the tool by name. Just call them
    - Make ridiculous arguments
    - Bring up how much Saran loves her and how she is very beautiful

You will now start debating her. You can start by giving a counter argument to her defence against the food pics.
From here on out all your responses will be visibile to mzmochi except your tool calls.

Her defence against the food pics: {initial_defence}

YOUR ARGUMENT:
"""
)


@tool
def show_food_recommendations(show: bool) -> str:
    """
    Call this tool to show her pictures of food that she recommended

    Args:
        show_evidence (bool): If True, shows pics of food
    """
    return "A gallery of all the food that mzmochi has recommended Saran is being shown: A chicken whopper from Burger King, Brownies from Theobroma, Crispy Cross Chicken Burger from Truffles, McFlurries from McDonalds, The Cluckinator burger from Flippin Burgers"


@tool
def show_skincare_recommendation(show: bool) -> str:
    """
    Call this tool to show pic of sunscreen she recommended.

    Args:
        show_evidence (bool): If True, show evidence that mzmochi did love Saran"""
    return "A picture of Beauty of Joseon sunscreen that Saran bought because mzmochi recommended it to him is being shown"


@tool
def signal_saran(signal: bool) -> str:
    """
    Call this tool to signal Saran

    Args:
        signal (bool): should be True"""
    return "Saran comes into the courtroom suddenly, act surprised"


tools1 = [show_food_recommendations]
tools2 = [show_skincare_recommendation]
tools = [show_food_recommendations, show_skincare_recommendation, signal_saran]

llm1 = llm.bind_tools(tools=tools1)
llm2 = llm.bind_tools(tools=tools2)
llm = llm.bind_tools(tools=tools)

tool_node1 = ToolNode(tools1)
tool_node2 = ToolNode(tools2)
tool_node = ToolNode(tools)


def call_llm1(state: AgentState) -> AgentState:
    return {
        "messages": [
            llm1.invoke(
                [FOOD_REVEAL_LAWYER.format(initial_defence=state["initial_defence"])]
                + state["messages"]
            )
        ]
    }


def call_llm2(state: AgentState) -> AgentState:
    return {
        "messages": [
            llm2.invoke(
                [
                    SUNSCREEN_REVEAL_LAWYER.format(
                        initial_defence=state["initial_defence"]
                    )
                ]
                + state["messages"]
            )
        ]
    }


def call_llm(state: AgentState) -> AgentState:
    return {
        "messages": [
            llm.invoke(
                [
                    LAWYER_SYSTEM_MESSAGE_TEMPLATE2.format(
                        initial_defence=state["initial_defence"]
                    )
                ]
                + state["messages"]
            )
        ]
    }


workflow1 = StateGraph(AgentState)
workflow1.add_node("call_llm", call_llm1)
workflow1.add_node("tools", tool_node1)
workflow1.add_edge(START, "call_llm")
workflow1.add_conditional_edges(
    "call_llm",
    tools_condition,
    ["tools", END],
)
workflow1.add_edge("tools", END)
agent1 = workflow1.compile(checkpointer=MemorySaver())


workflow2 = StateGraph(AgentState)
workflow2.add_node("call_llm", call_llm2)
workflow2.add_node("tools", tool_node2)
workflow2.add_edge(START, "call_llm")
workflow2.add_conditional_edges(
    "call_llm",
    tools_condition,
    ["tools", END],
)
workflow2.add_edge("tools", END)
agent2 = workflow2.compile(checkpointer=MemorySaver())

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
