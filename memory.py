from pathlib import Path
from dotenv import load_dotenv
import os

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore


# =========================================================
# Load environment variables
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]


# =========================================================
# Create PostgreSQL connections
# =========================================================

checkpointer_context = PostgresSaver.from_conn_string(
    DATABASE_URL
)

store_context = PostgresStore.from_conn_string(
    DATABASE_URL
)


# =========================================================
# Enter the context managers
# =========================================================

checkpointer = checkpointer_context.__enter__()

store = store_context.__enter__()


print("PostgreSQL memory objects created successfully.")