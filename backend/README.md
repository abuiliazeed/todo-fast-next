# Todo Application Backend

FastAPI backend for the Todo application with user authentication and CRUD operations.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /users/`: Create a new user
- `GET /users/me/`: Get current user information

### Todos
- `GET /todos`: List all todos for the current user
- `POST /todos`: Create a new todo
- `GET /todos/{todo_id}`: Get a specific todo
- `PUT /todos/{todo_id}`: Update a todo
- `DELETE /todos/{todo_id}`: Delete a todo

## Database

The application uses SQLite for data storage. The database file (`todos.db`) will be created automatically when you first run the application.

## Authentication

The API uses HTTP Basic Authentication. Include your username and password with each request to protected endpoints.

## Development

### Project Structure
```
backend/
├── app/
│   └── main.py          # Main application file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Features

1. Add new models in `main.py`
2. Create new endpoints in `main.py`
3. Update the OpenAPI documentation
4. Test the new endpoints using the Swagger UI

### Security Considerations

- Passwords are hashed before storage
- Each user can only access their own todos
- CORS is enabled for the frontend application
- Basic Auth is used for simplicity (consider using JWT for production)
