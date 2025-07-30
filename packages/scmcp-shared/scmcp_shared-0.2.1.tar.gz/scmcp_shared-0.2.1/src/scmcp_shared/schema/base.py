from pydantic import Field, BaseModel,ConfigDict


class AdataModel(BaseModel):
    """Input schema for the adata tool."""
    sampleid: str = Field(default=None, description="adata sampleid")
    adtype: str = Field(default="exp", description="adata.X data type")

    model_config = ConfigDict(
        extra="ignore"
    )
