import asyncio
from fastmcp import FastMCP
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any


import scmcp_shared.server as shs
from .util import ul_mcp



ads = shs.AdataState()

@asynccontextmanager
async def adata_lifespan(server: FastMCP) -> AsyncIterator[Any]:
    yield ads


scanpy_mcp = FastMCP("Scanpy-MCP-Server", lifespan=adata_lifespan)


async def setup(modules=None):
    mcp_dic = {
        "io": shs.io_mcp, 
        "pp": shs.pp_mcp, 
        "tl": shs.tl_mcp, 
        "pl": shs.pl_mcp, 
        "ul": shs.ul_mcp
        }
    if modules is None or modules == "all":
        modules = ["io", "pp", "tl", "pl", "ul"]
    for module in modules:
        await scanpy_mcp.import_server(module, mcp_dic[module])
    await scanpy_mcp.import_server("ul2", ul_mcp)
