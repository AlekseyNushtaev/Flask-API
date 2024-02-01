from abc import ABC
import pydantic
from typing import Optional

class AbstractAdvert(pydantic.BaseModel, ABC):
    title: str
    owner: str

    @pydantic.field_validator("owner")
    @classmethod
    def check_owner(cls, v: str):
        if len(v) > 10:
            raise ValueError(f"Maximal length of owner is 10")
        return v


    @pydantic.field_validator("title")
    @classmethod
    def check_title(cls, v: str):
        if len(v) > 20:
            raise ValueError(f"Maximal length of title is 20")
        return v


class CreateAdvert(AbstractAdvert):
    title: str
    description: str
    owner: str

class UpdateAdvert(AbstractAdvert):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None