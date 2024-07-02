from fastapi import FastAPI
import uvicorn

from routers import (
    user_router,
    subscription_router,
    author_router,
    narrator_router,
    audiobook_router,
    chapter_router,
    category_router,
    listening_history_router,
    bookmark_router,
    review_router,
    rating_router,
    purchase_router,
    web,
)
from database import create_db_and_tables

app = FastAPI(title="Audio Book App")

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(subscription_router.router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(author_router.router, prefix="/authors", tags=["authors"])
app.include_router(narrator_router.router, prefix="/narrators", tags=["narrators"])
app.include_router(audiobook_router.router, prefix="/audiobooks", tags=["audiobooks"])
app.include_router(chapter_router.router, prefix="/chapters", tags=["chapters"])
app.include_router(category_router.router, prefix="/categories", tags=["categories"])
app.include_router(listening_history_router.router, prefix="/listening_histories", tags=["listening_histories"])
app.include_router(bookmark_router.router, prefix="/bookmarks", tags=["bookmarks"])
app.include_router(review_router.router, prefix="/reviews", tags=["reviews"])
app.include_router(rating_router.router, prefix="/ratings", tags=["ratings"])
app.include_router(purchase_router.router, prefix="/purchases", tags=["purchases"])
app.include_router(web.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
