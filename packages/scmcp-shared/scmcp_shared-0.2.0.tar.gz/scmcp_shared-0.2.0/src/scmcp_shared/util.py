import inspect
import os
from pathlib import Path
from fastmcp.server.dependencies import get_context



def get_env(key):
    return os.environ.get(f"SCMCP_{key.upper()}")

 
def filter_args(request, func, **extra_kwargs):
    kwargs = request.model_dump()
    args = request.model_fields_set
    parameters = inspect.signature(func).parameters
    extra_kwargs = {k: extra_kwargs[k] for k in extra_kwargs if k in parameters}
    func_kwargs = {k: kwargs.get(k) for k in args if k in parameters}
    func_kwargs.update(extra_kwargs)
    return func_kwargs


def add_op_log(adata, func, kwargs):
    import hashlib
    import json
    
    if "operation" not in adata.uns:
        adata.uns["operation"] = {}
        adata.uns["operation"]["op"] = {}
        adata.uns["operation"]["opid"] = []
    # Handle different function types to get the function name
    if hasattr(func, "func") and hasattr(func.func, "__name__"):
        # For partial functions, use the original function name
        func_name = func.func.__name__
    elif hasattr(func, "__name__"):
        func_name = func.__name__
    elif hasattr(func, "__class__"):
        func_name = func.__class__.__name__
    else:
        func_name = str(func)
    new_kwargs = {}
    for k,v in kwargs.items():
        if isinstance(v, tuple):
            new_kwargs[k] = list(v)
        else:
            new_kwargs[k] = v
    try:
        kwargs_str = json.dumps(new_kwargs, sort_keys=True)
    except:
        kwargs_str = str(new_kwargs)
    hash_input = f"{func_name}:{kwargs_str}"
    hash_key = hashlib.md5(hash_input.encode()).hexdigest()
    adata.uns["operation"]["op"][hash_key] = {func_name: new_kwargs}
    adata.uns["operation"]["opid"].append(hash_key)
    from .logging_config import setup_logger
    logger = setup_logger(log_file=get_env("LOG_FILE"))
    logger.info(f"{func}: {new_kwargs}")



def savefig(axes, file):
    from matplotlib.axes import Axes

    try:
        file_path = Path(file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(axes, list):
            if isinstance(axes[0], Axes):
                axes[0].figure.savefig(file_path)
        elif isinstance(axes, dict):
            ax = list(axes.values())[0]
            if isinstance(ax, Axes):
                ax.figure.savefig(file_path)
        elif isinstance(axes, Axes):
            axes.figure.savefig(file_path)
        elif hasattr(axes, 'savefig'):  # if Figure 
            axes.savefig(file_path)
        elif hasattr(axes, 'save'):  # for plotnine.ggplot.ggplot
            axes.save(file_path)
        else:
            raise ValueError(f"axes must be a Axes or plotnine object, but got {type(axes)}")
        return file_path
    except Exception as e:
        raise e


def set_fig_path(axes, func=None, **kwargs):
    if hasattr(func, "func") and hasattr(func.func, "__name__"):
        # For partial functions, use the original function name
        func_name = func.func.__name__
    elif hasattr(func, "__name__"):
        func_name = func.__name__
    elif hasattr(func, "__class__"):
        func_name = func.__class__.__name__
    else:
        func_name = str(func)

    fig_dir = Path(os.getcwd()) / "figures"
    kwargs.pop("save", None)
    kwargs.pop("show", None)
    args = []
    for k,v in kwargs.items():
        if isinstance(v, (tuple, list, set)):
            args.append(f"{k}-{'-'.join([str(i) for i in v])}")
        else:
            args.append(f"{k}-{v}")
    args_str = "_".join(args)
    fig_path = fig_dir / f"{func_name}_{args_str}.png"
    try:
        savefig(axes, fig_path)
    except PermissionError:
        raise PermissionError("You don't have permission to rename this file")
    except Exception as e:
        raise e
    transport = get_env("TRANSPORT") 
    if transport == "stdio":
        return fig_path
    else:
        host = get_env("HOST")
        port = get_env("PORT")
        fig_path = f"http://{host}:{port}/figures/{Path(fig_path).name}"
        return fig_path



async def get_figure(request):
    from starlette.responses import FileResponse, Response

    figure_name = request.path_params["figure_name"]
    figure_path = f"./figures/{figure_name}"
    
    if not os.path.isfile(figure_path):
        return Response(content={"error": "figure not found"}, media_type="application/json")
    
    return FileResponse(figure_path)


async def forward_request(func, request, **kwargs):
    from fastmcp import Client
    forward_url = get_env("FORWARD")
    request_kwargs = request.model_dump()
    request_args = request.model_fields_set
    func_kwargs = {"request": {k: request_kwargs.get(k) for k in request_args}}
    func_kwargs.update({k:v for k,v in kwargs.items() if v is not None})
    if not forward_url:
        return None
        
    client = Client(forward_url)
    async with client:
        tools = await client.list_tools()
        func = [t.name for t in tools if t.name.endswith(func)][0]
        try:
            result = await client.call_tool(func, func_kwargs)
            return result
        except Exception as e:
            raise e

def obsm2adata(adata, obsm_key):
    from anndata import AnnData

    if obsm_key not in adata.obsm_keys():
        raise ValueError(f"key {obsm_key} not found in adata.obsm")
    else:
        return AnnData(adata.obsm[obsm_key], obs=adata.obs, obsm=adata.obsm)


async def get_figure(request):
    figure_name = request.path_params["figure_name"]
    figure_path = f"./figures/{figure_name}"
    
    if not os.path.isfile(figure_path):
        return Response(content={"error": "figure not found"}, media_type="application/json")
    
    return FileResponse(figure_path)


def add_figure_route(server):
    from starlette.routing import Route
    server._additional_http_routes = [Route("/figures/{figure_name}", endpoint=get_figure)]


def get_ads():
    ctx = get_context()
    ads = ctx.request_context.lifespan_context
    return ads


def generate_msg(request, adata, ads):
    kwargs = request.model_dump()
    sampleid = kwargs.get("sampleid")
    dtype = kwargs.get("dtype", "exp")
    return {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}


def sc_like_plot(plot_func, adata, request, **kwargs):
    func_kwargs = filter_args(request, plot_func, show=False, save=False)
    axes = plot_func(adata, **func_kwargs)
    fig_path = set_fig_path(axes, plot_func, **func_kwargs)
    add_op_log(adata, plot_func, func_kwargs)
    return fig_path


async def filter_tools(mcp, include_tools=None, exclude_tools=None):
    tools = await mcp.get_tools()
    for tool in tools:
        if exclude_tools and tool in exclude_tools:
            mcp.remove_tool(tool)
        if include_tools and tool not in include_tools:
            mcp.remove_tool(tool)
    return mcp