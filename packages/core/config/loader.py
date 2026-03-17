from pydantic import Field, BaseModel
from packages.core.enums import LoaderStrategy

class LoaderConfiguration(BaseModel):
    strategy: LoaderStrategy = Field(default=LoaderStrategy.SIMPLE, description="How to load documents (e.g., auto, pdf, markdown)")
