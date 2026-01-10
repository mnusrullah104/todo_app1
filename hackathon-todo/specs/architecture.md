# Todo App - Architecture Specification

## System Architecture
The application follows a clean, modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Auth Server     │    │    Backend      │
│  (Next.js)      │◄──►│  (Better Auth)   │◄──►│   (FastAPI)     │
│                 │    │                  │    │                 │
│ - React UI      │    │ - JWT Generation │    │ - Business Logic│
│ - State Mgmt    │    │ - User Mgmt      │    │ - Data Access   │
│ - API Client    │    │ - Session Mgmt   │    │ - Auth Mgmt     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                        ┌──────────────────┐
                        │   Database       │
                        │ (PostgreSQL)     │
                        └──────────────────┘
```

## Technology Stack
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS, React Hooks
- **Backend**: FastAPI, Python 3.11+, SQLModel, SQLAlchemy
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT
- **Deployment**: Vercel (Frontend), Railway/Docker (Backend)

## Layered Architecture

### 1. Presentation Layer (Frontend)
- **Components**: Reusable UI components with TypeScript interfaces
- **Pages**: Next.js App Router pages with proper routing
- **Hooks**: Custom React hooks for data fetching and state management
- **API Client**: Centralized API client with JWT token management

### 2. Service Layer (Backend)
- **API Layer**: FastAPI endpoints with proper validation
- **Business Logic**: Service classes with clean interfaces
- **Data Access**: Repository pattern with SQLModel
- **Authentication**: JWT middleware and validation

### 3. Data Layer
- **Models**: SQLModel classes with proper relationships
- **Schemas**: Pydantic models for request/response validation
- **Database**: PostgreSQL with proper indexing and constraints

## Security Architecture
- **Authentication**: JWT-based with Better Auth
- **Authorization**: Role-based access control at API level
- **Data Isolation**: User ID validation in all endpoints
- **Input Validation**: Pydantic models for all requests
- **Rate Limiting**: Per-user and global rate limiting

## API Architecture
- **RESTful Design**: Consistent endpoint patterns
- **Versioning**: API versioning in URL paths
- **Error Handling**: Standardized error response format
- **Documentation**: Automatic OpenAPI/Swagger generation

## Deployment Architecture
- **Frontend**: Static hosting on Vercel with CDN
- **Backend**: Containerized with Docker, deployed to Railway
- **Database**: Neon Serverless PostgreSQL with connection pooling
- **Auth**: Separate Better Auth service (can be self-hosted or cloud)

## Performance Considerations
- **Caching**: HTTP caching headers and CDN for static assets
- **Database**: Proper indexing and connection pooling
- **Frontend**: Code splitting and lazy loading
- **Backend**: Async operations and connection management

## Scalability Patterns
- **Horizontal Scaling**: Stateless services ready for containerization
- **Database Scaling**: Connection pooling and optimized queries
- **Load Balancing**: Ready for reverse proxy setup
- **Caching Layer**: Redis integration points prepared