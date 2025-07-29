"""
MCP tools for creating LinkML schemas and example datasets
"""
import os

from mcp.server.fastmcp import FastMCP

import aurelian.agents.filesystem.filesystem_tools as fst
from aurelian.agents.linkml.linkml_agent import SYSTEM
from aurelian.agents.linkml.linkml_config import LinkMLDependencies
from aurelian.agents.linkml.linkml_tools import validate_then_save_schema, ValidationResult
from aurelian.utils.search_utils import web_search

# Initialize FastMCP server
mcp = FastMCP("linkml", instructions=SYSTEM)

from linkml_runtime.loaders import yaml_loader
from linkml_runtime.linkml_model import SchemaDefinition
from linkml.validator import validate
from pydantic_ai import RunContext, ModelRetry

from aurelian.dependencies.workdir import WorkDir

def deps() -> LinkMLDependencies:
    deps = LinkMLDependencies()
    loc = os.getenv("AURELIAN_WORKDIR", "/tmp/aurelian")
    deps.workdir = WorkDir(loc)
    return deps

def ctx() -> RunContext[LinkMLDependencies]:
    rc: RunContext[LinkMLDependencies] = RunContext[LinkMLDependencies](
        deps=deps(),
        model=None, usage=None, prompt=None,
    )
    return rc


@mcp.tool()
async def validate_schema(schema: str, save_to_file: str="schema.yaml") -> ValidationResult:
    """
    Validate a LinkML schema.

    Args:
        schema: schema (as yaml) to validate. Do not truncate, always pass the whole schema.
        save_to_file: optional file name to save the schema to. Defaults to schema.yaml

    Returns:

    """
    return await validate_then_save_schema(ctx(), schema, save_to_file)


@mcp.tool()
async def inspect_file(data_file: str) -> str:
    """
    Inspect a file in the working directory.

    Args:
        data_file: name of file

    Returns:

    """
    return await fst.inspect_file(ctx(), data_file)


@mcp.tool()
async def list_files() -> str:
    """
    List files in the working directory.

    Args:

    Returns:

    """
    return "\n".join(deps().workdir.list_file_names())

@mcp.tool()
async def write_to_file(data: str, file_name: str) -> str:
    """
    Write data to a file in the working directory.

    Args:
        data:
        file_name:

    Returns:

    """
    print(f"Writing data to file: {file_name}")
    deps().workdir.write_file(file_name, data)
    return f"Data written to {file_name}"

@mcp.tool()
async def validate_data(schema: str, data_file: str) -> str:
    """
    Validate data file against a schema.

    This assumes the data file is present in the working directory.
    You can write data to the working directory using the `write_to_file` tool.

    Args:
        schema: the schema (as a YAML string)
        data_file: the name of the data file in the working directory

    Returns:

    """
    print(f"Validating data file: {data_file} using schema: {schema}")
    try:
        schema = yaml_loader.loads(schema, target_class=SchemaDefinition)
    except Exception as e:
        return f"Schema does not validate: {e}"
    try:
        instances = deps().parse_objects_from_file(data_file)
        for instance in instances:
            print(f"Validating {instance}")
            rpt = validate(instance, schema)
            print(f"Validation report: {rpt}")
            if rpt.results:
                return f"Data does not validate:\n{rpt.results}"
        return f"{len(instances)} instances all validate successfully"
    except Exception as e:
        return f"Data does not validate: {e}"


@mcp.tool()
async def search_web(query: str) -> str:
    """
    Search the web using a text query.

    Note, this will not retrieve the full content, for that you
    should use `retrieve_web_page`.

    Args:
        query: Text query

    Returns: matching web pages plus summaries
    """
    print(f"Web Search: {query}")
    return web_search(query)

@mcp.tool()
async def retrieve_web_page(url: str) -> str:
    """
    Fetch the contents of a web page.

    Args:
        url: URL of the web page

    Returns:
        The contents of the web page.
    """
    print(f"Fetch URL: {url}")
    import aurelian.utils.search_utils as su
    return su.retrieve_web_page(url)


@mcp.tool()
async def download_web_page(url: str, local_file_name: str) -> str:
    """
    Download contents of a web page.

    Args:
        url: URL of the web page
        local_file_name: Name of the local file to save the

    Returns:
        str: message
    """
    print(f"Fetch URL: {url}")
    import aurelian.utils.search_utils as su
    data = su.retrieve_web_page(url)
    deps().workdir.write_file(local_file_name, data)
    return f"Data written to {local_file_name}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
