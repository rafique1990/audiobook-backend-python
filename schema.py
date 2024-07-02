from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session


class UserSubscriptionLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.user_id", primary_key=True
    )
    subscription_id: Optional[int] = Field(
        default=None, foreign_key="subscription.subscription_id", primary_key=True
    )
    start_date: datetime
    end_date: datetime


class AudiobookCategoryLink(SQLModel, table=True):
    audiobook_id: Optional[int] = Field(
        default=None, foreign_key="audiobook.audiobook_id", primary_key=True
    )
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.category_id", primary_key=True
    )


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., max_length=50, unique=True)
    name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100, unique=True)
    password: str = Field(..., max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    subscriptions: List["Subscription"] = Relationship(
        back_populates="users", link_model=UserSubscriptionLink
    )
    listening_histories: List["ListeningHistory"] = Relationship(back_populates="user")
    bookmarks: List["Bookmark"] = Relationship(back_populates="user")
    reviews: List["Review"] = Relationship(back_populates="user")
    ratings: List["Rating"] = Relationship(back_populates="user")
    purchases: List["Purchase"] = Relationship(back_populates="user")


class Subscription(SQLModel, table=True):
    subscription_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=50)
    price: float = Field(...)
    duration_days: int = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    users: List[User] = Relationship(
        back_populates="subscriptions", link_model=UserSubscriptionLink
    )


class Author(SQLModel, table=True):
    author_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=255)
    bio: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    audiobooks: List["Audiobook"] = Relationship(back_populates="author")


class Narrator(SQLModel, table=True):
    narrator_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=255)
    bio: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    audiobooks: List["Audiobook"] = Relationship(back_populates="narrator")


class Audiobook(SQLModel, table=True):
    audiobook_id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., max_length=255)
    author_id: int = Field(default=None, foreign_key="author.author_id")
    narrator_id: Optional[int] = Field(default=None, foreign_key="narrator.narrator_id")
    duration: int = Field(...)  # in seconds
    description: Optional[str] = None
    release_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    author: "Author" = Relationship(back_populates="audiobooks")
    narrator: "Narrator" = Relationship(back_populates="audiobooks")
    chapters: List["Chapter"] = Relationship(back_populates="audiobook")
    categories: List["Category"] = Relationship(
        back_populates="audiobooks", link_model=AudiobookCategoryLink
    )
    listening_histories: List["ListeningHistory"] = Relationship(
        back_populates="audiobook"
    )
    bookmarks: List["Bookmark"] = Relationship(back_populates="audiobook")
    reviews: List["Review"] = Relationship(back_populates="audiobook")
    ratings: List["Rating"] = Relationship(back_populates="audiobook")
    purchases: List["Purchase"] = Relationship(back_populates="audiobook")


class Chapter(SQLModel, table=True):
    chapter_id: Optional[int] = Field(default=None, primary_key=True)
    audiobook_id: int = Field(default=None, foreign_key="audiobook.audiobook_id")
    title: Optional[str] = Field(..., max_length=255)
    duration: int = Field(...)  # in seconds
    position: int = Field(...)  # order of the chapter in the audiobook
    created_at: datetime = Field(default_factory=datetime.utcnow)

    audiobook: "Audiobook" = Relationship(back_populates="chapters")


class Category(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=255, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    audiobooks: List[Audiobook] = Relationship(
        back_populates="categories", link_model=AudiobookCategoryLink
    )


class ListeningHistory(SQLModel, table=True):
    history_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.user_id")
    audiobook_id: int = Field(default=None, foreign_key="audiobook.audiobook_id")
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None

    user: "User" = Relationship(back_populates="listening_histories")
    audiobook: "Audiobook" = Relationship(back_populates="listening_histories")


class Bookmark(SQLModel, table=True):
    bookmark_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.user_id")
    audiobook_id: int = Field(default=None, foreign_key="audiobook.audiobook_id")
    chapter_id: Optional[int] = Field(default=None, foreign_key="chapter.chapter_id")
    position: int = Field(...)  # in seconds
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="bookmarks")
    audiobook: "Audiobook" = Relationship(back_populates="bookmarks")
    chapter: Optional["Chapter"] = Relationship()


class Review(SQLModel, table=True):
    review_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.user_id")
    audiobook_id: int = Field(default=None, foreign_key="audiobook.audiobook_id")
    review_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="reviews")
    audiobook: "Audiobook" = Relationship(back_populates="reviews")


class Rating(SQLModel, table=True):
    rating_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.user_id")
    audiobook_id: int = Field(default=None, foreign_key="audiobook.audiobook_id")
    rating: int = Field(...)  # out of 5
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="ratings")
    audiobook: "Audiobook" = Relationship(back_populates="ratings")


class Purchase(SQLModel, table=True):
    purchase_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.user_id")
    audiobook_id: int = Field(default=None, foreign_key="audiobook.audiobook_id")
    purchase_date: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="purchases")
    audiobook: "Audiobook" = Relationship(back_populates="purchases")


# Create an SQLite database (or connect to an existing one)
sqlite_file_name = "test/test_audiobook_app.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

## Adds Pydantic classes

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# User Models
class UserBase(SQLModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Subscription Models
class SubscriptionBase(SQLModel):
    name: str
    price: float
    duration_days: int


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionRead(SubscriptionBase):
    subscription_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# UserSubscription Models
class UserSubscriptionBase(SQLModel):
    start_date: datetime
    end_date: datetime


class UserSubscriptionCreate(UserSubscriptionBase):
    user_id: int
    subscription_id: int


class UserSubscriptionRead(UserSubscriptionBase):
    user_subscription_id: int
    user: UserRead
    subscription: SubscriptionRead

    class Config:
        orm_mode = True


# Author Models
class AuthorBase(SQLModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Narrator Models
class NarratorBase(SQLModel):
    name: str
    bio: Optional[str] = None


class NarratorCreate(NarratorBase):
    pass


class NarratorRead(NarratorBase):
    narrator_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Audiobook Models
class AudiobookBase(SQLModel):
    title: str
    author_id: int
    narrator_id: Optional[int] = None
    duration: int
    description: Optional[str] = None
    release_date: Optional[datetime] = None


class AudiobookCreate(AudiobookBase):
    pass


class AudiobookRead(AudiobookBase):
    audiobook_id: int
    created_at: datetime
    author: AuthorRead
    narrator: Optional[NarratorRead] = None

    class Config:
        orm_mode = True


# Chapter Models
class ChapterBase(SQLModel):
    audiobook_id: int
    title: Optional[str] = None
    duration: int
    position: int


class ChapterCreate(ChapterBase):
    pass


class ChapterRead(ChapterBase):
    chapter_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Category Models
class CategoryBase(SQLModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    category_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# AudiobookCategory Models
class AudiobookCategoryBase(SQLModel):
    audiobook_id: int
    category_id: int


class AudiobookCategoryCreate(AudiobookCategoryBase):
    pass


class AudiobookCategoryRead(AudiobookCategoryBase):
    pass

    class Config:
        orm_mode = True


# ListeningHistory Models
class ListeningHistoryBase(SQLModel):
    user_id: int
    audiobook_id: int
    started_at: datetime
    finished_at: Optional[datetime] = None


class ListeningHistoryCreate(ListeningHistoryBase):
    pass


class ListeningHistoryRead(ListeningHistoryBase):
    history_id: int

    class Config:
        orm_mode = True


# Bookmark Models
class BookmarkBase(SQLModel):
    user_id: int
    audiobook_id: int
    chapter_id: Optional[int] = None
    position: int


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkRead(BookmarkBase):
    bookmark_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Review Models
class ReviewBase(SQLModel):
    user_id: int
    audiobook_id: int
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    review_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Rating Models
class RatingBase(SQLModel):
    user_id: int
    audiobook_id: int
    rating: int  # out of 5


class RatingCreate(RatingBase):
    pass


class RatingRead(RatingBase):
    rating_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Purchase Models
class PurchaseBase(SQLModel):
    user_id: int
    audiobook_id: int
    purchase_date: datetime


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseRead(PurchaseBase):
    purchase_id: int

    class Config:
        orm_mode = True


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
