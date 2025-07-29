import argparse
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from openai import AsyncOpenAI
from pydantic import Field

mcp = FastMCP("Robot Chemist MCP Server")


@mcp.tool()
def setup_glassware_with_stirrer(
    glassware: Annotated[str, Field(description="The glassware to be set up")],
):
    """Setup a glassware with a stirrer put in it"""
    return "done"


@mcp.tool()
def add_powder_to_glassware(
    glassware: Annotated[str, Field(description="The glassware to be set up")],
    powder: Annotated[str, Field(description="The powder to be added")],
    weight: Annotated[float, Field(description="The weight of the powder")],
):
    """Weigh a powder and add it to the glassware"""
    return "done"


@mcp.tool()
def add_liquid_to_glassware(
    glassware: Annotated[str, Field(description="The glassware to be set up")],
    liquid: Annotated[str, Field(description="The liquid to be added")],
    volume: Annotated[float, Field(description="The volume of the liquid")],
):
    """Add liquid of a certain volume to the glassware"""
    return "done"


@mcp.tool()
def calulate_solution_amount(
    concentration: Annotated[
        float, Field(description="Concentration of the solution")
    ] = 0.0,
    total_amount: Annotated[
        float, Field(description="Total volume of the solution")
    ] = 0.0,
    solvent_amount: Annotated[float, Field(description="Mass of the solvent")] = 0.0,
    solute_amount: Annotated[float, Field(description="Mass of the solute")] = 0.0,
):
    """Calculate the numbers during the preparation of a solution, given some of the numbers and calculate the others"""
    # assert if not 2 parameters are given
    assert (
        (concentration > 0) + (total_amount > 0) + (solvent_amount > 0)
        + (solute_amount > 0)
    ) == 2, "Please provide exactly two parameters"

    # Do the calculation
    if concentration > 0 and total_amount > 0:
        solvent_amount = total_amount * (1 - concentration)
        solute_amount = total_amount * concentration
    elif concentration > 0 and solvent_amount > 0:
        total_amount = solvent_amount / (1 - concentration)
        solute_amount = total_amount * concentration
    elif concentration > 0 and solute_amount > 0:
        total_amount = solute_amount / concentration
        solvent_amount = total_amount * (1 - concentration)
    elif solvent_amount > 0 and total_amount > 0:
        concentration = 1 - (solvent_amount / total_amount)
        solute_amount = total_amount * concentration
    elif solute_amount > 0 and total_amount > 0:
        concentration = solute_amount / total_amount
        solvent_amount = total_amount * (1 - concentration)

    return {
        "concentration": concentration,
        "total_amount": total_amount,
        "solvent_amount": solvent_amount,
        "solute_amount": solute_amount,
    }


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
