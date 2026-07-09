from app.database import Base, SessionLocal, engine
from app.models.memes import Memes
from app.models.tags import Tag
from app.models.profile import Profile
from app.models.favourites import Favourite
from app.repositories.memes_repository import MemesRepository
from app.repositories.tags_repository import TagRepository
from app.repositories.profile_repository import ProfileRepository
from app.repositories.favourites_repository import FavouriteRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

tag_repo = TagRepository(db)
profile_repo = ProfileRepository(db)
meme_repo = MemesRepository(db)
fav_repo = FavouriteRepository(db)


tag = Tag(name="Funny")
created_tag = tag_repo.create(tag)



mem = Memes(
    name="Test Meme",
    description="Test description",
    photo="test.jpg",
    tag_id=created_tag.id,
)
created_meme = meme_repo.create(mem)





memes = meme_repo.get_all()

for meme in memes:
    print(meme.id, meme.name, meme.description, meme.photo, meme.tag_id)


tags = tag_repo.get_all()
for tag in tags:
    print(tag.id, tag.name)





profiles = profile_repo.get_all()
for profile in profiles:
    print(profile.id, profile.user_id, profile.name)


favourites = fav_repo.get_all()
for fav in favourites:
    print(fav.id, fav.meme_id, fav.user_id)

db.close()