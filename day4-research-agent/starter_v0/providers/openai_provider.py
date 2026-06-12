from __future__ import annotations

import json
import os
from typing import Any

from providers.base import ModelResponse, ToolCall


class OpenAIProvider:
    """OpenAI Chat Completions provider with normalized tool_calls output."""

    def __init__(
        self,
        *,
        api_key_env: str = "OPENAI_API_KEY",
        base_url: str | None = None,
        default_model: str = "gpt-4o-mini",
    ) -> None:
        self.api_key_env = api_key_env
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL") or os.getenv("LOCAL_LLM_TUNNEL_URL")
        self.default_model = default_model

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install live provider dependency first: pip install openai") from exc

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing API key env var: {self.api_key_env}")

        client = OpenAI(api_key=api_key, base_url=self.base_url)
        kwargs: dict[str, Any] = {
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
        if tool_choice is not None:
            kwargs["tool_choice"] = tool_choice

        primary_model = model or self.default_model
        
        # Build list of candidate models to try
        models_to_try = [primary_model]
        if self.api_key_env == "OPENROUTER_API_KEY":
            free_fallbacks = [
                "google/gemini-2.5-flash:free",
                "meta-llama/llama-3.1-8b-instruct:free",
                "qwen/qwen-2.5-72b-instruct:free",
                "deepseek/deepseek-r1:free",
            ]
            for m in free_fallbacks:
                if m != primary_model:
                    models_to_try.append(m)

        last_error = None
        for current_model in models_to_try:
            try:
                kwargs["model"] = current_model
                print(f"[Model Fallback] Trying model: {current_model}...")
                resp = client.chat.completions.create(**kwargs)
                msg = resp.choices[0].message
                calls: list[ToolCall] = []
                for call in msg.tool_calls or []:
                    args = json.loads(call.function.arguments or "{}")
                    calls.append(ToolCall(name=call.function.name, args=args))
                print(f"[Model Fallback] Successfully completed request with: {current_model}")
                return ModelResponse(text=msg.content, tool_calls=calls, raw=resp)
            except Exception as e:
                last_error = e
                print(f"[Model Fallback] Failed model {current_model}. Error: {e}")

        # If all candidates failed, raise the last error
        raise last_error
