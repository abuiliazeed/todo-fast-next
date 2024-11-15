# Todo Application

A full-stack todo application with FastAPI backend and Next.js frontend.

## Project Structure

```
todo-application/
├── backend/           # FastAPI backend
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
│
└── frontend/          # Next.js frontend
    ├── src/
    ├── package.json
    └── README.md
```

## Backend (FastAPI)

### Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Frontend (Next.js)

### Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Features

- User authentication with Basic Auth
- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- Modern, responsive UI
- API documentation with OpenAPI/Swagger

## Development

### Backend Development

- API documentation available at `http://localhost:8000/docs`
- SQLite database for development
- Basic Auth for authentication
- CORS enabled for frontend communication

### Frontend Development

- Built with Next.js 14 and TypeScript
- Tailwind CSS for styling
- Context API for state management
- Responsive design

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
