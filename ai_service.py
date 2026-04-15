"""
AI Service Module
Handles API calls to Mistral AI with Groq as fallback.
Manages system prompts and response handling.
"""
import asyncio
import logging
import requests
import config


logger = logging.getLogger(__name__)


def load_instructions() -> str:
    """
    Load bot behavior instructions from instructions.txt file.
    Returns empty string if file doesn't exist.
    """
    try:
        with open("instructions.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.warning("instructions.txt not found, using default behavior")
        return ""


# Load system prompt at startup
SYSTEM_PROMPT = load_instructions()


async def get_mistral_response(text: str) -> str:
    """
    Call Mistral AI API to get a response.
    
    Args:
        text: User message to send to AI
        
    Returns:
        AI response as string
        
    Raises:
        Exception: If API call fails
    """
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build messages with system prompt
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({"role": "user", "content": text})
    
    payload = {
        "model": "mistral-tiny",
        "messages": messages
    }
    
    # Run blocking requests in executor to avoid blocking event loop
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, 
        lambda: requests.post(url, json=payload, headers=headers, timeout=30)
    )
    response.raise_for_status()
    
    return response.json()["choices"][0]["message"]["content"]


async def get_groq_response(text: str) -> str:
    """
    Call Groq AI API as fallback when Mistral fails.
    
    Args:
        text: User message to send to AI
        
    Returns:
        AI response as string
        
    Raises:
        Exception: If API call fails
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build messages with system prompt
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({"role": "user", "content": text})
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages
    }
    
    # Run blocking requests in executor to avoid blocking event loop
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: requests.post(url, json=payload, headers=headers, timeout=30)
    )
    response.raise_for_status()
    
    return response.json()["choices"][0]["message"]["content"]


async def get_ai_response(text: str) -> str:
    """
    Get AI response with automatic fallback.
    Tries Mistral first, falls back to Groq on failure.
    
    Args:
        text: User message to send to AI
        
    Returns:
        AI response as string, or fallback error message
    """
    # Try Mistral first
    try:
        return await get_mistral_response(text)
    except Exception as e:
        logger.warning(f"Mistral API error: {e}, attempting Groq fallback...")
        
        # Fallback to Groq
        try:
            return await get_groq_response(text)
        except Exception as e2:
            logger.error(f"Groq API error: {e2}")
            return "Oops! Something went wrong. Try again later!"