# older no support for enable" parameter in decorator and ctx don't work inside
# from mcp.server.fastmcp import Context, FastMCP
from urllib import parse

import aiofiles
from fastmcp import Context, FastMCP

mcp = FastMCP()

IMPORTANT_LOG_PATH: str = "important_log.txt"


# resource since it has no variables
@mcp.resource("data://default")
def get_data_resource() -> str:
    return "This is a resource!"


# resource template since it has a variable
@mcp.resource("resource://{name}")
def get_data(name: str) -> str:
    name = name.lower().strip()
    if name == "hi":
        return "Hello World!"

    if name == "no":
        return "404 Not Found"

    return "Dummy data"


@mcp.tool
def inspect_resource(resource_uri: str) -> str:
    return parse.urlparse(resource_uri).path


@mcp.tool
async def show_available_resources() -> list[str]:
    resources = await mcp.get_resources()
    return list(resources)


@mcp.resource(f"file://{IMPORTANT_LOG_PATH}", mime_type="text/plain")
async def read_important_log() -> str:
    """Show important logs."""
    global IMPORTANT_LOG_PATH

    # TODO: figure out where is this log shown
    # await ctx.debug("Reading important log...")
    # await ctx.info(f"Client {ctx.client_id or 'Unknown client'}")

    try:
        content: str
        async with aiofiles.open(IMPORTANT_LOG_PATH, mode="r") as f:
            content = await f.read()
        return content
    except FileNotFoundError:
        return "Log file not found."


@mcp.tool(enabled=False)
async def request_info(ctx: Context) -> dict:
    """Return information about the current request."""
    await ctx.info("TESTIN LOGGINGG")  # TODO: figure out where this shows
    return {
        "request_id": ctx.request_id,
        "client_id": ctx.client_id or "Unknown client",
    }


@mcp.tool
async def add_to_important_log(log: str) -> str:
    global IMPORTANT_LOG_PATH

    # TODO: figure out how to use ctx here inside tool with a parameter
    # await ctx.debug("Adding important log...")
    try:
        async with aiofiles.open(IMPORTANT_LOG_PATH, mode="a") as f:
            await f.write(f"{log}\n")
        return "Logs has been written"
    except FileNotFoundError:
        return "Log file not found."


if __name__ == "__main__":
    mcp.run(transport="stdio")
