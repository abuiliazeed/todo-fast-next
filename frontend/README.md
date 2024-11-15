# Todo Application Frontend

Next.js frontend for the Todo application with TypeScript and Tailwind CSS.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Features

- User registration and login
- Create and manage todos
- Mark todos as complete/incomplete
- Responsive design
- Authentication state persistence

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # Root layout with AuthProvider
│   │   ├── page.tsx        # Home page with auth redirects
│   │   ├── login/
│   │   │   └── page.tsx    # Login/Register page
│   │   └── todos/
│   │       └── page.tsx    # Todo management page
│   ├── contexts/
│   │   └── AuthContext.tsx # Authentication context
│   └── lib/
│       └── api.ts          # API client functions
├── package.json
└── README.md               # This file
```

## Development

### Technologies Used

- Next.js 14
- TypeScript
- Tailwind CSS
- React Context API
- Fetch API for backend communication

### Adding New Features

1. Create new components in appropriate directories
2. Add new API functions in `src/lib/api.ts`
3. Update types as needed
4. Add new pages in the `src/app` directory

### State Management

The application uses React Context for:
- Authentication state
- User information
- API credentials

### Styling

- Tailwind CSS for utility-first styling
- Responsive design patterns
- Custom components with consistent styling

### Authentication Flow

1. User registers or logs in
2. Credentials are stored securely
3. AuthContext provides authentication state
4. Protected routes redirect to login
5. API calls include authentication headers

## Production

Before deploying to production:

1. Update the API base URL in `src/lib/api.ts`
2. Configure environment variables
3. Build the application:
```bash
npm run build
```

4. Test the production build:
```bash
npm run start
```
