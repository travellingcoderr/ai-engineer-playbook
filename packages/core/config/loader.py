from pydantic import Field, BaseModel

class LoaderConfiguration(BaseModel):
    strategy: str = Field(default="auto", description="How to load documents (e.g., auto, pdf, markdown)")
