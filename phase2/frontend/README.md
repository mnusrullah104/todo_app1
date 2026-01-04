# Todo Frontend - Next.js

Phase II Todo Web Application frontend.

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT
- **Testing**: Vitest (unit/component), Playwright (E2E)

## Setup

### Prerequisites

- Node.js 20.x or later
- Backend API running (see [backend README](../backend/README.md))

### Installation

```bash
# Install dependencies
npm install
```

### Configuration

```bash
# Copy environment template
cp .env.local.example .env.local

# Edit .env.local and configure:
# - NEXT_PUBLIC_BASE_URL: Your frontend URL (default: http://localhost:3000)
# - NEXT_PUBLIC_API_BASE_URL: Your backend API URL (default: http://localhost:8000)
# - BETTER_AUTH_SECRET: MUST match backend secret exactly
```

**CRITICAL**: `BETTER_AUTH_SECRET` must be identical in both frontend and backend `.env` files.

### Running

```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx      # Root layout with auth provider
│   ├── page.tsx        # Landing page
│   ├── login/          # Login page
│   ├── register/       # Registration page
│   └── dashboard/      # Main task dashboard
├── components/         # React components
│   ├── ui/            # Reusable UI components
│   ├── TaskList.tsx   # Task list display
│   ├── TaskForm.tsx   # Task creation/edit form
│   ├── TaskItem.tsx   # Individual task display
│   └── AuthForm.tsx   # Login/register form
├── lib/               # Utility functions
│   ├── api-client.ts # API client with JWT
│   ├── auth.ts       # Better Auth configuration
│   └── types.ts      # TypeScript type definitions
├── public/           # Static assets
└── tests/            # Test suite
```

## Testing

```bash
# Run unit/component tests (Vitest)
npm test

# Run E2E tests (Playwright)
npm run test:e2e

# Run tests in watch mode
npm run test:watch
```

## Development

```bash
# Lint code
npm run lint

# Format code
npm run format
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_BASE_URL` | Yes | Frontend base URL |
| `NEXT_PUBLIC_API_BASE_URL` | Yes | Backend API URL |
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret (MUST match backend) |

## Features

- **User Authentication**: Register and login with JWT tokens
- **Task Management**: Create, view, update, complete, and delete tasks
- **Responsive Design**: Works on desktop and mobile browsers
- **Real-time Updates**: Optimistic UI updates for smooth UX
- **Data Isolation**: Users only see their own tasks

## See Also

- [Project Root README](../README.md)
- [Backend README](../backend/README.md)
- [Quickstart Guide](../specs/002-fullstack-todo-web/quickstart.md)
- [UI Specifications](../specs/002-fullstack-todo-web/contracts/api-endpoints.md)
