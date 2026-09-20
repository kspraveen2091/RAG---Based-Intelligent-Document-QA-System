# -----------------------------
# Load environment variables
# -----------------------------

from dotenv import load_dotenv

load_dotenv()


# -----------------------------
# Error handling middleware
# -----------------------------


from langchain.agents.middleware import ModelRetryMiddleware, ToolCallRequest, ToolErrorMiddleware, ToolRetryMiddleware, ModelFallbackMiddleware


def on_error(exc: Exception, request: ToolCallRequest) -> str | None:
    if isinstance(exc, ValueError):
        return f"`{request.tool_call['name']}` failed with {type(exc).__name__}."
    # propagate everything else
    return None

tool_error = ToolErrorMiddleware(
    on_error=on_error
)



# =========================================================
# Tool Retry - ToolRetryMiddleware
# =========================================================
tool_retry = ToolRetryMiddleware(
    max_retries=2, # number of times should retry after the initial attempt failed
    backoff_factor=2.0, # controls how the delay grows between retries. delay = initial_delay × backoff_factor^retry_number
    initial_delay=1.0, # number of seconds to wait before the first retry
    max_delay=10.0, # prevents the delay from growing indefinitely
    jitter=True, # adds a small random variation to the retry delay
    on_failure="error",
    tools = ["get_weather", "tavily_search"] # controls which tools should retry
)


# ========================================================
# Model Retry - ModelRetryMiddleware
# ========================================================
model_retry = ModelRetryMiddleware(
    max_retries=2,
    backoff_factor=2.0,
    initial_delay=1.0,
    max_delay=10.0,
    jitter=True
)


# ========================================================
# Model Fallback - ModelFallbackMiddleware
# ========================================================

from langchain.chat_models import init_chat_model

model_1 = init_chat_model(
    "minimax/minimax-m3:free",
    model_provider="openrouter",
    temperature=0
)

model_2 = init_chat_model(
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    model_provider="openrouter",
    temperature=0
)


model_fallback = ModelFallbackMiddleware(
            model_1, model_2
        )


# ========================================================
# PII detection Middleware
# ========================================================

from langchain.agents.middleware import PIIMiddleware

# Redact email addresses from user input.
email_redaction = PIIMiddleware(
    "email",
    strategy="mask",
    apply_to_input=False,
)


# ========================================================
# Summarization Middleware
# ========================================================

from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openai/gpt-oss-20b",
    model_provider="openrouter",
    temperature=0
)
from langchain.agents.middleware import SummarizationMiddleware

summary_middleware = SummarizationMiddleware(
            model=model,
            trigger=("tokens", 4000),
            keep=("messages", 20),
        )



middlewares = [
    tool_error,
    tool_retry,
    model_retry,
    model_fallback,
    email_redaction,
    summary_middleware
]