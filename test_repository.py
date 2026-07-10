from app.database import Base, SessionLocal, engine
from app.models.memes import Memes
from app.models.tags import Tag
from app.models.users import User
from app.repositories.memes_repository import MemesRepository
from app.repositories.tags_repository import TagRepository
from app.repositories.user_repository import UserRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

tag_repo = TagRepository(db)
user_repo = UserRepository(db)
meme_repo = MemesRepository(db)


tag = Tag(name="Funny")
created_tag = tag_repo.create(tag)


user = User(email="test@example.com", hashed_password="hashed_password")
created_user = user_repo.create(user)


mem = Memes(
    name="Test Meme",
    description="Test description",
    photo="test.jpg",
    tag_id=created_tag.id,
)
created_meme = meme_repo.create(mem)


created_user.memes.append(created_meme)
db.commit()


print("Мемы:")
for meme in meme_repo.get_all():
    print(f"  ID: {meme.id}, Name: {meme.name}, Tag: {meme.tag_id}")

print("\nПользователи:")
for user in user_repo.get_all():
    print(f"  ID: {user.id}, Email: {user.email}")

print("\nСвязи пользователь-мем:")
for user in user_repo.get_all():
    for meme in user.memes:
        print(f"  User {user.id} -> Meme {meme.id}")

db.close()