import os
import inspect
from pathlib import Path
import scanpy as sc
from fastmcp import FastMCP , Context
from fastmcp.exceptions import ToolError
from ..schema import AdataModel
from ..schema.io import *
from ..util import filter_args, forward_request, get_ads, generate_msg


io_mcp = FastMCP("SCMCP-IO-Server")


@io_mcp.tool()
async def read(
    request: ReadModel, 
    adinfo: AdataModel = AdataModel()
):
    """
    Read data from 10X directory or various file formats (h5ad, 10x, text files, etc.).
    """
    try:
        result = await forward_request("io_read", request, adinfo)
        if result is not None:
            return result        
        kwargs = request.model_dump()

        file = Path(kwargs.get("filename", None))
        if file.is_dir():
            kwargs["path"] = kwargs["filename"]
            func_kwargs = filter_args(request, sc.read_10x_mtx)
            adata = sc.read_10x_mtx(kwargs["path"], **func_kwargs)
        elif file.is_file():
            func_kwargs = filter_args(request, sc.read)
            adata = sc.read(**func_kwargs)
            if not kwargs.get("first_column_obs", True):
                adata = adata.T
        else:
            raise FileNotFoundError(f"{kwargs['filename']} does not exist")

        ads = get_ads()
        if adinfo.sampleid is not None:
            ads.active_id = adinfo.sampleid
        else:
            ads.active_id = f"adata{len(ads.adata_dic[adinfo.adtype])}"
            
        adata.layers["counts"] = adata.X
        adata.var_names_make_unique()
        adata.obs_names_make_unique()
        ads.set_adata(adata, adinfo=adinfo)
        return generate_msg(adinfo, adata, ads)
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@io_mcp.tool()
async def write(
    request: WriteModel, 
    adinfo: AdataModel = AdataModel()
):
    """save adata into a file.
    """
    try:
        result = await forward_request("io_write", request, adinfo)
        if result is not None:
            return result
        ads = get_ads()
        adata = ads.get_adata(adinfo=adinfo)
        kwargs = request.model_dump()
        sc.write(kwargs["filename"], adata)
        return {"filename": kwargs["filename"], "msg": "success to save file"}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)