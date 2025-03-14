from sqlalchemy.orm import Session
from app.models import Movie, Genre
from app.database import engine, Base

def seed_data(db: Session):
    print("Starting database seeding...")
    Base.metadata.create_all(bind=engine)
    
    # Check if we already have movies
    if db.query(Movie).count() == 0:
        print("No movies found, seeding database...")
        
        # Add genres
        genres = {
            "action": Genre(name="action"),
            "drama": Genre(name="drama"),
            "comedy": Genre(name="comedy"),
            "sci-fi": Genre(name="sci-fi"),
            "thriller": Genre(name="thriller"),
            "horror": Genre(name="horror"),
            "romance": Genre(name="romance"),
            "adventure": Genre(name="adventure"),
            "crime": Genre(name="crime"),
            "fantasy": Genre(name="fantasy")
        }
        
        for genre in genres.values():
            db.add(genre)
        
        # Add sample movies
        movies = [
            Movie(
                title="The Shawshank Redemption",
                director="Frank Darabont",
                year=1994,
                synopsis="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                rating_average=4.7,
                review_count=0,
                genres=[genres["drama"]]
            ),
            Movie(
                title="Inception",
                director="Christopher Nolan",
                year=2010,
                synopsis="A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                rating_average=4.5,
                review_count=0,
                genres=[genres["action"], genres["sci-fi"]]
            ),
            Movie(
                title="The Dark Knight",
                director="Christopher Nolan",
                year=2008,
                synopsis="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                rating_average=4.6,
                review_count=0,
                genres=[genres["action"], genres["crime"], genres["drama"]]
            ),
            Movie(
                title="Pulp Fiction",
                director="Quentin Tarantino",
                year=1994,
                synopsis="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                rating_average=4.5,
                review_count=0,
                genres=[genres["crime"], genres["drama"]]
            ),
            Movie(
                title="The Matrix",
                director="Lana and Lilly Wachowski",
                year=1999,
                synopsis="A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to break free.",
                rating_average=4.4,
                review_count=0,
                genres=[genres["action"], genres["sci-fi"]]
            ),
            Movie(
                title="Forrest Gump",
                director="Robert Zemeckis",
                year=1994,
                synopsis="The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
                rating_average=4.5,
                review_count=0,
                genres=[genres["drama"], genres["romance"]]
            ),
            Movie(
                title="The Silence of the Lambs",
                director="Jonathan Demme",
                year=1991,
                synopsis="A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.",
                rating_average=4.3,
                review_count=0,
                genres=[genres["crime"], genres["thriller"]]
            ),
            Movie(
                title="Jurassic Park",
                director="Steven Spielberg",
                year=1993,
                synopsis="A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park's cloned dinosaurs to run loose.",
                rating_average=4.2,
                review_count=0,
                genres=[genres["adventure"], genres["sci-fi"]]
            ),
            Movie(
                title="The Lord of the Rings: The Fellowship of the Ring",
                director="Peter Jackson",
                year=2001,
                synopsis="A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
                rating_average=4.6,
                review_count=0,
                genres=[genres["adventure"], genres["fantasy"]]
            ),
            Movie(
                title="Goodfellas",
                director="Martin Scorsese",
                year=1990,
                synopsis="The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.",
                rating_average=4.4,
                review_count=0,
                genres=[genres["crime"], genres["drama"]]
            ),
            Movie(
                title="The Godfather",
                director="Francis Ford Coppola",
                year=1972,
                synopsis="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                rating_average=4.8,
                review_count=0,
                genres=[genres["crime"], genres["drama"]]
            ),
            Movie(
                title="Fight Club",
                director="David Fincher",
                year=1999,
                synopsis="An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.",
                rating_average=4.4,
                review_count=0,
                genres=[genres["drama"], genres["thriller"]]
            ),
            Movie(
                title="The Sixth Sense",
                director="M. Night Shyamalan",
                year=1999,
                synopsis="A boy who communicates with spirits seeks the help of a disheartened child psychologist.",
                rating_average=4.1,
                review_count=0,
                genres=[genres["drama"], genres["thriller"]]
            ),
            Movie(
                title="Titanic",
                director="James Cameron",
                year=1997,
                synopsis="A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
                rating_average=4.3,
                review_count=0,
                genres=[genres["drama"], genres["romance"]]
            ),
            Movie(
                title="The Green Mile",
                director="Frank Darabont",
                year=1999,
                synopsis="The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift.",
                rating_average=4.5,
                review_count=0,
                genres=[genres["crime"], genres["drama"], genres["fantasy"]]
            ),
            Movie(
                title="Saving Private Ryan",
                director="Steven Spielberg",
                year=1998,
                synopsis="Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
                rating_average=4.6,
                review_count=0,
                genres=[genres["drama"], genres["action"]]
            ),
            Movie(
                title="The Terminator",
                director="James Cameron",
                year=1984,
                synopsis="A human soldier is sent from 2029 to 1984 to stop an almost indestructible cyborg killing machine, sent from the same year, which has been programmed to execute a young woman.",
                rating_average=4.2,
                review_count=0,
                genres=[genres["action"], genres["sci-fi"]]
            ),
            Movie(
                title="Gladiator",
                director="Ridley Scott",
                year=2000,
                synopsis="A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
                rating_average=4.4,
                review_count=0,
                genres=[genres["action"], genres["drama"]]
            ),
            Movie(
                title="The Departed",
                director="Martin Scorsese",
                year=2006,
                synopsis="An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.",
                rating_average=4.3,
                review_count=0,
                genres=[genres["crime"], genres["drama"], genres["thriller"]]
            ),
            Movie(
                title="Interstellar",
                director="Christopher Nolan",
                year=2014,
                synopsis="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                rating_average=4.4,
                review_count=0,
                genres=[genres["adventure"], genres["drama"], genres["sci-fi"]]
            )
        ]
        
        for movie in movies:
            db.add(movie)
        
        db.commit()
        print("Database seeded successfully!")
