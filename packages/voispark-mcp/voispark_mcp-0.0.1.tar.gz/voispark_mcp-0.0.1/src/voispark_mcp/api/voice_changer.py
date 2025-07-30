from voispark_mcp.core.api_request import get
from voispark_mcp.core.error_code import ErrorCode
from voispark_mcp.msg.base_resp import BaseResponse
from voispark_mcp.msg.voice_changer_msg import VoiceChangerModelsResponse


async def get_voice_changer_models():
    resp = await get(
        "/api/voice_changer/models",
        response_model=BaseResponse[VoiceChangerModelsResponse],
    )
    if resp is None:
        return "Failed to get voice changer models"
    if resp.code != ErrorCode.SUCCESS.code:
        return "Failed to get voice changer models"
    if resp.data is None:
        return "No voice changer models found"
    return resp.data.model_dump()
