from pydantic import BaseModel, HttpUrl


class LinkCreate(BaseModel):
    title: str
    url: HttpUrl
    description: str | None = None
    is_favorite: bool = False


class LinkUpdate(BaseModel):
    title: str
    url: HttpUrl
    description: str | None = None
    is_favorite: bool = False