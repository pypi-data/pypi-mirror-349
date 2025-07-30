import inspect
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
import os
import anndata as ad
from ..schema.util import *
from scmcp_shared.logging_config import setup_logger
from scmcp_shared.util import add_op_log,forward_request, get_ads
logger = setup_logger()


ul_mcp = FastMCP("ScanpyMCP-Util-Server")


@ul_mcp.tool()
async def map_cell_type(
    request: CelltypeMapCellTypeModel,
):
    """Map cluster id to cell type names"""
    try:
        result = await forward_request("ul_map_cell_type", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        cluster_key = request.cluster_key
        added_key = request.added_key

        if cluster_key not in adata.obs.columns:
            raise ValueError(f"cluster key '{cluster_key}' not found in adata.obs")
        if request.mapping is not None:
            adata.obs[added_key] = adata.obs[cluster_key].map(request.mapping)
        elif request.new_names is not None:
            adata.rename_categories(cluster_key, request.new_names)
        
        func_kwargs = {"cluster_key": cluster_key, "added_key": added_key, 
                    "mapping": request.mapping, "new_names": request.new_names}
        add_op_log(adata, "map_cell_type", func_kwargs)
        
        return {
            "status": "success", 
            "message": f"Successfully mapped values from '{cluster_key}' to '{added_key}'",
            "adata": adata
        }
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)
