# Full Stack Todo Application

A modern todo application built with FastAPI and Next.js.

## Project Structure

```
.
├── backend/           # FastAPI backend
└── frontend/         # Next.js frontend
```

## Backend Setup

1. Create and activate a virtual environment:
```bash
cd backend
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

The API will be available at http://localhost:8000

## Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Features

- User authentication
- Create, read, update, and delete todos
- Modern, responsive UI
- Real-time updates

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- JWT Authentication
- Uvicorn

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Next.js App Router

## Development

The application is set up with hot-reloading for both frontend and backend, making development smooth and efficient.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
