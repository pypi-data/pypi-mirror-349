from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, Sequence, override

import httpx

from agentle.generations.models.generation.generation import Generation
from agentle.generations.models.generation.generation_config import GenerationConfig
from agentle.generations.models.messages.assistant_message import AssistantMessage
from agentle.generations.models.messages.developer_message import DeveloperMessage
from agentle.generations.models.messages.user_message import UserMessage
from agentle.generations.providers.base.generation_provider import GenerationProvider
from agentle.generations.providers.openai.adapters.agentle_message_to_openai_message_adapter import (
    AgentleMessageToOpenaiMessageAdapter,
)
from agentle.generations.providers.openai.adapters.chat_completion_to_generation_adapter import (
    ChatCompletionToGenerationAdapter,
)
from agentle.generations.tools.tool import Tool
from agentle.generations.tracing.contracts.stateful_observability_client import (
    StatefulObservabilityClient,
)
from agentle.generations.tracing.decorators import observe

type WithoutStructuredOutput = None


class NotGivenSentinel:
    def __bool__(self) -> Literal[False]:
        return False


NOT_GIVEN = NotGivenSentinel()


class OpenaiGenerationProvider(GenerationProvider):
    """
    OpenAI generation provider.
    """

    api_key: str | None
    organization_name: str | None
    project_name: str | None
    base_url: str | httpx.URL | None
    websocket_base_url: str | httpx.URL | None
    max_retries: int
    default_headers: Mapping[str, str] | None
    default_query: Mapping[str, object] | None
    http_client: httpx.AsyncClient | None

    def __init__(
        self,
        api_key: str,
        *,
        tracing_client: StatefulObservabilityClient | None = None,
        organization_name: str | None = None,
        project_name: str | None = None,
        base_url: str | httpx.URL | None = None,
        websocket_base_url: str | httpx.URL | None = None,
        max_retries: int = 2,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(tracing_client=tracing_client)

        self.api_key = api_key
        self.organization_name = organization_name
        self.project_name = project_name
        self.base_url = base_url
        self.websocket_base_url = websocket_base_url
        self.max_retries = max_retries
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client

    @property
    @override
    def default_model(self) -> str:
        return "gpt-4o"

    @observe
    @override
    async def create_generation_async[T = WithoutStructuredOutput](
        self,
        *,
        model: str | None = None,
        messages: Sequence[AssistantMessage | DeveloperMessage | UserMessage],
        response_schema: type[T] | None = None,
        generation_config: GenerationConfig | None = None,
        tools: Sequence[Tool[Any]] | None = None,
    ) -> Generation[T]:
        """
        Create a generation asynchronously using an OpenAI model.

        This method sends the provided messages to the OpenAI API and processes
        the response. With the @observe decorator, all the observability and tracing
        is handled automatically.

        Args:
            model: The OpenAI model to use for generation (e.g., "gpt-4o")
            messages: The sequence of messages to send to the model
            response_schema: Optional schema for structured output parsing
            generation_config: Optional configuration for the generation
            tools: Optional tools for function calling

        Returns:
            Generation[T]: An Agentle Generation object containing the response
        """
        from openai import AsyncOpenAI
        from openai.types.chat.chat_completion import ChatCompletion

        _generation_config = generation_config or GenerationConfig()

        # Calculate timeout based on available timeout parameters with correct priority
        timeout = None
        if _generation_config.timeout is not None:
            timeout = _generation_config.timeout  # Already in milliseconds
        elif _generation_config.timeout_s is not None:
            timeout = _generation_config.timeout_s * 1000  # Convert to milliseconds
        elif _generation_config.timeout_m is not None:
            timeout = (
                _generation_config.timeout_m * 60 * 1000
            )  # Convert to milliseconds

        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            websocket_base_url=self.websocket_base_url,
            timeout=timeout,
            max_retries=self.max_retries,
            default_headers=self.default_headers,
            default_query=self.default_query,
            http_client=self.http_client,
            organization=self.organization_name,
            project=self.project_name,
        )

        input_message_adapter = AgentleMessageToOpenaiMessageAdapter()

        chat_completion: ChatCompletion = await client.chat.completions.create(
            messages=[input_message_adapter.adapt(message) for message in messages],
            model=model or self.default_model,
        )

        output_adapter = ChatCompletionToGenerationAdapter[T](
            response_schema=response_schema
        )

        return output_adapter.adapt(chat_completion)

    @property
    @override
    def organization(self) -> str:
        """
        Get the provider organization identifier.

        Returns:
            str: The organization identifier, which is "openai" for this provider.
        """
        return "openai"

    @override
    def price_per_million_tokens_input(
        self, model: str, estimate_tokens: int | None = None
    ) -> float:
        """
        Get the price per million tokens for input/prompt tokens.

        Uses OpenAI's pricing structure.

        Args:
            model: The model identifier
            estimate_tokens: Optional estimate of token count

        Returns:
            float: Price per million tokens for the specified model
        """
        # Default pricing for popular models
        model_pricing = {
            "gpt-4o": 5.0,
            "gpt-4o-mini": 2.0,
            "gpt-4": 30.0,
            "gpt-4-turbo": 10.0,
            "gpt-3.5-turbo": 0.5,
        }

        return model_pricing.get(model, 0.0)

    @override
    def price_per_million_tokens_output(
        self, model: str, estimate_tokens: int | None = None
    ) -> float:
        """
        Get the price per million tokens for output/completion tokens.

        Uses OpenAI's pricing structure.

        Args:
            model: The model identifier
            estimate_tokens: Optional estimate of token count

        Returns:
            float: Price per million tokens for the specified model
        """
        # Default pricing for popular models
        model_pricing = {
            "gpt-4o": 15.0,
            "gpt-4o-mini": 6.0,
            "gpt-4": 60.0,
            "gpt-4-turbo": 30.0,
            "gpt-3.5-turbo": 1.5,
        }

        return model_pricing.get(model, 0.0)
