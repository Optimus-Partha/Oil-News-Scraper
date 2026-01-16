import sys
import asyncio

# Set event loop policy BEFORE anything else
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import uvicorn

if __name__ == "__main__":
    # Run without reload to avoid reloader interfering with event loop
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)