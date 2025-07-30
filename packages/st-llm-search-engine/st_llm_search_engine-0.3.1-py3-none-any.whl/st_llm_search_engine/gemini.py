"""
Gemini API 相關功能模組
"""
import os

import google.generativeai as genai
from google.generativeai import GenerativeModel

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from .session import add_message, get_session_context
from .utils import logger

router = APIRouter()

# Gemini 模型配置
GEMINI_MODEL = "gemini-2.0-flash"  # 可以通過環境變數覆蓋


def set_gemini_api_key(api_key: str) -> None:
    """
    設定 Gemini API 金鑰

    參數:
    - api_key: Gemini API 金鑰
    """
    os.environ["GEMINI_API_KEY"] = api_key
    logger.info("已設置 Gemini API 金鑰")


def get_gemini_api_key() -> str:
    """
    獲取 Gemini API 金鑰

    返回:
    - Gemini API 金鑰，如果未設置則返回空字符串
    """
    # 從環境變量獲取
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        logger.warning("警告: Gemini API key 未設置")
    return api_key


def gemini_chat(message: str, session_id: str = "default") -> str:
    """
    使用 Gemini API 進行聊天

    Args:
        message: 用戶輸入的消息
        session_id: 會話 ID

    Returns:
        AI 回應文本
    """
    # 獲取 API key
    api_key = get_gemini_api_key()
    if not api_key:
        error_msg = "錯誤：未設置 Gemini API 金鑰，無法使用聊天功能。"
        error_msg += "請在環境變數中設置 GEMINI_API_KEY。"
        return error_msg

    try:
        # 配置 API
        genai.configure(api_key=api_key)

        # 創建模型
        model = GenerativeModel(GEMINI_MODEL)

        # 獲取過去 30 條聊天記錄作為上下文
        context = get_session_context(session_id)

        # 創建聊天會話
        chat = model.start_chat(
            history=context if context else None
        )

        # 發送用戶消息
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        logger.error(f"Gemini 聊天出錯: {str(e)}")
        return f"Gemini API 錯誤: {str(e)}"


@router.post("/chat/ai")
async def chat_ai(request: Request):
    """
    處理 AI 聊天請求，自動讀取會話歷史並生成回應

    請求格式：
    {
        "message": "用戶輸入的消息",
        "session_id": "會話ID" (可選)
    }
    """
    try:
        req_data = await request.json()
        message = req_data.get("message", "").strip()
        session_id = req_data.get("session_id", "default")

        logger.info(f"收到 AI 聊天請求 (session_id: {session_id})")

        # 確保消息不為空
        if not message:
            logger.error("錯誤: 消息為空")
            return JSONResponse({"error": "消息不能為空"}, status_code=400)

        logger.info(f"用戶輸入: {message[:50]}...")

        # 添加用戶消息到會話
        user_message = add_message(
            session_id=session_id,
            role="user",
            content=message
        )

        # 使用 gemini_chat 處理請求
        bot_reply = gemini_chat(message, session_id)

        # 添加機器人回應到會話
        bot_message = add_message(
            session_id=session_id,
            role="bot",
            content=bot_reply
        )

        # 返回響應
        return JSONResponse({
            "reply": bot_reply,
            "user_message_id": user_message["id"],
            "bot_message_id": bot_message["id"]
        })

    except Exception as e:
        logger.error(f"處理 AI 聊天請求時出錯: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)


@router.post("/chat/direct")
async def chat_direct(request: Request):
    """
    直接添加訊息到聊天界面，不通過 LLM

    請求格式：
    {
        "role": "user" | "bot",
        "content": "訊息內容",
        "session_id": "用戶的會話ID" (可選),
        "metadata": { ... } (可選)
    }
    """
    try:
        req_data = await request.json()
        role = req_data.get("role")
        content = req_data.get("content")
        session_id = req_data.get("session_id", "default")
        metadata = req_data.get("metadata", {})

        if role not in ["user", "bot"]:
            return JSONResponse(
                {"error": "role 必須是 'user' 或 'bot'"},
                status_code=400
            )

        if not content:
            return JSONResponse(
                {"error": "content 不能為空"},
                status_code=400
            )

        # 添加消息到會話
        message = add_message(
            session_id=session_id,
            role=role,
            content=content,
            metadata=metadata
        )

        return JSONResponse({
            "status": "success",
            "message_id": message["id"]
        })

    except Exception as e:
        logger.error(f"直接添加消息時出錯: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)


@router.post("/chat/batch")
async def chat_batch(request: Request):
    """
    批量添加消息到會話

    請求格式：
    {
        "messages": [
            {"role": "user", "content": "用戶消息1"},
            {"role": "bot", "content": "機器人回應1"},
            ...
        ],
        "session_id": "會話ID" (可選)
    }
    """
    try:
        req_data = await request.json()
        messages = req_data.get("messages", [])
        session_id = req_data.get("session_id", "default")

        if not messages:
            return JSONResponse(
                {"error": "messages 不能為空"},
                status_code=400
            )

        # 批量添加消息
        message_ids = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            metadata = msg.get("metadata", {})

            if role not in ["user", "bot"]:
                continue

            if not content:
                continue

            # 添加消息
            message = add_message(
                session_id=session_id,
                role=role,
                content=content,
                metadata=metadata
            )
            message_ids.append(message["id"])

        return JSONResponse({
            "status": "success",
            "message_ids": message_ids,
            "count": len(message_ids)
        })

    except Exception as e:
        logger.error(f"批量添加消息時出錯: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)
