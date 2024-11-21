import asyncio
from concurrent.futures import ThreadPoolExecutor
import contextvars


executor = ThreadPoolExecutor(max_workers=10)  # Adjust the max_workers as needed

# Context variable to hold the event loop
event_loop = contextvars.ContextVar("event_loop")


async def run_in_threadpool(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, func, *args, **kwargs)
