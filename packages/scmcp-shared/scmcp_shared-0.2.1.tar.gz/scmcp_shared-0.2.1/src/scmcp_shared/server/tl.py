from fastmcp import FastMCP, Context
import os
import scanpy as sc
from fastmcp.exceptions import ToolError
from ..schema.tl import *
from scmcp_shared.util import filter_args, add_op_log, forward_request, get_ads, generate_msg
from scmcp_shared.logging_config import setup_logger
logger = setup_logger()

tl_mcp = FastMCP("ScanpyMCP-TL-Server")


@tl_mcp.tool()
async def tsne(
    request: TSNEModel = TSNEModel() 
):
    """t-distributed stochastic neighborhood embedding (t-SNE) for visualization"""

    try:
        result = await forward_request("tl_tsne", request)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.tl.tsne)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.tsne(adata, **func_kwargs)
        add_op_log(adata, sc.tl.tsne, func_kwargs)
        return generate_msg(request, adata, ads)
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@tl_mcp.tool()
async def umap(
    request: UMAPModel = UMAPModel() 
):
    """Uniform Manifold Approximation and Projection (UMAP) for visualization"""

    try:
        result = await forward_request("tl_umap", request)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.tl.umap)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.umap(adata, **func_kwargs)
        add_op_log(adata, sc.tl.umap, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@tl_mcp.tool()
async def draw_graph(
    request: DrawGraphModel = DrawGraphModel() 
):
    """Force-directed graph drawing"""

    try:
        result = await forward_request("tl_draw_graph", request)
        if result is not None:
            return result    
        func_kwargs = filter_args(request, sc.tl.draw_graph)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.draw_graph(adata, **func_kwargs)
        add_op_log(adata, sc.tl.draw_graph, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@tl_mcp.tool()
async def diffmap(
    request: DiffMapModel = DiffMapModel() 
):
    """Diffusion Maps for dimensionality reduction"""

    try:
        result = await forward_request("tl_diffmap", request)
        if result is not None:
            return result    
        func_kwargs = filter_args(request, sc.tl.diffmap)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.diffmap(adata, **func_kwargs)
        adata.obsm["X_diffmap"] = adata.obsm["X_diffmap"][:,1:]
        add_op_log(adata, sc.tl.diffmap, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@tl_mcp.tool()
async def embedding_density(
    request: EmbeddingDensityModel = EmbeddingDensityModel() 
):
    """Calculate the density of cells in an embedding"""

    try:
        result = await forward_request("tl_embedding_density", request)
        if result is not None:
            return result        
        func_kwargs = filter_args(request, sc.tl.embedding_density)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.embedding_density(adata, **func_kwargs)
        add_op_log(adata, sc.tl.embedding_density, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@tl_mcp.tool()
async def leiden(
    request: LeidenModel = LeidenModel() 
):
    """Leiden clustering algorithm for community detection"""

    try:
        result = await forward_request("tl_leiden", request)
        if result is not None:
            return result            
        func_kwargs = filter_args(request, sc.tl.leiden)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.leiden(adata, **func_kwargs)
        add_op_log(adata, sc.tl.leiden, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@tl_mcp.tool()
async def louvain(
    request: LouvainModel = LouvainModel() 
):
    """Louvain clustering algorithm for community detection"""

    try:
        result = await forward_request("tl_louvain", request)
        if result is not None:
            return result          
        func_kwargs = filter_args(request, sc.tl.louvain)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.louvain(adata, **func_kwargs)
        add_op_log(adata, sc.tl.louvain, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@tl_mcp.tool()
async def dendrogram(
    request: DendrogramModel,
):
    """Hierarchical clustering dendrogram"""

    try:
        result = await forward_request("tl_dendrogram", request)
        if result is not None:
            return result        
        func_kwargs = filter_args(request, sc.tl.dendrogram)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.dendrogram(adata, **func_kwargs)
        add_op_log(adata, sc.tl.dendrogram, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@tl_mcp.tool()
async def dpt(
    request: DPTModel = DPTModel() 
):
    """Diffusion Pseudotime (DPT) analysis"""

    try:
        result = await forward_request("tl_dpt", request)
        if result is not None:
            return result          
        func_kwargs = filter_args(request, sc.tl.dpt)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.dpt(adata, **func_kwargs)
        add_op_log(adata, sc.tl.dpt, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@tl_mcp.tool()
async def paga(
    request: PAGAModel = PAGAModel() 
):
    """Partition-based graph abstraction"""

    try:
        result = await forward_request("tl_paga", request)
        if result is not None:
            return result         
        func_kwargs = filter_args(request, sc.tl.paga)
        ads = get_ads()
        adata = ads.get_adata(request=request)    
        sc.tl.paga(adata, **func_kwargs)
        add_op_log(adata, sc.tl.paga, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@tl_mcp.tool()
async def ingest(
    request: IngestModel = IngestModel() 
):
    """Map labels and embeddings from reference data to new data"""

    try:
        result = await forward_request("tl_ingest", request)
        if result is not None:
            return result       
        func_kwargs = filter_args(request, sc.tl.ingest)
        ads = get_ads()
        adata = ads.get_adata(request=request)    
        sc.tl.ingest(adata, **func_kwargs)
        add_op_log(adata, sc.tl.ingest, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@tl_mcp.tool()
async def rank_genes_groups(
    request: RankGenesGroupsModel,

):
    """Rank genes for characterizing groups, for differentially expressison analysis"""

    try:
        result = await forward_request("tl_rank_genes_groups", request)
        if result is not None:
            return result         
        func_kwargs = filter_args(request, sc.tl.rank_genes_groups)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.rank_genes_groups(adata, **func_kwargs)
        add_op_log(adata, sc.tl.rank_genes_groups, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@tl_mcp.tool()
async def filter_rank_genes_groups(
    request: FilterRankGenesGroupsModel = FilterRankGenesGroupsModel() 
):
    """Filter out genes based on fold change and fraction of genes"""

    try:
        result = await forward_request("tl_filter_rank_genes_groups", request)
        if result is not None:
            return result          
        func_kwargs = filter_args(request, sc.tl.filter_rank_genes_groups)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.filter_rank_genes_groups(adata, **func_kwargs)
        add_op_log(adata, sc.tl.filter_rank_genes_groups, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@tl_mcp.tool()
async def marker_gene_overlap(
    request: MarkerGeneOverlapModel = MarkerGeneOverlapModel() 
):
    """Calculate overlap between data-derived marker genes and reference markers"""

    try:
        result = await forward_request("tl_marker_gene_overlap", request)
        if result is not None:
            return result         
        func_kwargs = filter_args(request, sc.tl.marker_gene_overlap)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.marker_gene_overlap(adata, **func_kwargs)
        add_op_log(adata, sc.tl.marker_gene_overlap, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@tl_mcp.tool()
async def score_genes(
    request: ScoreGenesModel,
    
):
    """Score a set of genes based on their average expression"""
    try:
        result = await forward_request("tl_score_genes", request)
        if result is not None:
            return result       
        func_kwargs = filter_args(request, sc.tl.score_genes)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.score_genes(adata, **func_kwargs)
        add_op_log(adata, sc.tl.score_genes, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)

@tl_mcp.tool()
async def score_genes_cell_cycle(
    request: ScoreGenesCellCycleModel,
    
):
    """Score cell cycle genes and assign cell cycle phases"""

    try:
        result = await forward_request("tl_score_genes_cell_cycle", request)
        if result is not None:
            return result       
        func_kwargs = filter_args(request, sc.tl.score_genes_cell_cycle)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.tl.score_genes_cell_cycle(adata, **func_kwargs)
        add_op_log(adata, sc.tl.score_genes_cell_cycle, func_kwargs)
        return [generate_msg(request, adata, ads)]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)


@tl_mcp.tool()
async def pca(
    request: PCAModel = PCAModel() 
):
    """Principal component analysis"""

    try:
        result = await forward_request("tl_pca", request)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pp.pca)
        ads = get_ads()
        adata = ads.get_adata(request=request)
        sc.pp.pca(adata, **func_kwargs)
        add_op_log(adata, sc.pp.pca, func_kwargs)
        return [
            generate_msg(request, adata, ads)
        ]
    except ToolError as e:
        raise ToolError(e)
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise ToolError(e.__context__)
        else:
            raise ToolError(e)