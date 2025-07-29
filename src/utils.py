from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)
from semantic_kernel.contents import ChatHistory
from semantic_kernel.kernel import Kernel
from src.llm import get_llm_and_settings

llm, settings = get_llm_and_settings()
settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

history = ChatHistory()
kernel = Kernel()


async def chat(
    kernel: Kernel = kernel,
    *,
    llm: ChatCompletionClientBase = llm,
    settings: PromptExecutionSettings = settings,
) -> bool:
    """
    Continuously prompt the user for input and show the assistant's response.
    Type 'exit' to exit.
    """
    try:
        user_input = input("User:> ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting chat...")
        return False
    if user_input.lower().strip() == "exit":
        print("\n\nExiting chat...")
        return False

    history.add_user_message(user_input)
    result = await llm.get_chat_message_content(history, settings, kernel=kernel)
    if result:
        print(f"Assistant:> {result}")
        history.add_message(result)

    return True
