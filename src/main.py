import asyncio
from pathlib import Path

from semantic_kernel import Kernel
from semantic_kernel.connectors.mcp import MCPStdioPlugin

from src.utils import chat

kernel = Kernel()


async def main() -> None:
    async with MCPStdioPlugin(
        name="important_log",
        description="Important Log Plugin",
        command="uv",
        args=[
            "run",
            f"{Path(__file__).resolve().parent}/my_mcp_plugin",
        ],
    ) as my_plugin:
        await my_plugin.load_tools()
        kernel.add_plugin(my_plugin)

        chatting: bool = True

        while chatting:
            chatting = await chat(kernel=kernel)


if __name__ == "__main__":
    asyncio.run(main())
