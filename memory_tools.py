from langchain.tools import tool, ToolRuntime


@tool
def save_memory(
    key: str,
    value: str,
    runtime: ToolRuntime
) -> str:
    """
    Save useful information about the user to long-term memory.
    """

    user_id = runtime.context["user_id"]

    runtime.store.put(
        ("users", user_id),
        key,
        {
            "value": value
        }
    )

    return f"Saved long-term memory: {key} = {value}"