# This website is designed to ask my girlfriend to be my Valentine
# The concept is to present the case for which she should be my Valentine
# and make her concede her case

from time import sleep

import streamlit as st
from utils import type_writer

if "PHASE" not in st.session_state:
    st.session_state["PHASE"] = 1.1

# Check which phase she is in
if st.session_state["PHASE"] < 2:
    st.markdown("## The State of Tamil Nadu ⚖️ vs. mzmochi 💅🏼")
    cols = st.columns(3)
    with cols[0]:
        st.image(
            "https://www.capecodtimes.com/gcdn/authoring/2013/09/08/NCCT/ghows-CC-417faa57-519f-4a10-bef3-bc32d6118801-b8b281a6.jpeg?width=1200&disable=upscale&format=pjpg&auto=webp",
            width=200,
        )
    with cols[1]:
        sleep(1)
        if st.session_state["PHASE"] == 1.1:
            chat = st.empty()
            with chat:
                st.write_stream(
                    type_writer(
                        phrases=[
                            "MOCHI 😨...",
                            0.5,
                            "  \n.....",
                            0.5,
                            "  \n.....",
                            0.5,
                            "  \n.....",
                            1,
                            "  \n You have been summoned ! ! ! 😈",
                            2,
                            "  \n... to the Court of Love 💘",
                            1,
                        ]
                    )
                )
            with chat:
                st.write_stream(
                    type_writer(
                        phrases=[
                            "The State of Tamil Nadu",
                            0.5,
                            "  \nhome of the prettiest women in the world,",
                            0.5,
                            "  \nwhere people flaunt their luscious hair, lathered in coconut oil,",
                            0.5,
                            "  \naccuses you of being the",
                            0.5,
                            "  \n",
                            0.5,
                            "  \naccuses you of being the",
                            0.5,
                            "  \naccuses you of being the",
                            1,
                            "is now in session",
                        ]
                    )
                )
