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
# Initialize short-term memory tables
# =========================================================

with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
    checkpointer.setup()


# =========================================================
# Initialize long-term memory tables
# =========================================================

with PostgresStore.from_conn_string(DATABASE_URL) as store:
    store.setup()


print("PostgreSQL memory tables initialized successfully.")