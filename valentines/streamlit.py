# This website is designed to ask my girlfriend to be my Valentine
# The concept is to present the case for which she should be my Valentine
# and make her concede her case

import logging
from uuid import uuid4

import streamlit as st
from agents import agent
from langchain_core.messages import AIMessage, HumanMessage
from utils import type_writer

logger = logging.getLogger()
logger.level = logging.INFO

if "PHASE" not in st.session_state:
    st.session_state["PHASE"] = "Summoning"

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = uuid4()


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
        elif event["event"] == "on_tool_start" and event["name"] == "accept_concession":
            st.session_state["PHASE"] = "FINAL"


# Check which phase she is in
if st.session_state["PHASE"] == "Summoning":
    if "initial_defence" not in st.session_state:
        st.markdown("## The State of Tamil Nadu ⚖️ vs. Nehneva ")
        cols = st.columns([1, 2.5])
        with cols[0]:
            st.image(
                "https://c.ndtvimg.com/2024-11/gv48bav_dy-chandrachud-ians_625x300_08_November_24.jpeg",
            )
        logger.info("Showing pic of CJI")
        with cols[1]:
            chat = st.empty()
            with chat:
                st.write_stream(
                    type_writer(
                        phrases=[
                            "Syedah Tahniyat Sadaat Mosavi...",
                            0.5,
                            "  \n aka Nehneva",
                            0.5,
                            "  \n The State of Tamil Nadu",
                            0.5,
                            "  \nis filing a case against you!",
                            3,
                        ]
                    )
                )
            logger.info("Said: 'State Of Tamil Nadu is filing a case against you'")
            with chat:
                st.write_stream(
                    type_writer(
                        phrases=[
                            "  \n For being too pretty",
                            0.5,
                            "  \nAnd seducing a ward of the State",
                            0.5,
                            "  \none Mr. Saran K",
                            3,
                        ]
                    )
                )
            logger.info("Said: 'For being too pretty and seducing Saran'")
            with chat:
                st.write_stream(
                    type_writer(
                        phrases=[
                            "  \nYou are hereby summoned to defend yourself",
                            0.5,
                            "  \nAnd make your case",
                            2,
                        ],
                    )
                )
            logger.info("Said: 'Defend yourself'")

    if initial_defence := st.text_input(
        label="initial_defence",
        key="initial_defence",
        placeholder="What do you have to say for yourself?",
        label_visibility="hidden",
    ):
        logger.info(f"Initial Defence Given: {initial_defence}")
        st.session_state["PHASE"] = "Argumentation"
        st.session_state["messages"] = [HumanMessage(content=initial_defence)]
        st.session_state["initial_defence_value"] = initial_defence
        st.rerun()


elif st.session_state["PHASE"] == "Argumentation":
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("ai"):
                st.markdown(message.content)
    if prompt := st.chat_input("Respond"):
        logger.info(f"Nehneva argues: {prompt}")
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
        logger.info(f"bot argues: {response}")
    st.session_state.messages.append(AIMessage(content=response))

elif st.session_state["PHASE"] == "FINAL":
    st.title("Will you be my Valentine Princess? 💝")
    st.markdown(
        """Now that you've confessed to your witch-like charm over my heart
You have to concede to one of the following? ......
......as an ailment to my aching heart? 🥺👉🏻👈🏻"""
    )
    cols = st.columns(3)
    with cols[0]:
        if hand := st.button(label="Hand Holding Rights"):
            st.write("assa")
    with cols[1]:
        if cheek := st.button(label="Cheek Pinching/Squishing Rights"):
            st.write("assa")
    with cols[2]:
        if poem := st.button(label="A Poem"):
            st.write("assa")
