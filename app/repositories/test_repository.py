from app.database import Base, SessionLocal, engine
from app.models.memes import Memes
from app.repositories.memes_repository import MemesRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

repository = MemesRepository(db)

mem = Memes(
    name = "Memes",
    description = "Memes description",
    photo = "Memes image",

)

repository.create(mem)

mems = repository.get_all()

for mem in mems:
    print(mem.id, mem.name, mem.description, mem.photo)

db.close()