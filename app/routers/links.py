from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from app.database import engine
from app.models import Link
from app.schemas import LinkCreate, LinkUpdate


router = APIRouter(prefix="/links", tags=["links"])


@router.get("")
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


@router.post("", status_code=201)
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


@router.get("/{link_id}")
def get_link(link_id: int):
    with Session(engine) as session:
        link = session.get(Link, link_id)

        if link is None:
            raise HTTPException(status_code=404, detail="Link not found")

        return link


@router.put("/{link_id}")
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


@router.delete("/{link_id}")
def delete_link(link_id: int):
    with Session(engine) as session:
        link = session.get(Link, link_id)

        if link is None:
            raise HTTPException(status_code=404, detail="Link not found")

        session.delete(link)
        session.commit()

        return {
            "message": "Link deleted successfully",
            "deleted_link": link,
        }