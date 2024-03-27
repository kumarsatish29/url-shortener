import json
import os
from collections.abc import Generator
from datetime import datetime, timezone

from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import ShortenedUrl, get_db_session
from .service import create_short_link

fastapi_app = FastAPI()

CORS_ORIGINS = json.loads(os.getenv("CORS_ORIGINS", "[]"))
DEFAULT_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8001",
]


def get_allowed_origins(origins_: list[str]) -> Generator[str]:
    """
    Returns domain with and without trailing slash
    """
    for origin in filter(lambda x: x, origins_):
        if origin.endswith("/"):
            origin = origin[:-1]
        yield origin + "/"
        yield origin


fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=list(get_allowed_origins(CORS_ORIGINS or DEFAULT_ORIGINS)),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapi_app.post("/api/shorten")
def get_short_link(
    db: Session = Depends(get_db_session), url: HttpUrl = Body(..., embed=True)
):

    timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    short_link = create_short_link(url, timestamp)
    obj = ShortenedUrl(original_url=url, short_link=short_link)
    db.add(obj)
    db.commit()

    return {"short_link": short_link}


@fastapi_app.get("/{short_link}")
def redirect(short_link: str, db: Session = Depends(get_db_session)):
    obj = (
        db.query(ShortenedUrl)
        .filter_by(short_link=short_link)
        .order_by(ShortenedUrl.id.desc())
        .first()
    )
    if obj is None:
        raise HTTPException(
            status_code=404, detail="The link does not exist, could not redirect."
        )
    return RedirectResponse(url=obj.original_url)
