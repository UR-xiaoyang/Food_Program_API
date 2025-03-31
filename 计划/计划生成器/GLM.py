import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import AsyncGenerator
import logging

from zhipuai import ZhipuAI
from 计划.计划生成器.GLM_config import GLM配置

logger = logging.getLogger(__name__)

async def chat(messages) -> AsyncGenerator[str, None]:
    q = asyncio.Queue()

    def enqueue():
        client = ZhipuAI(api_key=GLM配置.api_key)
        response = client.chat.completions.create(

            model=GLM配置.model,
            messages=messages,
            stream=True,
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                logger.info(f"Received chunk: {content}")
                q.put_nowait(content)
        logger.info("Sending [DONE]")
        q.put_nowait('[DONE]')  # 发送结束标识符

    loop = asyncio.get_running_loop()
    loop.run_in_executor(ThreadPoolExecutor(), enqueue)

    while True:
        item = await q.get()
        if item is None or item == '[DONE]':
            break
        yield f"{item}"
