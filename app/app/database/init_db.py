from sqlalchemy.orm import Session
from app.models import models
from app.database.database import engine, Base

def init_db():
    Base.metadata.create_all(bind=engine)
    
def seed_data(db: Session):
    # Check if we already have movies
    if db.query(models.Movie).first():
        return
    
    # Create genres
    action = models.Genre(name="Action")
    comedy = models.Genre(name="Comedy")
    drama = models.Genre(name="Drama")
    scifi = models.Genre(name="Sci-Fi")
    
    db.add_all([action, comedy, drama, scifi])
    db.commit()
    
    # Create some sample movies
    movies = [
        models.Movie(
            title="Inception",
            director="Christopher Nolan",
            year=2010,
            genres=[action, scifi]
        ),
        models.Movie(
            title="The Dark Knight",
            director="Christopher Nolan",
            year=2008,
            genres=[action, drama]
        ),
        models.Movie(
            title="Pulp Fiction",
            director="Quentin Tarantino",
            year=1994,
            genres=[drama, action]
        ),
        models.Movie(
            title="The Grand Budapest Hotel",
            director="Wes Anderson",
            year=2014,
            genres=[comedy, drama]
        )
    ]
    
    db.add_all(movies)
    db.commit() 