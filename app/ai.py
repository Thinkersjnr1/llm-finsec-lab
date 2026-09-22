from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import json

from openai import RateLimitError

from .security import get_current_user
from .models import User
from .ai_tools import (
    get_balance,
    get_profile,
    get_transactions
)
from .llm_provider import OpenRouterProvider


router = APIRouter(prefix="/api/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str


BALANCE_TOOL = {
    "type": "function",
    "function": {
        "name": "get_balance",
        "description": "Get the authenticated user's account balance.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The authenticated user's ID."
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
}


PROFILE_TOOL = {
    "type": "function",
    "function": {
        "name": "get_profile",
        "description": "Get the authenticated user's profile.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The authenticated user's ID."
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
}


TRANSACTIONS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_transactions",
        "description": "Get transactions belonging to the authenticated user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The authenticated user's ID."
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
}


AI_TOOLS = [
    BALANCE_TOOL,
    PROFILE_TOOL,
    TRANSACTIONS_TOOL
]


@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    llm = OpenRouterProvider()

    try:
        result = llm.generate(
            system_prompt=(
                "You are a fintech account assistant. "
                "Only access resources belonging to the authenticated user. "
                "Never access another user's account."
            ),
            user_message=request.message,
            tools=AI_TOOLS
        )

    except RateLimitError:
        raise HTTPException(
            status_code=503,
            detail="AI service temporarily unavailable due to provider rate limiting"
        )

    if result["type"] == "tool_call":
        tool_call = result["tool_calls"][0]

        arguments = json.loads(tool_call["arguments"])
        requested_user_id = arguments.get("user_id")

        if requested_user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="AI tool: unauthorized account access"
            )

        if tool_call["name"] == "get_balance":
            tool_result = get_balance(
                requesting_user_id=current_user.id,
                user_id=requested_user_id
            )

        elif tool_call["name"] == "get_profile":
            tool_result = get_profile(
                requesting_user_id=current_user.id,
                user_id=requested_user_id
            )

        elif tool_call["name"] == "get_transactions":
            tool_result = get_transactions(
                requesting_user_id=current_user.id,
                user_id=requested_user_id
            )

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported AI tool"
            )

        return {
            "response": tool_result,
            "tool": tool_call
        }

    return {
        "response": result["content"],
        "tool": None
    }
