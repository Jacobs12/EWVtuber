"""
EWVtuber
项目名称：虚拟主播软件
版权所有：北京光线传媒股份有限公司
技术支持：北京光线传媒股份有限公司
Editor:fengtao
Mails:fengtao23@mails.ucas.ac.cn
"""
import asyncio

import edge_tts

# edge-tts --list-voices


TEXT = "11月3日，上海陆家嘴金融贸易区开发股份有限公司（下称“陆家嘴”）发布公告称，控股子公司苏州绿岸房地产开发有限公司（以下简称“苏州绿岸”）名下14块土地存在污染，且污染面积和污染程度远超苏钢集团挂牌出让时所披露的污染情况。"
VOICE = "zh-CN-XiaoyiNeural"
OUTPUT = "Buffer/Audio/speech.mp3"


# WEBVTT_FILE = "test.vtt"

# async def text_to_speech(text: str) -> str:
#     communicate = edge_tts.Communicate(text, VOICE)
#     submaker = edge_tts.SubMaker()
#     with open(OUTPUT, "wb") as file:
#         async for chunk in communicate.stream():
#             if chunk["type"] == "audio":
#                 file.write(chunk["data"])
#             elif chunk["type"] == "WordBoundary":
#                 submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
#     return OUTPUT


async def text_to_speech(text: str) -> str:
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT)
    return OUTPUT

# async def _main() -> None:
#     communicate = edge_tts.Communicate(TEXT, VOICE)
#     submaker = edge_tts.SubMaker()
#     with open(OUTPUT_FILE, "wb") as file:
#         async for chunk in communicate.stream():
#             if chunk["type"] == "audio":
#                 file.write(chunk["data"])
#             elif chunk["type"] == "WordBoundary":
#                 submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

# with open(WEBVTT_FILE, "w", encoding="utf-8") as file:
#     file.write(submaker.generate_subs())


# if __name__ == "__main__":
#     asyncio.run(_main())
