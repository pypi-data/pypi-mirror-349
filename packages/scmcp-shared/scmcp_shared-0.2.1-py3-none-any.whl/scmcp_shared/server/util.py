import os
import inspect
from pathlib import Path
import scanpy as sc
from fastmcp import FastMCP , Context
from fastmcp.exceptions import ToolError
from ..schema.util import *
from ..util import filter_args, forward_request, get_ads, generate_msg,add_op_log


ul_mcp = FastMCP("SCMCP-Util-Server")


@ul_mcp.tool()
async def query_op_log(request: QueryOpLogModel = QueryOpLogModel()):
    """Query the adata operation log"""
    adata = get_ads().get_adata(request=request)
    op_dic = adata.uns["operation"]["op"]
    opids = adata.uns["operation"]["opid"][-n:]
    op_list = []
    for opid in opids:
        op_list.append(op_dic[opid])
    return op_list


@ul_mcp.tool()
async def mark_var(
    request: MarkVarModel = MarkVarModel() 
):
    """
    Determine if each gene meets specific conditions and store results in adata.var as boolean values.
    For example: mitochondrion genes startswith MT-.
    The tool should be called first when calculate quality control metrics for mitochondrion, ribosomal, harhemoglobin genes, or other qc_vars.
    """
    try:
        result = await forward_request("ul_mark_var", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        var_name = request.var_name
        gene_class = request.gene_class
        pattern_type = request.pattern_type
        patterns = request.patterns
        if gene_class is not None:
            if gene_class == "mitochondrion":
                adata.var["mt"] = adata.var_names.str.startswith(('MT-', 'Mt','mt-'))
                var_name = "mt"
            elif gene_class == "ribosomal":
                adata.var["ribo"] = adata.var_names.str.startswith(("RPS", "RPL", "Rps", "Rpl"))
                var_name = "ribo"
            elif gene_class == "hemoglobin":
                adata.var["hb"] = adata.var_names.str.contains("^HB[^(P)]", case=False)
                var_name = "hb"    
        elif pattern_type is not None and patterns is not None:
            if pattern_type == "startswith":
                adata.var[var_name] = adata.var_names.str.startswith(patterns)
            elif pattern_type == "endswith":
                adata.var[var_name] = adata.var_names.str.endswith(patterns)
            elif pattern_type == "contains":
                adata.var[var_name] = adata.var_names.str.contains(patterns)
            else:
                raise ValueError(f"Did not support pattern_type: {pattern_type}")
        else:
            raise ValueError(f"Please provide validated parameter")
    
        res = {var_name: adata.var[var_name].value_counts().to_dict(), "msg": f"add '{var_name}' column in adata.var"}
        func_kwargs = {"var_name": var_name, "gene_class": gene_class, "pattern_type": pattern_type, "patterns": patterns}
        add_op_log(adata, "mark_var", func_kwargs)
        return res
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@ul_mcp.tool()
async def list_var(
    request: ListVarModel = ListVarModel() 
):
    """List key columns in adata.var. It should be called for checking when other tools need var key column names as input."""
    try:
        result = await forward_request("ul_list_var", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        columns = list(adata.var.columns)
        add_op_log(adata, list_var, {})
        return columns
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@ul_mcp.tool()
async def list_obs(
    request: ListObsModel = ListObsModel() 
):
    """List key columns in adata.obs. It should be called before other tools need obs key column names input."""
    try:
        result = await forward_request("ul_list_obs", request)
        if result is not None:
            return result    
        adata = get_ads().get_adata(request=request)
        columns = list(adata.obs.columns)
        add_op_log(adata, list_obs, {})
        return columns
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@ul_mcp.tool()
async def check_var(
    request: VarNamesModel = VarNamesModel() 
):
    """Check if genes/variables exist in adata.var_names. This tool should be called before gene expression visualizations or color by genes."""
    try:
        result = await forward_request("ul_check_var", request)
        if result is not None:
            return result     
        adata = get_ads().get_adata(request=request)
        var_names = request.var_names
        result = {v: v in adata.var_names for v in var_names}
        add_op_log(adata, check_var, {"var_names": var_names})
        return result
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@ul_mcp.tool()
async def merge_adata(
    request: ConcatAdataModel = ConcatAdataModel() 
):
    """Merge multiple adata objects."""
     
    try:
        result = await forward_request("ul_merge_adata", request)
        if result is not None:
            return result
        ads = get_ads()
        adata = ads.get_adata(request=request)
        kwargs = {k: v for k, v in request.model_dump().items() if v is not None}
        merged_adata = adata.concat(list(ads.adata_dic[dtype].values()), **kwargs)
        ads.adata_dic[dtype] = {}
        ads.active_id = "merged_adata"
        add_op_log(merged_adata, ad.concat, kwargs)
        ads.adata_dic[ads.active_id] = merged_adata
        return {"status": "success", "message": "Successfully merged all AnnData objects"}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@ul_mcp.tool()
async def set_dpt_iroot(
    request: DPTIROOTModel,
    
):
    """Set the iroot cell"""
    try:
        result = await forward_request("ul_set_dpt_iroot", request)
        if result is not None:
            return result     
        adata = get_ads().get_adata(request=request)
        diffmap_key = request.diffmap_key
        dimension = request.dimension
        direction = request.direction
        if diffmap_key not in adata.obsm:
            raise ValueError(f"Diffusion map key '{diffmap_key}' not found in adata.obsm")
        if direction == "min":
            adata.uns["iroot"] = adata.obsm[diffmap_key][:, dimension].argmin()
        else:  
            adata.uns["iroot"] = adata.obsm[diffmap_key][:, dimension].argmax()
        
        func_kwargs = {"diffmap_key": diffmap_key, "dimension": dimension, "direction": direction}
        add_op_log(adata, "set_dpt_iroot", func_kwargs)
        
        return {"status": "success", "message": f"Successfully set root cell for DPT using {direction} of dimension {dimension}"}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@ul_mcp.tool()
async def add_layer(
    request: AddLayerModel,
):
    """Add a layer to the AnnData object.
    """
    try:
        result = await forward_request("ul_add_layer", request)
        if result is not None:
            return result         
        adata = get_ads().get_adata(request=request)
        layer_name = request.layer_name
        
        # Check if layer already exists
        if layer_name in adata.layers:
            raise ValueError(f"Layer '{layer_name}' already exists in adata.layers")
        # Add the data as a new layer
        adata.layers[layer_name] = adata.X.copy()

        func_kwargs = {"layer_name": layer_name}
        add_op_log(adata, "add_layer", func_kwargs)
        
        return {
            "status": "success", 
            "message": f"Successfully added layer '{layer_name}' to adata.layers"
        }
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@ul_mcp.tool()
async def check_samples():
    """check the stored samples    
    """
    try:
        ads = get_ads()
        return {"sampleid": [list(ads.adata_dic[dk].keys()) for dk in ads.adata_dic.keys()]}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)