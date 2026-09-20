from langchain.agents.middleware import AgentMiddleware


class LongTermMemoryMiddleware(AgentMiddleware):

    def before_model(self, state, runtime):

        user_id = runtime.context["user_id"]

        memories = runtime.store.search(
            ("users", user_id)
        )

        if not memories:
            return None

        memory_text = "\n".join(
            f"- {item.key}: {item.value}"
            for item in memories
        )

        return {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Here are the user's long-term memories. "
                        "Use them when relevant to the user's request:\n\n"
                        + memory_text
                    )
                }
            ]
        }