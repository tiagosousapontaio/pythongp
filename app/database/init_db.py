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
    thriller = models.Genre(name="Thriller")
    horror = models.Genre(name="Horror")
    romance = models.Genre(name="Romance")
    
    db.add_all([action, comedy, drama, scifi, thriller, horror, romance])
    db.commit()
    
    # Create movies
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
            genres=[drama, thriller]
        ),
        models.Movie(
            title="The Grand Budapest Hotel",
            director="Wes Anderson",
            year=2014,
            genres=[comedy, drama]
        ),
        models.Movie(
            title="The Matrix",
            director="Lana and Lilly Wachowski",
            year=1999,
            genres=[action, scifi]
        ),
        models.Movie(
            title="Interstellar",
            director="Christopher Nolan",
            year=2014,
            genres=[scifi, drama]
        ),
        models.Movie(
            title="The Shawshank Redemption",
            director="Frank Darabont",
            year=1994,
            genres=[drama]
        ),
        models.Movie(
            title="Forrest Gump",
            director="Robert Zemeckis",
            year=1994,
            genres=[drama, romance]
        ),
        models.Movie(
            title="The Silence of the Lambs",
            director="Jonathan Demme",
            year=1991,
            genres=[thriller, horror]
        ),
        models.Movie(
            title="Goodfellas",
            director="Martin Scorsese",
            year=1990,
            genres=[drama, thriller]
        ),
        models.Movie(
            title="Fight Club",
            director="David Fincher",
            year=1999,
            genres=[drama, thriller]
        ),
        models.Movie(
            title="The Godfather",
            director="Francis Ford Coppola",
            year=1972,
            genres=[drama, thriller]
        ),
        models.Movie(
            title="Jurassic Park",
            director="Steven Spielberg",
            year=1993,
            genres=[action, scifi]
        ),
        models.Movie(
            title="Back to the Future",
            director="Robert Zemeckis",
            year=1985,
            genres=[scifi, comedy]
        ),
        models.Movie(
            title="The Departed",
            director="Martin Scorsese",
            year=2006,
            genres=[drama, thriller]
        ),
        models.Movie(
            title="Eternal Sunshine of the Spotless Mind",
            director="Michel Gondry",
            year=2004,
            genres=[drama, romance, scifi]
        )
    ]
    
    db.add_all(movies)
    db.commit()

if __name__ == "__main__":
    from app.database.database import SessionLocal
    db = SessionLocal()
    init_db()
    seed_data(db)
    db.close() 