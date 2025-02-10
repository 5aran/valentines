# This website is designed to ask my girlfriend to be my Valentine
# The concept is to present the case for which she should be my Valentine
# and make her concede her case

from time import sleep
from uuid import uuid4

import streamlit as st
from agents import agent
from langchain_core.messages import HumanMessage
from utils import type_writer

if "PHASE" not in st.session_state:
    st.session_state["PHASE"] = 1
else:
    st.session_state["PHASE"] += 1

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = uuid4()

# Check which phase she is in
if st.session_state["PHASE"] == 1:
    st.markdown("## The State of Tamil Nadu ⚖️ vs. mzmochi 💅🏼")
    cols = st.columns([1, 2.5])
    with cols[0]:
        st.image(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT92iwTeCowFAd3glBsM0Yo7BZ3LdJk1fZWig&s",
        )
    with cols[1]:
        sleep(1)
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
                        "  \nYou are hereby summoned to defend yourself",
                        # 0.5,
                        # "  \nAnd make your case",
                        # 2,
                    ],
                    letters_per_sec=25,
                )
            )

    if her_defence := st.text_input(
        label="her_defence",
        key="her_defence",
        placeholder="What do you have to say for yourself?",
        label_visibility="hidden",
    ):
        st.session_state["her_defence"] = her_defence

elif st.session_state["PHASE"] == 2:
    agent_input = [
        HumanMessage(
            content=f"""You are a lawyer who is fighting a fictional case against mzmochi. She has been accused of
being too pretty and seducing a ward of the State: Mr. Saran K. She has been summoned to defend herself
and make her case. She will be giving her defense in the chat. You have to make her concede her case. This
is purely comical and for entertainment purposes. Make sure to keep the conversation light-hearted and fun.
Ridiculous argumentation is encouraged.

MzMochi's defense against the charges is: {st.session_state["her_defence"]}

Now give a counter argument to make her concede her case.

After three turns show her evidence that she did love Saran""",
        )
    ]
    config = {"thread_id": st.session_state["thread_id"]}

    async def stream_response():
        async for event in agent.astream_events(
            input={"messages": agent_input},
            config=config,
            stream_mode="messages",
            version="v2",
        ):
            if event["event"] == "on_chat_model_stream" and "chunk" in event["data"]:
                yield event["data"]["chunk"].content

    st.write_stream(stream_response())
