from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlmodel import Field, Session, SQLModel, create_engine, select


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if database_url is None:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(database_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Link Saver", lifespan=lifespan)


class Link(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    url: str
    description: str | None = None
    is_favorite: bool = False


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


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/links")
def get_links(
    favorite: bool | None = None,
    search: str | None = None,
):
    with Session(engine) as session:
        statement = select(Link)
        links = session.exec(statement).all()

        if favorite is not None:
            links = [
                link for link in links
                if link.is_favorite == favorite
            ]

        if search is not None:
            search_lower = search.lower()

            links = [
                link for link in links
                if search_lower in link.title.lower()
                or (
                    link.description is not None
                    and search_lower in link.description.lower()
                )
            ]

        return links


@app.post("/links", status_code=201)
def create_link(link_data: LinkCreate):
    link = Link(
        title=link_data.title,
        url=str(link_data.url),
        description=link_data.description,
        is_favorite=link_data.is_favorite,
    )

    with Session(engine) as session:
        session.add(link)
        session.commit()
        session.refresh(link)

        return link


@app.get("/links/{link_id}")
def get_link(link_id: int):
    with Session(engine) as session:
        link = session.get(Link, link_id)

        if link is None:
            raise HTTPException(status_code=404, detail="Link not found")

        return link


@app.put("/links/{link_id}")
def update_link(link_id: int, link_data: LinkUpdate):
    with Session(engine) as session:
        link = session.get(Link, link_id)

        if link is None:
            raise HTTPException(status_code=404, detail="Link not found")

        link.title = link_data.title
        link.url = str(link_data.url)
        link.description = link_data.description
        link.is_favorite = link_data.is_favorite

        session.add(link)
        session.commit()
        session.refresh(link)

        return link


@app.delete("/links/{link_id}")
def delete_link(link_id: int):
    with Session(engine) as session:
        link = session.get(Link, link_id)

        if link is None:
            raise HTTPException(status_code=404, detail="Link not found")

        session.delete(link)
        session.commit()

        return {"message": "Link deleted successfully", "deleted_link": link}