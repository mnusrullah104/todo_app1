# Hackathon Todo App

A professional full-stack todo application built with modern technologies and spec-driven development practices.

## 🚀 Features

- **Secure Authentication**: Powered by Better Auth with JWT tokens
- **Task Management**: Complete CRUD operations for personal tasks
- **Data Isolation**: Users can only access their own data
- **Responsive UI**: Mobile-first design with Tailwind CSS
- **Real-time Updates**: Live task status updates
- **Type Safety**: Full TypeScript coverage on frontend
- **Clean Architecture**: Well-structured backend with services layer

## 🛠 Tech Stack

- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python), SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT-based)
- **Architecture**: Monorepo with spec-driven development

## 📁 Project Structure

```
hackathon-todo/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── ...
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── ...
│   └── ...
└── README.md
```

## 🏗 Architecture

This application follows a clean architecture pattern with:

- **Specification-driven development**: All code is generated from detailed specs
- **Separation of concerns**: Clear boundaries between frontend, backend, and auth layers
- **Security-first**: JWT-based authentication with proper token validation
- **Scalable design**: Ready for horizontal scaling and microservices

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (for frontend and auth server)
- Python 3.11+ (for backend)
- PostgreSQL (or Neon Serverless for cloud database)
- Git

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd hackathon-todo
```

2. **Setup Better Auth Server**
```bash
# Create auth server directory
mkdir auth-server && cd auth-server
npm init -y
npm install better-auth

# Create auth-server/index.js with Better Auth configuration
```

3. **Setup Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Configure environment variables
alembic upgrade head
uvicorn app.main:app --reload
```

4. **Setup Frontend**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Configure environment variables
npm run dev
```

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:8888
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BASE_URL=http://localhost:3000
BETTER_AUTH_URL=http://localhost:8888
```

## 📄 Specifications

This project follows spec-driven development. All features are defined in the `specs/` directory:

- **Architecture**: Clean, scalable design with proper separation of concerns
- **API**: RESTful endpoints with consistent response formats
- **Database**: Well-designed schema with proper relationships
- **UI/UX**: Professional interface with excellent user experience

## 🤝 Contributing

This project follows strict spec-driven development practices. All contributions must:

1. Align with existing specifications in the `specs/` directory
2. Update specifications when adding new features
3. Follow the established architecture patterns
4. Maintain type safety and proper error handling

## 📄 License

MIT License - Free to use and modify for learning and commercial purposes.