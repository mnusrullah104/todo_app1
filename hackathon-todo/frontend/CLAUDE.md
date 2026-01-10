# Frontend Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-09

## Active Technologies

- **Framework**: Next.js 16+ (App Router, TypeScript)
- **Styling**: Tailwind CSS with custom configuration
- **State Management**: React Hooks + Context API (where needed)
- **API Client**: Custom fetch wrapper with Better Auth integration
- **Authentication**: Better Auth client
- **Environment**: Node.js 18+

## Project Structure

```text
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── layout.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Label.tsx
│   │   └── ...
│   ├── tasks/
│   │   ├── TaskForm.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskList.tsx
│   │   └── TaskStats.tsx
│   └── auth/
│       ├── LoginForm.tsx
│       └── RegisterForm.tsx
├── lib/
│   ├── auth.ts
│   ├── api.ts
│   ├── types.ts
│   └── utils.ts
├── hooks/
│   ├── useAuth.ts
│   ├── useTasks.ts
│   └── ...
├── .env.local.example
├── .gitignore
├── CLAUDE.md
├── package.json
├── README.md
├── tailwind.config.ts
├── tsconfig.json
└── next.config.ts
```

## Commands

### Development
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run linter
- `npm run type-check` - Run type checker

### Testing
- `npm test` - Run unit tests (when implemented)
- `npm run test:e2e` - Run E2E tests (when implemented)

## Code Style

### TypeScript
- Use TypeScript for all components and modules
- Implement proper type definitions for all props and functions
- Use interfaces over types for object shapes
- Follow naming conventions: PascalCase for components, camelCase for functions/variables

### React/Next.js
- Use functional components with hooks
- Follow Next.js App Router conventions
- Implement proper error boundaries
- Use React.Suspense for lazy-loaded components
- Implement proper loading states
- Follow accessibility best practices

### Styling
- Use Tailwind CSS utility classes
- Implement responsive design with mobile-first approach
- Use consistent spacing and typography scales
- Follow the design system defined in tailwind.config.ts

## Recent Changes

- Initial project structure setup
- Better Auth integration
- Task management components
- API client with Better Auth token handling
- Responsive UI components

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->