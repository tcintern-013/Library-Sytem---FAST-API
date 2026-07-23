# Library System using FastAPI

A simple FastAPI-based library management system with SQLite persistence and JWT-based authentication.

## Features
- Create, view, update, and delete books
- Persist books in a SQLite database
- Prevent duplicate book IDs
- Store a creation timestamp for each book
- User signup and login
- Password hashing with bcrypt
- JWT-based protected access to the /me endpoint

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- PyJWT
- passlib

## Project Structure
- main.py - FastAPI routes and auth endpoints
- models.py - SQLAlchemy models
- schemas.py - Pydantic schemas
- database.py - SQLite database configuration
- crud.py - CRUD operations
- auth.py - JWT and password hashing logic

## Installation
```bash
pip install -r requirements.txt
```

## Run the Application
```bash
uvicorn main:app --reload
```

## API Documentation
Once the server is running, open:
```bash
http://127.0.0.1:8000/docs
```

## Authentication Endpoints
### Signup
```bash
POST /signup
{
  "username": "alice",
  "password": "secret123"
}
```

### Login
```bash
POST /login
{
  "username": "alice",
  "password": "secret123"
}
```

### Protected Route
```bash
GET /me
Authorization: Bearer <access_token>
```

## Example Book Endpoints
- POST /books
- GET /books
- GET /books/{book_id}
- PUT /books/{book_id}
- DELETE /books/{book_id}

## Quick Test Flow
1. Start the server with `uvicorn main:app --reload`
2. Create a user at `/signup`
3. Sign in at `/login` to get a JWT token
4. Call `/me` with the token in the `Authorization` header
