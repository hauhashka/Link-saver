from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="Link Saver")


class LinkCreate(BaseModel):
    title: str
    url: HttpUrl
    description: str | None = None
    is_favorite: bool = False


class Link(LinkCreate):
    id: int


links: list[Link] = []
next_id = 1


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/links")
def get_links(favorite: bool | None = None):
    if favorite is None:
        return links

    return [link for link in links if link.is_favorite == favorite]


@app.post("/links", status_code=201)
def create_link(link_data: LinkCreate):
    global next_id

    new_link = Link(
        id=next_id,
        title=link_data.title,
        url=link_data.url,
        description=link_data.description,
        is_favorite=link_data.is_favorite,
    )

    links.append(new_link)
    next_id += 1

    return new_link


@app.get("/links/{link_id}")
def get_link(link_id: int):
    for link in links:
        if link.id == link_id:
            return link

    raise HTTPException(status_code=404, detail="Link not found")


@app.put("/links/{link_id}")
def update_link(link_id: int, link_data: LinkCreate):
    for index, link in enumerate(links):
        if link.id == link_id:
            updated_link = Link(
                id=link.id,
                title=link_data.title,
                url=link_data.url,
                description=link_data.description,
                is_favorite=link_data.is_favorite,
            )

            links[index] = updated_link
            return updated_link

    raise HTTPException(status_code=404, detail="Link not found")


@app.delete("/links/{link_id}")
def delete_link(link_id: int):
    for index, link in enumerate(links):
        if link.id == link_id:
            deleted_link = links.pop(index)
            return deleted_link

    raise HTTPException(status_code=404, detail="Link not found")