# Empty file to make the schemas directory a Python package 

from .schemas import (
    MovieBase,
    MovieCreate,
    Movie,
    MovieResponse,
    MovieWithReviews,
    ReviewBase,
    ReviewCreate,
    Review,
    ReviewResponse,
    ReviewWithMovie,
    UserBase,
    UserCreate,
    User,
    UserResponse,
    UserProfile,
    UserInDB,
    WatchlistBase,
    WatchlistCreate,
    WatchlistWithMovie,
    WatchlistResponse,
    Genre,
    GenreBase,
    GenreCreate,
    UserWithStats
)

__all__ = [
    "MovieBase",
    "MovieCreate",
    "Movie",
    "MovieResponse",
    "MovieWithReviews",
    "ReviewBase",
    "ReviewCreate",
    "Review",
    "ReviewResponse",
    "ReviewWithMovie",
    "UserBase",
    "UserCreate",
    "User",
    "UserResponse",
    "UserProfile",
    "UserInDB",
    "WatchlistBase",
    "WatchlistCreate",
    "WatchlistWithMovie",
    "WatchlistResponse",
    "Genre",
    "GenreBase",
    "GenreCreate",
    "UserWithStats"
] 