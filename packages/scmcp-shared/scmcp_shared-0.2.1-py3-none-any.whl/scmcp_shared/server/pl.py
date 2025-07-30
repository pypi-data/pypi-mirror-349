import os
import inspect
from functools import partial
import scanpy as sc
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from ..schema.pl import *
from pathlib import Path
from ..logging_config import setup_logger
from ..util import forward_request, sc_like_plot, get_ads


logger = setup_logger()

pl_mcp = FastMCP("ScanpyMCP-PL-Server")



@pl_mcp.tool()
async def pca(request: PCAModel = PCAModel()):
    """Scatter plot in PCA coordinates. default figure for PCA plot"""
    try:
        result = await forward_request("pl_pca", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.pca, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def diffmap(request: DiffusionMapModel = DiffusionMapModel()):
    """Plot diffusion map embedding of cells."""
    try:
        result = await forward_request("pl_diffmap", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.diffmap, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def violin(request: ViolinModel,):
    """Plot violin plot of one or more variables."""
    try:
        result = await forward_request("pl_violin", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.violin, adata, request)
        return {"figpath": fig_path}
    except KeyError as e:
        raise ToolError(f"doest found {e} in current sampleid with adtype {request.adtype}")
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def stacked_violin(request: StackedViolinModel = StackedViolinModel()):
    """Plot stacked violin plots. Makes a compact image composed of individual violin plots stacked on top of each other."""
    try:
        result = await forward_request("pl_stacked_violin", request)
        if result is not None:
            return result           
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.stacked_violin, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def heatmap(request: HeatmapModel):
    """Heatmap of the expression values of genes."""
    try:
        result = await forward_request("pl_heatmap", request)
        if result is not None:
            return result           
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.heatmap, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def dotplot(request: DotplotModel):
    """Plot dot plot of expression values per gene for each group."""
    try:
        result = await forward_request("pl_dotplot", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.dotplot, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def matrixplot(request: MatrixplotModel):
    """matrixplot, Create a heatmap of the mean expression values per group of each var_names."""
    try:
        result = await forward_request("pl_matrixplot", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.matrixplot, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def tracksplot(request: TracksplotModel):
    """tracksplot, compact plot of expression of a list of genes."""
    try:
        result = await forward_request("pl_tracksplot", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.tracksplot, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def scatter(request: EnhancedScatterModel = EnhancedScatterModel()):
    """Plot a scatter plot of two variables, Scatter plot along observations or variables axes."""
    try:
        result = await forward_request("pl_scatter", request)
        if result is not None:
            return result    
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.scatter, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def embedding(request: EmbeddingModel):
    """Scatter plot for user specified embedding basis (e.g. umap, tsne, etc)."""
    try:
        result = await forward_request("pl_embedding", request)
        if result is not None:
            return result       
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.embedding, adata, request)
        return {"figpath": fig_path}
    except KeyError as e:
        raise ToolError(f"doest found {e} in current sampleid with adtype {request.adtype}")
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def embedding_density(request: EmbeddingDensityModel):
    """Plot the density of cells in an embedding."""
    try:
        result = await forward_request("pl_embedding_density", request)
        if result is not None:
            return result          
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.embedding_density, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def rank_genes_groups(request: RankGenesGroupsModel):
    """Plot ranking of genes based on differential expression."""
    try:
        result = await forward_request("pl_rank_genes_groups", request)
        if result is not None:
            return result         
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.rank_genes_groups, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def rank_genes_groups_dotplot(
    request: RankGenesGroupsDotplotModel,
):
    """Plot ranking of genes(DEGs) using dotplot visualization. Defualt plot DEGs for rank_genes_groups tool"""
    from fastmcp.exceptions import ClientError 
    try:
        result = await forward_request("pl_rank_genes_groups_dotplot", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.rank_genes_groups_dotplot, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def clustermap(
    request: ClusterMapModel = ClusterMapModel() 
):
    """Plot hierarchical clustering of cells and genes."""
    try:
        result = await forward_request("pl_clustermap", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.clustermap, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def highly_variable_genes(
    request: HighlyVariableGenesModel = HighlyVariableGenesModel() 
):
    """plot highly variable genes; Plot dispersions or normalized variance versus means for genes."""
    try:
        result = await forward_request("pl_highly_variable_genes", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.highly_variable_genes, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def pca_variance_ratio(
    request: PCAVarianceRatioModel = PCAVarianceRatioModel() 
):
    """Plot the PCA variance ratio to visualize explained variance."""
    try:
        result = await forward_request("pl_pca_variance_ratio", request)
        if result is not None:
            return result
        adata = get_ads().get_adata(request=request)
        fig_path = sc_like_plot(sc.pl.pca_variance_ratio, adata, request)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)
