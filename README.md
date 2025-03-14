# MovieRater

A web application for rating and reviewing movies built with FastAPI.

## Features
- User authentication
- Movie browsing and searching
- Rating and reviewing movies
- Genre filtering
- Personal movie lists

## Setup
1. Create virtual environment:
```python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```python
pip install -r requirements.txt
```

3. Run the application:
```python
uvicorn app.main:app --reload
```

4. Visit http://localhost:8000 