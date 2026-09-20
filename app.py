import streamlit as st
import uuid

from chat_db import (
    create_chat,
    get_chats,
    create_chat_table,
    update_chat_name
)

from agent import agent


# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# User
# =========================================================

USER_ID = "user_1"


# =========================================================
# Initialize database
# =========================================================

create_chat_table()


# =========================================================
# Session state
# =========================================================

if "current_chat" not in st.session_state:

    st.session_state.current_chat = None


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.title("💬 Chats")


    # -----------------------------------------------------
    # New Chat
    # -----------------------------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        thread_id = str(uuid.uuid4())

        existing_chats = get_chats(USER_ID)

        chat_number = len(existing_chats) + 1

        chat_name = f"Chat {chat_number}"

        create_chat(
            USER_ID,
            thread_id,
            chat_name
        )

        st.session_state.current_chat = thread_id

        st.rerun()


    st.divider()


    # -----------------------------------------------------
    # Existing Chats
    # -----------------------------------------------------

    chats = get_chats(USER_ID)

    for thread_id, chat_name in chats:

        if st.button(
            chat_name,
            key=f"chat_{thread_id}",
            use_container_width=True
        ):

            st.session_state.current_chat = thread_id

            st.rerun()


# =========================================================
# Select first chat if no chat is selected
# =========================================================

if st.session_state.current_chat is None:

    chats = get_chats(USER_ID)

    if chats:

        st.session_state.current_chat = chats[0][0]

    else:

        thread_id = str(uuid.uuid4())

        create_chat(
            USER_ID,
            thread_id,
            "Chat 1"
        )

        st.session_state.current_chat = thread_id


thread_id = st.session_state.current_chat


# =========================================================
# Find current chat name
# =========================================================

chats = get_chats(USER_ID)

current_chat_name = next(
    (
        chat_name
        for chat_thread_id, chat_name in chats
        if chat_thread_id == thread_id
    ),
    "New Chat"
)


# =========================================================
# Page title
# =========================================================

st.title("🤖 AI Agent")

st.caption(
    f"Current chat: {current_chat_name}"
)


# =========================================================
# Load conversation history from LangGraph
# =========================================================

state = agent.get_state(
    {
        "configurable": {
            "thread_id": thread_id
        }
    }
)


messages = state.values.get(
    "messages",
    []
)


# =========================================================
# Display previous messages
# =========================================================

for message in messages:

    # human → user
    # ai    → assistant

    if message.type == "human":

        role = "user"

    elif message.type == "ai":

        role = "assistant"

    else:

        continue


    with st.chat_message(role):

        st.write(message.content)


# =========================================================
# User input
# =========================================================

question = st.chat_input(
    "Ask your agent something..."
)


# =========================================================
# Run agent
# =========================================================

if question:


    # =====================================================
    # Automatically name a new chat
    # =====================================================

    chats = get_chats(USER_ID)

    current_chat_name = next(
        (
            chat_name
            for chat_thread_id, chat_name in chats
            if chat_thread_id == thread_id
        ),
        None
    )


    if (
        current_chat_name
        and current_chat_name.startswith("Chat ")
    ):

        new_chat_name = question.strip()

        if len(new_chat_name) > 40:

            new_chat_name = (
                new_chat_name[:40]
                + "..."
            )


        update_chat_name(
            thread_id,
            new_chat_name
        )


    # =====================================================
    # Display user message
    # =====================================================

    with st.chat_message("user"):

        st.write(question)


    # =====================================================
    # Agent configuration
    # =====================================================

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }


    # =====================================================
    # Long-term memory identity
    # =====================================================

    context = {
        "user_id": USER_ID
    }


    # =====================================================
    # Run agent with ALL streaming modes
    # =====================================================

    with st.chat_message("assistant"):

        # Container for token-by-token response
        response_container = st.empty()

        # Store streamed answer
        answer = ""


        # -------------------------------------------------
        # Start streaming
        # -------------------------------------------------

        for stream_mode, chunk in agent.stream(

            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },

            stream_mode=[
                "updates",
                "messages",
                "custom"
            ],

            config=config,

            context=context
        ):


            # =================================================
            # 1. UPDATES
            # =================================================

            if stream_mode == "updates":

                print(
                    "\n========== UPDATE =========="
                )

                print(chunk)

                print(
                    "============================"
                )


            # =================================================
            # 2. MESSAGES
            # =================================================

            elif stream_mode == "messages":

                message_chunk, metadata = chunk


                # Only process chunks containing text
                if message_chunk.content:

                    answer += message_chunk.content

                    response_container.markdown(
                        answer
                    )


            # =================================================
            # 3. CUSTOM
            # =================================================

            elif stream_mode == "custom":

                print(
                    "\n========== CUSTOM =========="
                )

                print(chunk)

                print(
                    "============================"
                )