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


LAWYER_SYSTEM_MESSAGE_TEMPLATE = SystemMessagePromptTemplate.from_template("""You are a lawyer who is fighting a fictional case against mzmochi. She has been accused of
being too pretty and seducing a ward of the State: Mr. Saran K. She has been summoned to defend herself
and make her case. She will be giving her defense. You have to make her concede her case. This
is purely comical and for entertainment purposes. Ridiculous argumentation is encouraged.
Slowly nudge the conversation into a direction where you can show her evidence that she did love Saran
by showing her pictures of food that she recommended to him, a skincare product he bought because of her.
You can do this by calling the tools show_food_recommendations and show_skincare_recommendation.
Don't mention the tools directly in the conversation.

YOU MUST SHOW THE EVIDENCE ONE BY ONE. After calling one of the tools let mzmochi speak at least once before calling the next tool.
MzMochi's defense against the charges is: {initial_defence}

Now give a counter argument. She will then give a counter argument to your counter argument.
""")


@tool
def show_food_recommendations(show: bool) -> str:
    """
    Call this tool to show evidence that mzmochi did love Saran by showing her pictures of food that she recommended to him.

    Args:
        show_evidence (bool): If True, show evidence that mzmochi did love Saran"""
    return "A gallery of all the food that mzmochi has recommended Saran is being shown: A chicken whopper from Burger King, Brownies from Theobroma, Crispy Cross Chicken Burger from Truffles, McFlurries from McDonalds, The Cluckinator burger from Flippin Burgers"


@tool
def show_skincare_recommendation(show: bool) -> str:
    """
    Call this tool to show evidence that mzmochi did love Saran by showing her pictures of food that she recommended to him.

    Args:
        show_evidence (bool): If True, show evidence that mzmochi did love Saran"""
    return "A picture of Beauty of Joseon sunscreen that Saran bought because mzmochi recommended it to him is being shown"


tools = [show_food_recommendations, show_skincare_recommendation]
llm_with_tools = llm.bind_tools(tools=tools)

tool_node = ToolNode(tools)


def call_llm(state: AgentState) -> AgentState:
    return {
        "messages": [
            llm_with_tools.invoke(
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
