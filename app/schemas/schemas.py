from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum
from pydantic import field_validator

class GenreEnum(str, Enum):
    ACTION = "action"
    DRAMA = "drama"
    CRIME = "crime"
    SCIFI = "sci-fi"
    THRILLER = "thriller"
    HORROR = "horror"
    ROMANCE = "romance"
    ADVENTURE = "adventure"
    FANTASY = "fantasy"
    ANIMATION = "animation"
    WAR = "war"
    MYSTERY = "mystery"

# Movie schemas first
class MovieBase(BaseModel):
    title: str
    director: str
    year: int
    genres: List[str]

class MovieCreate(MovieBase):
    pass

class MovieSchema(MovieBase):
    id: int
    genres: List[str]

    class Config:
        from_attributes = True

class Movie(MovieBase):
    id: int

    class Config:
        from_attributes = True

class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    year: int
    genres: List[str]

    class Config:
        from_attributes = True

# Review schemas after Movie schemas
class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(BaseModel):
    rating: int
    comment: str

class Review(ReviewBase):
    id: int
    created_at: datetime
    user_id: int
    movie_id: int

    class Config:
        from_attributes = True

class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str
    created_at: datetime
    user_id: int
    movie_id: int
    user_username: str

    class Config:
        from_attributes = True

class ReviewWithMovie(ReviewResponse):
    movie: MovieResponse

    class Config:
        from_attributes = True

# Movie schema that includes reviews
class MovieWithReviews(MovieResponse):
    reviews: List[ReviewResponse] = []
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True

# User schemas last
class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class UserProfile(UserBase):
    id: int
    reviews: List[ReviewResponse] = []
    watchlist: List[MovieResponse] = []

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

    class Config:
        from_attributes = True

# Watchlist schemas
class WatchlistBase(BaseModel):
    user_id: int
    movie_id: int

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistWithMovie(BaseModel):
    id: int
    user_id: int
    movie_id: int
    movie: MovieResponse

    class Config:
        from_attributes = True

class WatchlistResponse(WatchlistBase):
    id: int

    class Config:
        from_attributes = True

# Genre schemas
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    reviews_count: Optional[int] = 0
    watchlist_count: Optional[int] = 0

    class Config:
        from_attributes = True

class UserWithStats(BaseModel):
    id: int
    email: str
    created_at: datetime
    review_count: int

    class Config:
        from_attributes = True 