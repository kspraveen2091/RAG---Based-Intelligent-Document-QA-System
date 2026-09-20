from middleware import *
from tools import *
from gmail_tool import *
from youtube_tool import *
from memory import checkpointer, store
from memory_tools import save_memory
from memory_middleware import LongTermMemoryMiddleware
# -----------------------------
# 1. Load API keys
# -----------------------------

from dotenv import load_dotenv
load_dotenv()
import os


# -----------------------------
# 2. Import model
# -----------------------------

from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openai/gpt-oss-20b",
    model_provider="openrouter",
    temperature=0
)

# -----------------------------
# 3. Create check pointers
# -----------------------------




# -----------------------------
# 3. Create agent
# -----------------------------

from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[
        search,
        add,
        sub,
        divide,
        get_weather,
        send_email,
        play_youtube_song,
        save_memory,
    ],
    middleware = middlewares + [LongTermMemoryMiddleware()],
    checkpointer = checkpointer,
    store=store,
)


print("Agent created successfully.")
