from sqlmodel import Session, create_engine, SQLModel
from schema import (
    User,
    Subscription,
    Author,
    Narrator,
    Audiobook,
    Chapter,
    Category,
    ListeningHistory,
    Bookmark,
    Review,
    Rating,
    Purchase,
    UserSubscriptionLink,
    AudiobookCategoryLink,
)
from datetime import datetime

# Database URL for SQLite
DATABASE_URL = "sqlite:///test_audiobook_app.db"

# Create a new SQLite engine instance
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables in the database
SQLModel.metadata.create_all(engine)

# Create a new session
with Session(engine) as session:
    # Adding sample users
    user1 = User(
        username="user1",
        name="John Doe",
        email="john@example.com",
        password="password1",
        created_at=datetime.utcnow(),
    )
    user2 = User(
        username="user2",
        name="Jane Smith",
        email="jane@example.com",
        password="password2",
        created_at=datetime.utcnow(),
    )
    user3 = User(
        username="user3",
        name="Alice Johnson",
        email="alice@example.com",
        password="password3",
        created_at=datetime.utcnow(),
    )

    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.flush()  # Ensure IDs are populated

    # Adding sample subscriptions
    subscription1 = Subscription(
        name="Monthly Plan", price=9.99, duration_days=30, created_at=datetime.utcnow()
    )
    subscription2 = Subscription(
        name="Quarterly Plan",
        price=27.99,
        duration_days=90,
        created_at=datetime.utcnow(),
    )
    subscription3 = Subscription(
        name="Yearly Plan", price=99.99, duration_days=365, created_at=datetime.utcnow()
    )

    session.add(subscription1)
    session.add(subscription2)
    session.add(subscription3)
    session.flush()  # Ensure IDs are populated

    # Linking users to subscriptions
    user_sub1 = UserSubscriptionLink(
        user_id=user1.user_id,
        subscription_id=subscription1.subscription_id,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
    )
    user_sub2 = UserSubscriptionLink(
        user_id=user2.user_id,
        subscription_id=subscription2.subscription_id,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
    )
    user_sub3 = UserSubscriptionLink(
        user_id=user3.user_id,
        subscription_id=subscription3.subscription_id,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
    )

    session.add(user_sub1)
    session.add(user_sub2)
    session.add(user_sub3)
    session.flush()  # Ensure IDs are populated

    # Adding sample authors
    author1 = Author(name="Author One", created_at=datetime.utcnow())
    author2 = Author(name="Author Two", created_at=datetime.utcnow())
    author3 = Author(name="Author Three", created_at=datetime.utcnow())

    session.add(author1)
    session.add(author2)
    session.add(author3)
    session.flush()  # Ensure IDs are populated

    # Adding sample narrators
    narrator1 = Narrator(name="Narrator One", created_at=datetime.utcnow())
    narrator2 = Narrator(name="Narrator Two", created_at=datetime.utcnow())
    narrator3 = Narrator(name="Narrator Three", created_at=datetime.utcnow())

    session.add(narrator1)
    session.add(narrator2)
    session.add(narrator3)
    session.flush()  # Ensure IDs are populated

    # Adding sample audiobooks
    audiobook1 = Audiobook(
        title="Audiobook One",
        author_id=author1.author_id,
        narrator_id=narrator1.narrator_id,
        duration=600,
        created_at=datetime.utcnow(),
    )
    audiobook2 = Audiobook(
        title="Audiobook Two",
        author_id=author2.author_id,
        narrator_id=narrator2.narrator_id,
        duration=1200,
        created_at=datetime.utcnow(),
    )
    audiobook3 = Audiobook(
        title="Audiobook Three",
        author_id=author3.author_id,
        narrator_id=narrator3.narrator_id,
        duration=1800,
        created_at=datetime.utcnow(),
    )

    session.add(audiobook1)
    session.add(audiobook2)
    session.add(audiobook3)
    session.flush()  # Ensure IDs are populated

    # Linking audiobooks to categories
    category1 = Category(name="Category One", created_at=datetime.utcnow())
    category2 = Category(name="Category Two", created_at=datetime.utcnow())
    category3 = Category(name="Category Three", created_at=datetime.utcnow())

    session.add(category1)
    session.add(category2)
    session.add(category3)
    session.flush()  # Ensure IDs are populated

    audiobook_category1 = AudiobookCategoryLink(
        audiobook_id=audiobook1.audiobook_id, category_id=category1.category_id
    )
    audiobook_category2 = AudiobookCategoryLink(
        audiobook_id=audiobook2.audiobook_id, category_id=category2.category_id
    )
    audiobook_category3 = AudiobookCategoryLink(
        audiobook_id=audiobook3.audiobook_id, category_id=category3.category_id
    )

    session.add(audiobook_category1)
    session.add(audiobook_category2)
    session.add(audiobook_category3)
    session.flush()  # Ensure IDs are populated

    # Adding sample chapters
    chapter1 = Chapter(
        audiobook_id=audiobook1.audiobook_id,
        title="Chapter One",
        duration=300,
        position=1,
        created_at=datetime.utcnow(),
    )
    chapter2 = Chapter(
        audiobook_id=audiobook2.audiobook_id,
        title="Chapter Two",
        duration=300,
        position=1,
        created_at=datetime.utcnow(),
    )
    chapter3 = Chapter(
        audiobook_id=audiobook3.audiobook_id,
        title="Chapter Three",
        duration=300,
        position=1,
        created_at=datetime.utcnow(),
    )

    session.add(chapter1)
    session.add(chapter2)
    session.add(chapter3)
    session.flush()  # Ensure IDs are populated

    # Adding sample listening histories
    history1 = ListeningHistory(
        user_id=user1.user_id,
        audiobook_id=audiobook1.audiobook_id,
        started_at=datetime.utcnow(),
    )
    history2 = ListeningHistory(
        user_id=user2.user_id,
        audiobook_id=audiobook2.audiobook_id,
        started_at=datetime.utcnow(),
    )
    history3 = ListeningHistory(
        user_id=user3.user_id,
        audiobook_id=audiobook3.audiobook_id,
        started_at=datetime.utcnow(),
    )

    session.add(history1)
    session.add(history2)
    session.add(history3)
    session.flush()  # Ensure IDs are populated

    # Adding sample bookmarks
    bookmark1 = Bookmark(
        user_id=user1.user_id,
        audiobook_id=audiobook1.audiobook_id,
        chapter_id=chapter1.chapter_id,
        position=150,
        created_at=datetime.utcnow(),
    )
    bookmark2 = Bookmark(
        user_id=user2.user_id,
        audiobook_id=audiobook2.audiobook_id,
        chapter_id=chapter2.chapter_id,
        position=150,
        created_at=datetime.utcnow(),
    )
    bookmark3 = Bookmark(
        user_id=user3.user_id,
        audiobook_id=audiobook3.audiobook_id,
        chapter_id=chapter3.chapter_id,
        position=150,
        created_at=datetime.utcnow(),
    )

    session.add(bookmark1)
    session.add(bookmark2)
    session.add(bookmark3)
    session.flush()  # Ensure IDs are populated

    # Adding sample reviews
    review1 = Review(
        user_id=user1.user_id,
        audiobook_id=audiobook1.audiobook_id,
        review_text="Great audiobook!",
        created_at=datetime.utcnow(),
    )
    review2 = Review(
        user_id=user2.user_id,
        audiobook_id=audiobook2.audiobook_id,
        review_text="Amazing audiobook!",
        created_at=datetime.utcnow(),
    )
    review3 = Review(
        user_id=user3.user_id,
        audiobook_id=audiobook3.audiobook_id,
        review_text="Loved it!",
        created_at=datetime.utcnow(),
    )

    session.add(review1)
    session.add(review2)
    session.add(review3)
    session.flush()  # Ensure IDs are populated

    # Adding sample ratings
    rating1 = Rating(
        user_id=user1.user_id,
        audiobook_id=audiobook1.audiobook_id,
        rating=5,
        created_at=datetime.utcnow(),
    )
    rating2 = Rating(
        user_id=user2.user_id,
        audiobook_id=audiobook2.audiobook_id,
        rating=4,
        created_at=datetime.utcnow(),
    )
    rating3 = Rating(
        user_id=user3.user_id,
        audiobook_id=audiobook3.audiobook_id,
        rating=5,
        created_at=datetime.utcnow(),
    )

    session.add(rating1)
    session.add(rating2)
    session.add(rating3)
    session.flush()  # Ensure IDs are populated

    # Adding sample purchases
    purchase1 = Purchase(
        user_id=user1.user_id,
        audiobook_id=audiobook1.audiobook_id,
        purchase_date=datetime.utcnow(),
    )
    purchase2 = Purchase(
        user_id=user2.user_id,
        audiobook_id=audiobook2.audiobook_id,
        purchase_date=datetime.utcnow(),
    )
    purchase3 = Purchase(
        user_id=user3.user_id,
        audiobook_id=audiobook3.audiobook_id,
        purchase_date=datetime.utcnow(),
    )

    session.add(purchase1)
    session.add(purchase2)
    session.add(purchase3)

    session.commit()

print("Database populated with sample data.")
