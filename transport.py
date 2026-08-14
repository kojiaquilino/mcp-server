import asyncio
import sys
from typing import AsyncGenerator
from logger import log_stderr

async def stdio_reader() -> AsyncGenerator[str, None]:
    """
    Asynchronously reads raw lines from sys.stdin without blocking the event loop.
    Yields each line as a decoded UTF-8 string.
    """
    loop = asyncio.get_running_loop()                   # event loop
    reader = asyncio.StreamReader()                     # buffer to store stdin content asynchronously
    protocol = asyncio.StreamReaderProtocol(reader)     # protocol to wrap buffer, async reads stdin

    # Connect stdin pipe to async stream reader -> lines are moved into the async buffer "reader"
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    while True:
        line_bytes = await reader.readline()

        if not line_bytes:
            break # EOF: stream closed by client, return None

        request = line_bytes.decode("utf-8").strip()
        if request:
            yield request
