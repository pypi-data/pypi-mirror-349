from contextlib import asynccontextmanager
from dataclasses import dataclass
import logging
from typing import AsyncIterator
from mcp.server.fastmcp import FastMCP

from voispark_mcp.api.conversation import (
    get_conversation_models as _get_conversation_models,
)
from voispark_mcp.api.tts import get_tts_models as _get_tts_models
from voispark_mcp.api.voice_clone import (
    get_voice_clone_models as _get_voice_clone_models,
)
from voispark_mcp.api.voice_changer import (
    get_voice_changer_models as _get_voice_changer_models,
)
from voispark_mcp.api.voices import list_all_voices as _list_all_voices
from voispark_mcp.api.voices import get_providers as _get_providers


@dataclass
class AppContext:
    pass


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    logging.info("Starting MCP server")
    try:
        yield AppContext()
    finally:
        # Cleanup on shutdown
        logging.info("Shutting down MCP server")


# Create an MCP server
mcp = FastMCP("Demo", lifespan=app_lifespan)


# -*- conversation -*-


@mcp.resource(uri="conversation://models")
async def get_conversation_models() -> str | dict:
    """
    Get all conversation models
    """
    return await _get_conversation_models()


# -*- text_to_speech -*-


@mcp.resource(uri="textToSpeech://models")
async def get_tts_models() -> str | dict:
    """
    Get all TTS models
    """
    return await _get_tts_models()


# -*- voice_changer -*-


@mcp.resource(uri="voiceChanger://models")
async def get_voice_changer_models() -> str | dict:
    """
    Get all voice changer models
    """
    return await _get_voice_changer_models()


# -*- voice_clone -*-


@mcp.resource(uri="voiceClone://models")
async def get_voice_clone_models() -> str | dict:
    """
    Get all voice clone models
    """
    return await _get_voice_clone_models()


# -*- voices -*-


@mcp.resource(uri="voices://providers")
async def get_providers() -> str | dict:
    """
    Get all voice providers
    """
    return await _get_providers()


@mcp.resource(uri="voices://{provider_id}/{voice_type}/list")
async def list_all_voices(provider_id: str, voice_type: str) -> str | dict:
    """
    List all voices
    """
    return await _list_all_voices(provider_id, voice_type)


def main():
    """Entry point for the voispark_mcp command."""
    mcp.run()
