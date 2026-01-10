# UI Components Specification

## Overview
This document outlines the reusable UI components for the TaskMaster application, following consistent design patterns and accessibility standards.

## Base Components

### 1. Button Component
**Purpose**: Trigger actions and navigate users

**Props**:
- `variant`: "primary" | "secondary" | "destructive" | "ghost" | "link"
- `size`: "sm" | "md" | "lg"
- `isLoading`: boolean (shows spinner when true)
- `children`: ReactNode
- Inherits all HTML button attributes

**Variants**:
- **Primary**: `bg-primary text-primary-foreground hover:bg-primary/90`
- **Secondary**: `bg-secondary text-secondary-foreground hover:bg-secondary/80`
- **Destructive**: `bg-destructive text-destructive-foreground hover:bg-destructive/90`
- **Ghost**: `hover:bg-accent hover:text-accent-foreground`
- **Link**: `underline-offset-4 hover:underline text-primary`

**Sizes**:
- **sm**: `h-9 px-3 rounded-md text-sm`
- **md**: `h-10 py-2 px-4 rounded-md`
- **lg**: `h-11 px-8 rounded-md text-base`

**States**:
- **Default**: Normal appearance with hover effects
- **Loading**: Shows spinner and reduced opacity
- **Disabled**: 50% opacity and pointer events disabled

**Accessibility**:
- Focus ring: `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2`
- Proper role and aria attributes
- Keyboard navigable

### 2. Input Component
**Purpose**: Collect user text input with validation

**Props**:
- `label`: Optional string for accessibility
- `error`: Optional string for error messaging
- `description`: Optional string for helper text
- Inherits all HTML input attributes

**Structure**:
- Label element with proper styling
- Input field with consistent padding and borders
- Error or description message below

**Styling**:
- Base: `flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm`
- Focus: `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2`
- Error: `border-destructive` when error prop provided
- Disabled: `disabled:cursor-not-allowed disabled:opacity-50`

**Accessibility**:
- Proper label association
- ARIA-invalid for error states
- Proper focus management

### 3. Card Component
**Purpose**: Group related content with consistent styling

**Props**:
- `children`: ReactNode
- `className`: Optional string for additional styling

**Styling**:
- Base: `bg-card text-card-foreground rounded-xl border border-border shadow-sm`
- Padding: Typically applied by parent components
- Consistent corner radius and border

**Usage**:
- Authentication forms
- Task items
- Statistics cards
- Content groupings

### 4. Checkbox Component
**Purpose**: Toggle completion state for tasks

**Props**:
- `checked`: boolean indicating state
- `onChange`: Function to handle state changes
- `disabled`: boolean for disabled state

**Styling**:
- Size: `h-5 w-5`
- Border: `border-2` with different states
- Background: Changes when checked
- Hover effects for interactivity
- Smooth transitions for state changes

## Task-Specific Components

### 5. TaskItem Component
**Purpose**: Display individual tasks with interactive controls

**Props**:
- `task`: Task object with title, description, completed, created_at
- `onUpdate`: Function to trigger refresh
- `userId`: String for API calls

**Structure**:
- Checkbox for completion toggle
- Task title with strikethrough when completed
- Optional description
- Metadata (creation date, completion status)
- Action buttons (delete)

**States**:
- **Pending**: Normal appearance
- **Completed**: Strikethrough title, muted text
- **Loading**: Reduced opacity during updates
- **Hover**: Subtle shadow increase

### 6. TaskForm Component
**Purpose**: Create new tasks with validation

**Props**:
- `onSubmit`: Function to handle form submission
- `isSubmitting`: Boolean for loading state

**Structure**:
- Title input with validation
- Description textarea with character counter
- Primary submit button
- Loading states

**Validation**:
- Title required (max 200 characters)
- Description optional (max 2000 characters)
- Real-time character counting

### 7. TaskList Component
**Purpose**: Display organized list of tasks

**Props**:
- `tasks`: Array of task objects
- `onTaskUpdate`: Function to refresh data
- `userId`: String for API calls

**Structure**:
- Statistics cards showing totals
- Pending tasks section
- Completed tasks section
- Empty state with illustration

**Sections**:
- **Stats**: Total, completed, pending counts
- **Pending**: Tasks not yet completed
- **Completed**: Tasks marked as complete
- **Empty**: Friendly message when no tasks

## Layout Components

### 8. TopBar Component
**Purpose**: Consistent navigation across application

**Structure**:
- App title/logo on left
- User profile dropdown on right
- Logout button
- Sticky positioning

**Elements**:
- Application name
- User avatar with initials
- User name and role
- Logout icon button

## Utility Components

### 9. Toast Provider
**Purpose**: Display temporary feedback messages

**Features**:
- Success, error, warning variants
- Auto-dismissal
- Positioning at top-right
- Smooth animations

### 10. Confirmation Dialog
**Purpose**: Confirm destructive actions

**Props**:
- `isOpen`: Boolean for visibility
- `onClose`: Function to close
- `onConfirm`: Function for confirmed action
- `title`: Dialog title
- `message`: Confirmation message
- `confirmText`: Text for confirm button
- `cancelText`: Text for cancel button

**Structure**:
- Modal overlay
- Card with title and message
- Confirm and cancel buttons

## Design Principles

### Consistency
- All components follow the same spacing system
- Typography scales are consistent
- Color usage follows established palette
- Interactive elements have consistent states

### Accessibility
- All interactive elements are keyboard accessible
- Sufficient color contrast ratios
- Proper ARIA attributes
- Semantic HTML structure
- Focus management

### Responsiveness
- Components adapt to different screen sizes
- Touch targets are appropriately sized
- Layout adjusts gracefully
- Typography remains readable

### State Management
- Loading states with spinners
- Error states with clear messaging
- Disabled states for inactive elements
- Hover and focus states for interactivity

## Component Relationships

### Composition Pattern
- Base components (Button, Input) compose into complex components (TaskForm)
- Complex components (TaskItem) compose into pages (Dashboard)
- Layout components provide structure (TopBar, Card)

### Data Flow
- Props flow down from parent to child
- Callbacks flow up for state changes
- Context providers for global state (auth, toasts)
- API clients for data fetching

## Styling Approach

### Tailwind CSS
- Utilize utility classes for consistent styling
- Custom properties for theme values
- Responsive prefixes for adaptive layouts
- Focus on composition over custom CSS

### Custom Properties
- CSS variables defined in globals.css
- Consistent naming convention
- Theme support with media queries
- Easy customization points

## Performance Considerations

### Rendering
- Efficient component trees
- Memoization where appropriate
- Lazy loading for non-critical content
- Optimized re-renders

### Bundle Size
- Tree-shaking for unused styles
- Minimal dependencies
- Efficient imports
- Compressed assets

This component system ensures consistent, accessible, and maintainable UI across the entire application.