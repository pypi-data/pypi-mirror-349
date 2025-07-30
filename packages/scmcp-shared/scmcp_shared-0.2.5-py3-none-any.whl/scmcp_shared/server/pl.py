import os
import inspect
from functools import partial
import scanpy as sc
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from ..schema.pl import *
from ..schema import AdataModel
from pathlib import Path
from ..logging_config import setup_logger
from ..util import forward_request, sc_like_plot, get_ads


logger = setup_logger()

pl_mcp = FastMCP("ScanpyMCP-PL-Server")



@pl_mcp.tool()
async def pca(
    request: PCAModel = PCAModel(), 
    adinfo: AdataModel = AdataModel()
):
    """Scatter plot in PCA coordinates. default figure for PCA plot"""
    try:
        result = await forward_request("pl_pca", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.pca, adata, request, adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def diffmap(
    request: DiffusionMapModel = DiffusionMapModel(), 
    adinfo: AdataModel = AdataModel()
):
    """Plot diffusion map embedding of cells."""
    try:
        result = await forward_request("pl_diffmap", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.diffmap, adata, request, adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def violin(
    request: ViolinModel,
    adinfo: AdataModel = AdataModel()
):
    """Plot violin plot of one or more variables."""
    try:
        result = await forward_request("pl_violin", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.violin, adata, request, adinfo)
        return {"figpath": fig_path}
    except KeyError as e:
        raise ToolError(f"doest found {e} in current sampleid with adtype {adinfo.adtype}")
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def stacked_violin(
    request: StackedViolinModel = StackedViolinModel(),
    adinfo: AdataModel = AdataModel()
):
    """Plot stacked violin plots. Makes a compact image composed of individual violin plots stacked on top of each other."""
    try:
        result = await forward_request("pl_stacked_violin", request, adinfo)
        if result is not None:
            return result           
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.stacked_violin, adata, request,adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def heatmap(
    request: HeatmapModel,
    adinfo: AdataModel = AdataModel()
):
    """Heatmap of the expression values of genes."""
    try:
        result = await forward_request("pl_heatmap", request, adinfo)
        if result is not None:
            return result           
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.heatmap, adata, request,adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def dotplot(
    request: DotplotModel,
    adinfo: AdataModel = AdataModel()
):
    """Plot dot plot of expression values per gene for each group."""
    try:
        result = await forward_request("pl_dotplot", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.dotplot, adata, request,adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def matrixplot(
    request: MatrixplotModel,
    adinfo: AdataModel = AdataModel()
):
    """matrixplot, Create a heatmap of the mean expression values per group of each var_names."""
    try:
        result = await forward_request("pl_matrixplot", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.matrixplot, adata, request,adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def tracksplot(
    request: TracksplotModel,
    adinfo: AdataModel = AdataModel()
):
    """tracksplot, compact plot of expression of a list of genes."""
    try:
        result = await forward_request("pl_tracksplot", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.tracksplot, adata, request,adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def scatter(
    request: EnhancedScatterModel = EnhancedScatterModel(),
    adinfo: AdataModel = AdataModel()
):
    """Plot a scatter plot of two variables, Scatter plot along observations or variables axes."""
    try:
        result = await forward_request("pl_scatter", request, adinfo)
        if result is not None:
            return result    
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.scatter, adata, request,adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def embedding(
    request: EmbeddingModel,
    adinfo: AdataModel = AdataModel()
):
    """Scatter plot for user specified embedding basis (e.g. umap, tsne, etc)."""
    try:
        result = await forward_request("pl_embedding", request, adinfo)
        if result is not None:
            return result       
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.embedding, adata, request,adinfo)
        return {"figpath": fig_path}
    except KeyError as e:
        raise ToolError(f"doest found {e} in current sampleid with adtype {adinfo.adtype}")
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@pl_mcp.tool()
async def embedding_density(
    request: EmbeddingDensityModel,
    adinfo: AdataModel = AdataModel()
):
    """Plot the density of cells in an embedding."""
    try:
        result = await forward_request("pl_embedding_density", request, adinfo)
        if result is not None:
            return result          
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.embedding_density, adata, request,adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@pl_mcp.tool()
async def rank_genes_groups(
    request: RankGenesGroupsModel,
    adinfo: AdataModel = AdataModel()
):
    """Plot ranking of genes based on differential expression."""
    try:
        result = await forward_request("pl_rank_genes_groups", request, adinfo)
        if result is not None:
            return result         
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.rank_genes_groups, adata, request,adinfo)
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
    adinfo: AdataModel = AdataModel()
):
    """Plot ranking of genes(DEGs) using dotplot visualization. Defualt plot DEGs for rank_genes_groups tool"""
    from fastmcp.exceptions import ClientError 
    try:
        result = await forward_request("pl_rank_genes_groups_dotplot", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.rank_genes_groups_dotplot, adata, request,adinfo)
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
    request: ClusterMapModel = ClusterMapModel(),
    adinfo: AdataModel = AdataModel()
):
    """Plot hierarchical clustering of cells and genes."""
    try:
        result = await forward_request("pl_clustermap", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.clustermap, adata, request,adinfo)
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
    request: HighlyVariableGenesModel = HighlyVariableGenesModel(),
    adinfo: AdataModel = AdataModel()
):
    """plot highly variable genes; Plot dispersions or normalized variance versus means for genes."""
    try:
        result = await forward_request("pl_highly_variable_genes", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.highly_variable_genes, adata, request,adinfo)
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
    request: PCAVarianceRatioModel = PCAVarianceRatioModel(),
    adinfo: AdataModel = AdataModel()
):
    """Plot the PCA variance ratio to visualize explained variance."""
    ### there is some bug, as scanpy.pl.pca_variance_ratio didn't return axis
    try:
        result = await forward_request("pl_pca_variance_ratio", request, adinfo)
        if result is not None:
            return result
        adata = get_ads().get_adata(adinfo=adinfo)
        fig_path = sc_like_plot(sc.pl.pca_variance_ratio, adata, request,adinfo)
        return {"figpath": fig_path}
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)
