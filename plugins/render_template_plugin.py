from semantic_kernel.functions import kernel_function
import chainlit as cl
class RenderTemplatePlugin:
    @kernel_function(
        name="get_video_note_block_format",
        description="Return the JSON output format for rendering exercise videos with notes and tips."
    )
    async def get_video_note_block_format(self) -> str:
        async with cl.Step(name=f"正在归纳整理图文笔记...", type="function"):
            pass
        return """
{
  "render": [
    {
      "type": "video_note_block",
      "title": "<exercise name>",
      "props": {
        "sideUrl": "<side view video URL>",
        "frontUrl": "<front view video URL>",
        "notes": "<important form or safety notes>",
        "tips": "<effective training tips>"
      }
    }
  ]
}
"""
