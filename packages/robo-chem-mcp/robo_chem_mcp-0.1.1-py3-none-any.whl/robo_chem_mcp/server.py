import argparse

from mcp.server.fastmcp import FastMCP
from openai import AsyncOpenAI

mcp = FastMCP("Robot Chemist MCP Server")


@mcp.tool()
def setup_round_bottle_flask_with_stirrer():
    """
    To setup a round bottle flask with a stirrer.
    """
    return "done"


@mcp.tool()
def add_powder_to_flask():
    """
    To add powder to the flask.
    """
    return "done"


@mcp.tool()
def add_liquid_to_flask():
    """
    to add liquid to the flask.
    """
    return "done"


def main():
    parser = argparse.ArgumentParser(description="DeepResearch Server")
    # parser.add_argument(
    #     "--openai_api_key", type=str, required=True, help="Your OpenAI API Key"
    # )
    args = parser.parse_args()

    # external_client = AsyncOpenAI(
    #     base_url = "https://ai.devtool.tech/proxy/v1",
    #     api_key = args.openai_api_key,
    # )
    # set_default_openai_client(external_client)
    # set_tracing_disabled(True)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
