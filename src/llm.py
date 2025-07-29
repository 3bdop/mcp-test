from enum import StrEnum, auto

from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings,
)

from src.config import settings

SERVICE_ID = "default"


class ChatService(StrEnum):
    OPENAI = auto()
    AZURE_OPENAI = auto()


def get_llm(
    chat_service: ChatService = ChatService.AZURE_OPENAI,
    instructions: str | None = None,
) -> ChatCompletionClientBase:
    """Get chat completion service."""
    return {
        ChatService.AZURE_OPENAI: lambda: AzureChatCompletion(
            service_id=SERVICE_ID,
            endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            deployment_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            instruction_role=instructions,
        ),
    }[chat_service]()


def get_llm_settings(chat_service: ChatService) -> PromptExecutionSettings:
    return {
        ChatService.AZURE_OPENAI: lambda: AzureChatPromptExecutionSettings(
            service_id=SERVICE_ID
        ),
    }[chat_service]()


def get_llm_and_settings(
    chat_service: ChatService = ChatService.AZURE_OPENAI,
    *,
    instructions: str | None = None,
) -> tuple[ChatCompletionClientBase, PromptExecutionSettings]:
    return get_llm(
        chat_service=chat_service, instructions=instructions
    ), get_llm_settings(chat_service=chat_service)
