from fastapi import FastAPI, Depends, HTTPException, Query, Request, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
from app.models import Movie, User, Review, Genre, Watchlist
from app import schemas  # Make sure this import is correct
from app.database import SessionLocal, engine, Base, get_db
from app.dependencies import get_current_user
from datetime import datetime, timedelta
from sqlalchemy import func
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.data.sample_data import init_db
from app.security.security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import models
from app.schemas.schemas import UserCreate  # Make sure this import exists
from app.database.seed import seed_data
from app.schemas.schemas import MovieBase, MovieResponse, MovieCreate, Genre  # Updated import
from app.security.utils import authenticate_user
from pathlib import Path
from app.models.models import Genre as GenreModel  # Add this import at the top
from app.database.init_db import init_db, seed_data
from app.database.database import SessionLocal

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize database and seed data
init_db()
db = SessionLocal()
seed_data(db)
db.close()

app = FastAPI(title="Movie Rating System")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Frontend route
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/movies")
async def movies_page(request: Request):
    return RedirectResponse(url="/", status_code=303)

# API routes
@app.get("/api")
async def read_root():
    return {
        "message": "Welcome to the Movie Rating System API!",
        "documentation": "/docs",
        "endpoints": {
            "movies": "/movies/",
            "users": "/users/",
            "reviews": "/reviews/"
        }
    }

@app.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    db_genre = Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/movies/", response_model=schemas.MovieResponse)
async def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(
        title=movie.title,
        director=movie.director,
        year=movie.year,
        synopsis=movie.synopsis
    )
    
    # Add genres
    genres = db.query(Genre).filter(Genre.id.in_(movie.genre_ids)).all()
    db_movie.genres = genres
    
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.post("/reviews/", response_model=schemas.ReviewResponse)
async def create_review(
    review: schemas.ReviewCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_review = Review(
        **review.dict(),
        user_id=user_id
    )
    db.add(db_review)
    
    # Update movie rating average
    movie = db.query(Movie).filter(Movie.id == review.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie.review_count += 1
    avg_rating = db.query(func.avg(Review.rating))\
        .filter(Review.movie_id == review.movie_id)\
        .scalar()
    movie.rating_average = float(avg_rating)
    
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/movies/", response_model=List[schemas.MovieResponse])
async def get_movies(
    search: str = "", 
    genre: str = "All Genres", 
    db: Session = Depends(get_db)
):
    query = db.query(models.Movie)
    
    if search:
        query = query.filter(models.Movie.title.ilike(f"%{search}%"))
    if genre and genre != "All Genres":
        query = query.join(models.Movie.genres).filter(models.Genre.name == genre)
    
    movies = query.all()
    
    return [
        schemas.MovieResponse(
            id=movie.id,
            title=movie.title,
            director=movie.director,
            year=movie.year,
            genres=[genre.name for genre in movie.genres]
        )
        for movie in movies
    ]

@app.post("/reviews/{review_id}/like")
def like_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    db_review.likes += 1
    db.commit()
    db.refresh(db_review)
    return {"message": "Review liked successfully"}

@app.get("/movies/top/", response_model=List[schemas.Movie])
def get_top_movies(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    query = db.query(Movie)
    query = query.order_by(Movie.rating_average.desc(), Movie.review_count.desc())
    return query.limit(limit).all()

@app.get("/movies/recommended/", response_model=List[schemas.Movie])
def get_recommended_movies(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Get user's favorite genres based on their reviews
    user_reviews = db.query(Review).filter(Review.user_id == user_id).all()
    user_rated_movies = [review.movie_id for review in user_reviews]
    
    # Find similar movies in those genres but not yet rated by the user
    recommended = db.query(Movie)\
        .filter(Movie.id.notin_(user_rated_movies))\
        .order_by(Movie.rating_average.desc())\
        .limit(limit)\
        .all()
    
    return recommended

@app.get("/debug/db")
def view_database(db: Session = Depends(get_db)):
    return {
        "users": db.query(User).all(),
        "movies": db.query(Movie).all(),
        "reviews": db.query(Review).all()
    }

@app.get("/movies/search/", response_model=List[schemas.Movie])
def search_movies(
    query: str,
    db: Session = Depends(get_db)
):
    search = f"%{query}%"
    return db.query(Movie)\
        .filter(
            (Movie.title.ilike(search)) |
            (Movie.director.ilike(search)) |
            (Movie.synopsis.ilike(search))
        ).all()

@app.post("/init-sample-data/")
def initialize_sample_data(db: Session = Depends(get_db)):
    return init_db(db)

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Debug print
    print(f"Attempting to register user with email: {user.email}")
    
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"Successfully registered user: {user.email}")
        return {"email": user.email}
    except Exception as e:
        print(f"Error registering user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/my-profile", response_model=schemas.UserProfile)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "reviews_count": len(current_user.reviews),
        "watchlist_count": len(current_user.watchlist)
    }

@app.get("/my-reviews", response_model=List[schemas.ReviewWithMovie])
def get_user_reviews(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reviews = db.query(models.Review).filter(
        models.Review.user_id == current_user.id
    ).all()
    return reviews

@app.get("/my-watched", response_model=List[schemas.Movie])
def get_watched_movies(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get movies that the user has reviewed
    watched_movies = db.query(models.Movie).join(
        models.Review
    ).filter(
        models.Review.user_id == current_user.id
    ).distinct().all()
    return watched_movies

@app.get("/my-watchlist", response_model=List[schemas.Movie])
async def get_user_watchlist(current_user: User = Depends(get_current_user)):
    return [item.movie for item in current_user.watchlist]

@app.post("/watchlist/{movie_id}")
async def add_to_watchlist(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    watchlist_item = Watchlist(user_id=current_user.id, movie_id=movie_id)
    db.add(watchlist_item)
    db.commit()
    return {"message": "Added to watchlist"}

@app.get("/genres/", response_model=List[Genre])
def get_genres(db: Session = Depends(get_db)):
    genres = db.query(models.Genre).all()
    return [{"id": genre.id, "name": genre.name} for genre in genres]

@app.on_event("startup")
async def startup_event():
    # Create a new database session
    db = next(get_db())
    # Initialize the database with seed data
    seed_data(db)
    # Close the session
    db.close()

# Add this new endpoint to serve the your_movies page
@app.get("/your-movies")
async def your_movies_page(request: Request):
    return templates.TemplateResponse("your_movies.html", {"request": request})

# Add this API endpoint to get user reviews
@app.get("/api/user/reviews", response_model=List[schemas.ReviewWithMovie])
async def get_user_reviews(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reviews = db.query(models.Review).filter(
        models.Review.user_id == current_user.id
    ).all()
    return reviews

@app.get("/movie/{movie_id}")
async def movie_details_page(request: Request, movie_id: int):
    return templates.TemplateResponse("movie_details.html", {"request": request})

@app.get("/api/movies/{movie_id}", response_model=schemas.MovieResponse)
def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return {
        "id": movie.id,
        "title": movie.title,
        "director": movie.director,
        "year": movie.year,
        "genres": [genre.name for genre in movie.genres]  # Convert Genre objects to strings
    }

@app.get("/api/movies/{movie_id}/reviews", response_model=List[schemas.ReviewResponse])
def get_movie_reviews(movie_id: int, db: Session = Depends(get_db)):
    reviews = (
        db.query(models.Review)
        .join(models.User)  # Join with User table
        .filter(models.Review.movie_id == movie_id)
        .all()
    )
    
    return [
        {
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "user_id": review.user_id,
            "movie_id": review.movie_id,
            "user_username": review.user.username
        }
        for review in reviews
    ]

@app.post("/api/movies/{movie_id}/reviews", response_model=schemas.ReviewResponse)
def create_review(
    movie_id: int,
    review: schemas.ReviewCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_review = models.Review(
        rating=review.rating,
        comment=review.comment,
        movie_id=movie_id,
        user_id=current_user.id
    )
    
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # Create response with username
    return {
        "id": db_review.id,
        "rating": db_review.rating,
        "comment": db_review.comment,
        "created_at": db_review.created_at,
        "user_id": db_review.user_id,
        "movie_id": db_review.movie_id,
        "user_username": current_user.username  # Add the username
    }

@app.get("/your-movies/list", response_model=List[schemas.MovieResponse])
async def get_your_movies(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_reviews = db.query(models.Review).filter(models.Review.user_id == current_user.id).all()
    movies = []
    for review in user_reviews:
        movie = review.movie
        movie_response = schemas.MovieResponse(
            id=movie.id,
            title=movie.title,
            director=movie.director,
            year=movie.year,
            genres=[genre.name for genre in movie.genres],
            your_rating=review.rating
        )
        movies.append(movie_response)
    return movies

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request}) 