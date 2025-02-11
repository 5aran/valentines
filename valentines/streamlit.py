# This website is designed to ask my girlfriend to be my Valentine
# The concept is to present the case for which she should be my Valentine
# and make her concede her case

from os import listdir
from uuid import uuid4

import streamlit as st
from agents import agent
from langchain_core.messages import AIMessage, HumanMessage
from PIL import Image
from utils import type_writer

# load all the images in images directory
if "food_pics" not in st.session_state:
    st.session_state["food_pics"] = [
        Image.open(f"images/food/{i}") for i in listdir("images/food")
    ]

if "PHASE" not in st.session_state:
    st.session_state["PHASE"] = "Summoning"

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = uuid4()


@st.dialog(title="A Gallery of Food mzmochi has reccommended to Saran")
def show_food():
    st.image(st.session_state["food_pics"], width=200)


@st.dialog(title="Sunscreen recommendation from mzmochi")
def show_sunscreen():
    st.image(
        "images/sunscreen/WhatsApp Image 2025-02-09 at 6.18.59 PM(6).jpeg", width=200
    )


async def stream_response(messages, initial_defence, thread_id):
    async for event in agent.astream_events(
        input={
            "messages": messages,
            "initial_defence": initial_defence,
        },
        config={"thread_id": thread_id},
        stream_mode="messages",
        version="v2",
    ):
        if (
            event["event"] == "on_chat_model_stream"
            and event["metadata"]["langgraph_node"] == "call_llm"
        ):
            yield event["data"]["chunk"].content
        elif (
            event["event"] == "on_tool_end"
            and event["name"] == "show_food_recommendations"
        ):
            show_food()
        elif (
            event["event"] == "on_tool_end"
            and event["name"] == "show_skincare_recommendation"
        ):
            show_sunscreen()


# Check which phase she is in
if st.session_state["PHASE"] == "Summoning":
    if "initial_defence" not in st.session_state:
        st.markdown("## The State of Tamil Nadu ⚖️ vs. mzmochi 💅🏼")
        cols = st.columns([1, 2.5])
        with cols[0]:
            st.image(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT92iwTeCowFAd3glBsM0Yo7BZ3LdJk1fZWig&s",
            )
        with cols[1]:
            chat = st.empty()
            # with chat:
            #     st.write_stream(
            #         type_writer(
            #             phrases=[
            #                 "MOCHI 😨...",
            #                 0.5,
            #                 "  \n.....",
            #                 0.5,
            #                 "  \n.....",
            #                 0.5,
            #                 "  \n.....",
            #                 1,
            #                 "  \n You have been summoned ! ! ! 😈",
            #                 2,
            #                 "  \n... to the Court of Love 💘",
            #                 3,
            #             ]
            #         )
            #     )
            # with chat:
            #     st.write_stream(
            #         type_writer(
            #             phrases=[
            #                 "The State of Tamil Nadu",
            #                 0.5,
            #                 "  \nhome of the prettiest women in the world,",
            #                 0.5,
            #                 "  \nwhere people flaunt their luscious hair, lathered in coconut oil,",
            #                 0.5,
            #                 "  \nis filing a case against you 🫵🏻 !",
            #                 3,
            #             ]
            #         )
            #     )
            # with chat:
            #     st.write_stream(
            #         type_writer(
            #             phrases=[
            #                 "  \n For being too pretty",
            #                 0.5,
            #                 "  \nAnd seducing a ward of the State",
            #                 0.5,
            #                 "  \none Mr. Saran K",
            #                 3,
            #             ]
            #         )
            #     )
            with chat:
                st.write_stream(
                    type_writer(
                        phrases=[
                            # "  \nYou are hereby summoned to defend yourself",
                            # 0.5,
                            "  \nAnd make your case",
                            # 2,
                        ],
                        letters_per_sec=35,
                    )
                )

    if initial_defence := st.text_input(
        label="initial_defence",
        key="initial_defence",
        placeholder="What do you have to say for yourself?",
        label_visibility="hidden",
    ):
        st.session_state["PHASE"] = "Lawyer Reveal"
        st.session_state["messages"] = [HumanMessage(content=initial_defence)]
        st.session_state["initial_defence_value"] = initial_defence
        st.rerun()

elif st.session_state["PHASE"] == "Lawyer Reveal":
    if "Clicked Start Argumentation" not in st.session_state:
        # Make a mockery of her initial defence by repeating it in
        # alteranting case
        mock_initial_defence = ""
        odd = True
        for c in " ".join(st.session_state["initial_defence_value"].split()[:5]):
            if odd:
                mock_initial_defence = mock_initial_defence + c.upper()
            else:
                mock_initial_defence = mock_initial_defence + c.lower()
            odd = not odd
        cols = st.columns([1, 2.5])
        with cols[1]:
            chat = st.empty()
            with chat:
                st.write_stream(
                    type_writer(
                        phrases=[
                            ".....",
                            0.5,
                            f"{mock_initial_defence} seriously?",
                            1,
                            "  \nYou really think you can win with that?",
                            1.5,
                            # "  \nThe audacity",
                            # 0.5,
                            # "  \nThe gall",
                            # 0.5,
                            # "  \nThe gumption",
                            # 0.5,
                            # "  \nThe nerve",
                            # 0.5,
                            # "  \nThe temerity",
                            # 0.5,
                            # "  \nThe chutzpah",
                            # 0.5,
                            # "  \nThe brass",
                            # 0.5,
                            # "  \nThe effrontery",
                            # 0.5,
                            # "  \nThe impudence",
                            # 0.5,
                            # "  \nThe insolence",
                            # 0.5,
                            # "  \nThe impertinence",
                            # 0.5,
                            # "  \nThe rudeness",
                            # 0.5,
                            # "  \nThe presumption",
                            # 0.5,
                            # "  \nThe cheek",
                        ]
                    )
                )
        with cols[0]:
            st.image(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqPP0EROzzr9W643kfKswLqmFuNfbFA4pDWA&s",
                width=200,
                caption="BOOM! 💥",
            )
        with cols[1]:
            with chat:
                st.write_stream(
                    type_writer(
                        phrases=[
                            "  \nTO TALK BACK ! ! !",
                            2,
                            "  \nI'll be representing this poor boy you siren!",
                            2,
                        ]
                    )
                )
    if st.button(label="Start Argumentation", key="Clicked Start Argumentation"):
        st.session_state["PHASE"] = "Argumentation"
        st.rerun()

elif st.session_state["PHASE"] == "Argumentation":
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("ai"):
                st.markdown(message.content)
    if prompt := st.chat_input("SPEAK UP BITCH!!!"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(
            stream_response(
                messages=st.session_state.messages,
                initial_defence=st.session_state.initial_defence_value,
                thread_id=st.session_state.thread_id,
            )
        )
    st.session_state.messages.append(AIMessage(content=response))

elif st.session_state["PHASE"] == "End":
    st.header("I LOVE YOU POOKIE")
