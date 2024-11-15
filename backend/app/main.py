from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import secrets
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import hashlib

# FastAPI app setup
app = FastAPI(
    title="TODO List API",
    description="""
    A modern TODO List API with user authentication and CRUD operations.
    
    ## Features
    * User registration and authentication using Basic Auth
    * Create, read, update, and delete TODO items
    * Each user can only access their own TODOs
    * Secure password hashing
    
    ## Authentication
    This API uses HTTP Basic Authentication. Include your username and password with each request.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@todoapi.com",
    },
    license_info={
        "name": "MIT",
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model for database
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
    owner = Column(String, index=True, nullable=False)  # Make owner required and indexed

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title: str
    completed: bool = False

class Todo(BaseModel):
    id: int
    title: str
    completed: bool
    owner: str
    class Config:
        from_attributes = True

# Create tables
Base.metadata.drop_all(bind=engine)  # Drop all tables first
Base.metadata.create_all(bind=engine)

# Helper functions
def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)], db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.username

# User management endpoints
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="""
    Create a new user with the following information:
    
    - **username**: Unique username for the account
    - **password**: Strong password for authentication
    
    The password will be hashed before storage.
    """,
    response_description="The created user object",
    responses={
        400: {"description": "Username already exists"},
    }
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me/", response_model=User,
    summary="Get current user information",
    description="Retrieve the information of the currently authenticated user.",
    response_description="The current user's information"
)
def read_users_me(current_user: Annotated[str, Depends(get_current_user)]):
    return {"username": current_user}

@app.get("/",
    summary="API Welcome Page",
    description="Returns welcome message and a comprehensive list of all available endpoints.",
    response_description="Welcome message and detailed endpoints overview"
)
async def index():
    return {
        "message": "Welcome to TODO API",
        "available_endpoints": {
            "documentation": {
                "swagger_ui": "/docs",
                "redoc": "/redoc",
                "openapi_schema": "/openapi.json"
            },
            "user_management": {
                "create_user": {
                    "path": "/users/",
                    "method": "POST",
                    "description": "Create a new user account"
                },
                "get_current_user": {
                    "path": "/users/me/",
                    "method": "GET",
                    "description": "Get current user information"
                }
            },
            "todo_operations": {
                "list_todos": {
                    "path": "/todos",
                    "method": "GET",
                    "description": "List all TODOs for authenticated user"
                },
                "create_todo": {
                    "path": "/todos",
                    "method": "POST",
                    "description": "Create a new TODO item"
                },
                "get_todo": {
                    "path": "/todos/{todo_id}",
                    "method": "GET",
                    "description": "Get a specific TODO by ID"
                },
                "update_todo": {
                    "path": "/todos/{todo_id}",
                    "method": "PUT",
                    "description": "Update a specific TODO by ID"
                },
                "delete_todo": {
                    "path": "/todos/{todo_id}",
                    "method": "DELETE",
                    "description": "Delete a specific TODO by ID"
                }
            }
        },
        "authentication": "This API uses HTTP Basic Authentication. Include your username and password with each request.",
        "version": "1.0.0"
    }

@app.get("/todos", response_model=list[Todo],
    summary="List all TODOs",
    description="""
    Retrieve all TODOs for the authenticated user.
    
    The response will be a list of TODO items, each containing:
    - **id**: Unique identifier
    - **title**: The TODO item's title
    - **completed**: Whether the TODO is completed
    - **owner**: Username of the TODO item's owner
    """,
    response_description="List of TODO items"
)
async def read_todos(
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    todos = db.query(TodoDB).filter(TodoDB.owner == current_user).all()
    return todos

@app.get("/todos/{todo_id}", response_model=Todo,
    summary="Get a specific TODO",
    description="""
    Retrieve a specific TODO item by its ID.
    
    Parameters:
    - **todo_id**: The unique identifier of the TODO item
    """,
    response_description="The requested TODO item",
    responses={
        404: {"description": "TODO item not found"},
    }
)
async def read_todo(
    todo_id: int,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).filter(TodoDB.owner == current_user).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED,
    summary="Create a new TODO",
    description="""
    Create a new TODO item with the following information:
    
    - **title**: The title of the TODO item
    - **completed**: Whether the TODO is completed (defaults to false)
    
    The TODO will be automatically associated with the authenticated user.
    """,
    response_description="The created TODO item"
)
async def create_todo(
    todo: TodoCreate,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    db_todo = TodoDB(**todo.dict(), owner=current_user)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}", response_model=Todo,
    summary="Update a TODO",
    description="""
    Update an existing TODO item by its ID.
    
    Parameters:
    - **todo_id**: The unique identifier of the TODO item
    - **title**: New title for the TODO item
    - **completed**: New completion status
    
    Only the owner can update their TODOs.
    """,
    response_description="The updated TODO item",
    responses={
        404: {"description": "TODO item not found"},
    }
)
async def update_todo(
    todo_id: int,
    todo: TodoCreate,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).filter(TodoDB.owner == current_user).first()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a TODO",
    description="""
    Delete a specific TODO item by its ID.
    
    Parameters:
    - **todo_id**: The unique identifier of the TODO item to delete
    
    Only the owner can delete their TODOs.
    """,
    response_description="No content, successful deletion",
    responses={
        404: {"description": "TODO item not found"},
    }
)
async def delete_todo(
    todo_id: int,
    current_user: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    db_todo = db.query(TodoDB).filter(TodoDB.id == todo_id).filter(TodoDB.owner == current_user).first()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return None
