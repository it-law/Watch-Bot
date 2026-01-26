from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_basic_auth
from app.models import Post, Publication
from app.schemas import PostRead, PublicationRead
from app.workers.tasks import publish_publication

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_basic_auth)])


@router.get("/posts", response_model=list[PostRead])
def list_posts(db: Session = Depends(get_db)) -> list[Post]:
    return db.query(Post).order_by(Post.created_at.desc()).all()


@router.get("/publications", response_model=list[PublicationRead])
def list_publications(db: Session = Depends(get_db)) -> list[Publication]:
    return db.query(Publication).order_by(Publication.updated_at.desc()).all()


@router.post("/publications/{publication_id}/retry", response_model=PublicationRead)
def retry_publication(publication_id: int, db: Session = Depends(get_db)) -> Publication:
    publication = db.get(Publication, publication_id)
    if not publication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    publish_publication.delay(publication_id)
    return publication
