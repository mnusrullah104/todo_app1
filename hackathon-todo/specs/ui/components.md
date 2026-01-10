# UI Components Specification

## Component Architecture
The UI follows a component-based architecture with reusable elements and clear hierarchy:

```
Layout Components
├── Header
├── Navigation
├── Main Content Area
├── Footer
└── Modal/Dialog Layer

Feature Components
├── Authentication
│   ├── LoginForm
│   ├── RegisterForm
│   └── ForgotPasswordForm
├── Task Management
│   ├── TaskList
│   ├── TaskItem
│   ├── TaskForm
│   ├── TaskStats
│   └── EmptyState
└── Shared Components
    ├── Button
    ├── Input
    ├── Card
    ├── Alert
    ├── LoadingSpinner
    └── Toast
```

## Typography System
- **Font Family**: System font stack (Inter, SF Pro, Segoe UI, etc.)
- **Heading Scale**:
  - H1: 2.5rem (40px) - Page titles
  - H2: 2rem (32px) - Section headings
  - H3: 1.5rem (24px) - Subsection headings
  - H4: 1.25rem (20px) - Small headings
- **Body Text**:
  - Large: 1.125rem (18px) - Primary content
  - Regular: 1rem (16px) - Secondary content
  - Small: 0.875rem (14px) - Labels, captions
- **Line Height**: 1.5 for body text, 1.25 for headings

## Color Palette
- **Primary**: #3B82F6 (Blue-500) - Buttons, links, highlights
- **Secondary**: #6B7280 (Gray-500) - Secondary buttons, muted text
- **Success**: #10B981 (Emerald-500) - Success states, positive actions
- **Warning**: #F59E0B (Amber-500) - Warnings, caution states
- **Danger**: #EF4444 (Red-500) - Error states, destructive actions
- **Background**: #FFFFFF (White) - Main background
- **Surface**: #F9FAFB (Gray-50) - Card backgrounds
- **Text**: #111827 (Gray-900) - Primary text
- **Text Secondary**: #6B7280 (Gray-500) - Secondary text

## Spacing System
- **Base Unit**: 0.25rem (4px)
- **Scale**: 0, 0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8 (in rem units)
- **Common Spacing**:
  - Component padding: 1rem
  - Section spacing: 2rem
  - Grid gaps: 1rem
  - Form element spacing: 0.5rem

## Shared Components

### Button
- **Variants**: Primary, Secondary, Success, Warning, Danger, Ghost
- **Sizes**: Small (sm), Medium (md), Large (lg)
- **States**: Default, Hover, Active, Disabled, Loading
- **Accessibility**: Proper focus states, ARIA labels for icon buttons
- **Props**:
  - variant: "primary" | "secondary" | "success" | "warning" | "danger" | "ghost"
  - size: "sm" | "md" | "lg"
  - disabled: boolean
  - loading: boolean
  - onClick: () => void
  - children: ReactNode

### Input
- **Types**: Text, Password, Email, Number, TextArea
- **States**: Default, Focused, Error, Success, Disabled
- **Features**: Label, Helper text, Error message, Prefix/suffix icons
- **Accessibility**: Proper labels, error announcements
- **Props**:
  - label: string
  - type: "text" | "password" | "email" | "number"
  - value: string
  - onChange: (value: string) => void
  - error: string
  - helperText: string
  - disabled: boolean

### Card
- **Purpose**: Contain related content with consistent styling
- **Variants**: Default, Elevated, Outline
- **Padding**: Default 1.5rem
- **Border Radius**: 0.5rem (8px)
- **Shadow**: Subtle elevation effect
- **Props**:
  - variant: "default" | "elevated" | "outline"
  - children: ReactNode
  - className: string

### LoadingSpinner
- **Purpose**: Indicate loading states
- **Size**: Small (1rem), Medium (1.5rem), Large (2rem)
- **Color**: Primary brand color by default
- **Animation**: Smooth rotation animation
- **Props**:
  - size: "sm" | "md" | "lg"
  - color: string

### Alert
- **Variants**: Info, Success, Warning, Error
- **Features**: Close button, icon, title, description
- **Behaviors**: Auto-dismissible, manual dismiss
- **Props**:
  - variant: "info" | "success" | "warning" | "error"
  - title: string
  - description: string
  - closable: boolean
  - onClose?: () => void

### Toast
- **Purpose**: Temporary notifications
- **Position**: Top-right corner
- **Duration**: Auto-dismiss after 5 seconds
- **Variants**: Success, Error, Warning, Info
- **Props**:
  - message: string
  - variant: "success" | "error" | "warning" | "info"
  - duration: number

## Authentication Components

### LoginForm
- **Purpose**: User login form
- **Fields**: Email, Password
- **Features**: "Remember me" checkbox, "Forgot password" link
- **Validation**: Real-time validation with error messages
- **Actions**: Login, Navigate to registration
- **Props**:
  - onSubmit: (credentials: {email: string, password: string}) => void
  - onForgotPassword: () => void
  - onNavigateToRegister: () => void

### RegisterForm
- **Purpose**: User registration form
- **Fields**: Email, Password, Confirm Password, Name (optional)
- **Features**: Password strength indicator, terms acceptance
- **Validation**: Real-time validation with error messages
- **Actions**: Register, Navigate to login
- **Props**:
  - onSubmit: (userData: {email: string, password: string, name?: string}) => void
  - onNavigateToLogin: () => void

## Task Management Components

### TaskList
- **Purpose**: Display list of tasks with filtering/sorting
- **Features**:
  - Grouping by completion status (Pending/Completed)
  - Stats display (total, completed, pending)
  - Empty state
  - Loading state
- **Props**:
  - tasks: Task[]
  - loading: boolean
  - onTaskToggle: (taskId: string) => void
  - onTaskDelete: (taskId: string) => void
  - onTaskEdit: (taskId: string) => void

### TaskItem
- **Purpose**: Individual task display with actions
- **Features**:
  - Checkbox for completion toggle
  - Title and description
  - Created date
  - Action buttons (Edit, Delete)
  - Completion strikethrough
- **Props**:
  - task: Task
  - onToggle: () => void
  - onDelete: () => void
  - onEdit: () => void

### TaskForm
- **Purpose**: Create/edit task form
- **Fields**: Title (required), Description (optional), Completion status
- **Features**: Character counters, validation
- **Actions**: Save, Cancel
- **Props**:
  - task?: Task (if editing)
  - onSubmit: (taskData: {title: string, description?: string, completed: boolean}) => void
  - onCancel: () => void

### TaskStats
- **Purpose**: Display task statistics
- **Features**: Total tasks, completed tasks, pending tasks
- **Visual**: Progress bar, percentage, numbers
- **Props**:
  - total: number
  - completed: number
  - pending: number

### EmptyState
- **Purpose**: Display when no tasks exist
- **Features**: Friendly illustration, encouraging message, create task button
- **Props**:
  - onAction: () => void
  - actionText: string

## Layout Components

### Header
- **Purpose**: Main navigation and user controls
- **Features**:
  - Logo/branding
  - Navigation links
  - User profile dropdown
  - Mobile hamburger menu
- **Props**:
  - user?: User
  - navLinks: NavLink[]
  - onLogout: () => void

### Navigation
- **Purpose**: Main application navigation
- **Features**: Active state highlighting, icons, responsive
- **Props**:
  - links: NavLink[]
  - currentPath: string

### Main Content Area
- **Purpose**: Container for page content
- **Features**: Consistent padding, max-width, responsive
- **Props**:
  - children: ReactNode

### Footer
- **Purpose**: Page footer with secondary information
- **Features**: Copyright, links, social media
- **Props**:
  - links: FooterLink[]

## Responsive Design

### Breakpoints
- **Mobile**: 0px - 640px
- **Tablet**: 641px - 1024px
- **Desktop**: 1025px+

### Responsive Behaviors
- **Mobile**: Stacked layouts, touch-friendly targets, hamburger menus
- **Tablet**: Adaptive layouts, medium-sized targets, split menus
- **Desktop**: Expanded layouts, precise targets, full menus

## Accessibility Standards
- **WCAG 2.1 AA**: All components meet accessibility guidelines
- **Keyboard Navigation**: Full keyboard operability
- **Screen Reader Support**: Proper ARIA labels and roles
- **Focus Management**: Clear focus indicators and logical focus order
- **Color Contrast**: Minimum 4.5:1 contrast ratio

## Animation & Transitions
- **Duration**: 150ms for micro-interactions, 300ms for major transitions
- **Easing**: Cubic-bezier(0.4, 0, 0.2, 1) for smooth animations
- **Elements**: Fade, slide, scale for state changes
- **Performance**: Hardware-accelerated transforms where possible

## Internationalization (i18n)
- **Text Direction**: Support for RTL languages
- **Date/Time**: Localized formats
- **Numbers**: Localized formatting
- **Plurals**: Proper pluralization handling
- **Text Expansion**: Account for text expansion in translations

## Component Props Interface

### Common Prop Types
```typescript
interface CommonProps {
  className?: string;
  children?: React.ReactNode;
  style?: React.CSSProperties;
}

interface WithId {
  id: string;
}

interface WithData {
  data?: Record<string, any>;
}
```

### Form Element Props
```typescript
interface FormElementProps {
  value: string | boolean;
  onChange: (value: any) => void;
  error?: string;
  disabled?: boolean;
  required?: boolean;
}
```

## Testing Requirements
- **Unit Tests**: Each component has unit tests for props and interactions
- **Integration Tests**: Component combinations work as expected
- **Accessibility Tests**: Automated a11y testing with axe-core
- **Visual Regression**: Storybook-based visual testing
- **Responsive Tests**: Cross-device layout verification