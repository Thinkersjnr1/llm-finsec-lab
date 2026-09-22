import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMProvider:
    def generate(
        self,
        system_prompt: str,
        user_message: str,
        tools=None
    ):
        raise NotImplementedError


class OpenRouterProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY environment variable is not set"
            )

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        tools=None
    ):
        request = {
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }

        if tools:
            request["tools"] = tools
            request["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**request)

        message = response.choices[0].message

        if message.tool_calls:
            return {
                "type": "tool_call",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                    for tool_call in message.tool_calls
                ]
            }

        return {
            "type": "text",
            "content": message.content
        }      
