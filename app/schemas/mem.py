from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, FileUrl, UrlConstraints
from pydantic_core import Url


class MemesCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=200)



class MemesUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=200)


class MemesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str