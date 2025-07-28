from pydantic import BaseModel, ConfigDict


class PostingModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
