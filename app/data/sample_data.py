from app.models.models import Movie, Genre
from sqlalchemy.orm import Session

SAMPLE_MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "year": 1994,
        "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "genres": ["drama"]
    },
    {
        "title": "The Godfather",
        "director": "Francis Ford Coppola",
        "year": 1972,
        "synopsis": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "genres": ["drama", "crime"]
    },
    {
        "title": "The Dark Knight",
        "director": "Christopher Nolan",
        "year": 2008,
        "synopsis": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "genres": ["action", "crime", "drama"]
    },
    {
        "title": "Pulp Fiction",
        "director": "Quentin Tarantino",
        "year": 1994,
        "synopsis": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "genres": ["crime", "drama"]
    },
    {
        "title": "Inception",
        "director": "Christopher Nolan",
        "year": 2010,
        "synopsis": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "genres": ["action", "sci-fi", "thriller"]
    },
    {
        "title": "The Matrix",
        "director": "Lana and Lilly Wachowski",
        "year": 1999,
        "synopsis": "A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to break free.",
        "genres": ["action", "sci-fi"]
    },
    {
        "title": "Forrest Gump",
        "director": "Robert Zemeckis",
        "year": 1994,
        "synopsis": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
        "genres": ["drama", "romance"]
    },
    {
        "title": "The Silence of the Lambs",
        "director": "Jonathan Demme",
        "year": 1991,
        "synopsis": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.",
        "genres": ["crime", "thriller", "horror"]
    },
    {
        "title": "Jurassic Park",
        "director": "Steven Spielberg",
        "year": 1993,
        "synopsis": "A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park's cloned dinosaurs to run loose.",
        "genres": ["action", "adventure", "sci-fi"]
    },
    {
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "director": "Peter Jackson",
        "year": 2001,
        "synopsis": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
        "genres": ["action", "adventure", "fantasy"]
    },
    {
        "title": "Goodfellas",
        "director": "Martin Scorsese",
        "year": 1990,
        "synopsis": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.",
        "genres": ["crime", "drama"]
    },
    {
        "title": "The Green Mile",
        "director": "Frank Darabont",
        "year": 1999,
        "synopsis": "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift.",
        "genres": ["crime", "drama", "fantasy"]
    },
    {
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "year": 2014,
        "synopsis": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "genres": ["adventure", "drama", "sci-fi"]
    },
    {
        "title": "The Departed",
        "director": "Martin Scorsese",
        "year": 2006,
        "synopsis": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.",
        "genres": ["crime", "drama", "thriller"]
    },
    {
        "title": "Gladiator",
        "director": "Ridley Scott",
        "year": 2000,
        "synopsis": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "genres": ["action", "adventure", "drama"]
    },
    {
        "title": "The Sixth Sense",
        "director": "M. Night Shyamalan",
        "year": 1999,
        "synopsis": "A boy who communicates with spirits seeks the help of a disheartened child psychologist.",
        "genres": ["drama", "mystery", "thriller"]
    },
    {
        "title": "Saving Private Ryan",
        "director": "Steven Spielberg",
        "year": 1998,
        "synopsis": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
        "genres": ["drama", "war"]
    },
    {
        "title": "Titanic",
        "director": "James Cameron",
        "year": 1997,
        "synopsis": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "genres": ["drama", "romance"]
    },
    {
        "title": "The Avengers",
        "director": "Joss Whedon",
        "year": 2012,
        "synopsis": "Earth's mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.",
        "genres": ["action", "adventure", "sci-fi"]
    },
    {
        "title": "The Lion King",
        "director": "Roger Allers, Rob Minkoff",
        "year": 1994,
        "synopsis": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
        "genres": ["animation", "adventure", "drama"]
    }
]

def init_db(db: Session):
    # Create genres
    genres = {}
    for movie in SAMPLE_MOVIES:
        for genre_name in movie["genres"]:
            if genre_name not in genres:
                genre = Genre(name=genre_name)
                db.add(genre)
                genres[genre_name] = genre
    db.commit()

    # Create movies
    for movie_data in SAMPLE_MOVIES:
        movie_genres = [genres[genre_name] for genre_name in movie_data["genres"]]
        movie = Movie(
            title=movie_data["title"],
            director=movie_data["director"],
            year=movie_data["year"],
            synopsis=movie_data["synopsis"],
            genres=movie_genres
        )
        db.add(movie)
    
    db.commit()
    return {"message": f"Initialized {len(SAMPLE_MOVIES)} movies and {len(genres)} genres"} 