import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]


def create_chat_table():

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    user_id TEXT NOT NULL,
                    thread_id TEXT PRIMARY KEY,
                    chat_name TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

        conn.commit()


def create_chat(user_id, thread_id, chat_name):

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO chats
                    (user_id, thread_id, chat_name)
                VALUES
                    (%s, %s, %s)
                """,
                (user_id, thread_id, chat_name)
            )

        conn.commit()

def update_chat_name(thread_id, chat_name):

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                UPDATE chats
                SET chat_name = %s
                WHERE thread_id = %s
                """,
                (chat_name, thread_id)
            )

        conn.commit()
        
def get_chats(user_id):

    with psycopg.connect(DATABASE_URL) as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT thread_id, chat_name
                FROM chats
                WHERE user_id = %s
                ORDER BY created_at
                """,
                (user_id,)
            )

            return cur.fetchall()


if __name__ == "__main__":

    create_chat_table()

    print("Chat table created successfully.")