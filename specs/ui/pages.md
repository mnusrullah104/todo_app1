# UI Pages Specification

## Overview
This document outlines the UI pages for the TaskMaster application, a modern todo management application with clean, professional design and intuitive user experience.

## Design System

### Color Palette
- **Background**: #F7F8FA (soft light gray)
- **Card Background**: #FFFFFF (white)
- **Primary**: #4f46e5 (indigo) - for primary actions and highlights
- **Secondary**: #f3f4f6 (light gray) - for secondary elements
- **Success**: #10b981 (emerald green) - for positive actions
- **Warning**: #f59e0b (amber) - for warnings
- **Destructive**: #ef4444 (red) - for destructive actions
- **Text**: #1f2937 (dark gray) - for primary text
- **Muted**: #6b7280 (gray) - for secondary text

### Typography
- **Page Titles**: 1.25rem (20px), font-medium
- **Section Headers**: 1.125rem (18px), font-semibold
- **Body Text**: 1rem (16px), font-normal
- **Labels**: 0.875rem (14px), font-medium
- **Captions**: 0.75rem (12px), font-normal

### Spacing System
- **Spacing-1**: 0.25rem (4px)
- **Spacing-2**: 0.5rem (8px)
- **Spacing-3**: 0.75rem (12px)
- **Spacing-4**: 1rem (16px)
- **Spacing-6**: 1.5rem (24px)
- **Spacing-8**: 2rem (32px)

## Page Specifications

### 1. Authentication Pages

#### Sign In Page (`/login`)
**Purpose**: Allow existing users to authenticate

**Layout**:
- Centered card on full-height background
- Max width: 448px (max-w-md)
- Vertical spacing: 3rem (py-12)
- Horizontal padding: 1rem (px-4), scales to 2rem on larger screens

**Components**:
- Header with title "Welcome back" and subtitle
- Email input field with label
- Password input field with label
- Primary sign-in button with loading state
- Link to registration page

**States**:
- Loading: Button shows spinner and "Signing in..." text
- Error: Inline validation messages appear below fields
- Success: Redirects to dashboard

#### Sign Up Page (`/register`)
**Purpose**: Allow new users to create accounts

**Layout**:
- Same as sign in page
- Three input fields: email, password, name (optional)

**Components**:
- Header with title "Create your account"
- Email input with validation
- Password input with minimum length requirement
- Name input (optional)
- Primary create account button
- Link to sign in page

**States**:
- Loading: Button shows spinner and "Creating account..." text
- Validation: Real-time validation with error messages
- Success: Redirects to dashboard

### 2. Main Application Pages

#### Dashboard (`/dashboard`)
**Purpose**: Main application interface for task management

**Layout**:
- Sticky top navigation bar (16px height)
- Two-column layout on desktop (responsive grid)
  - Left column: Task creation form (1/3 width on lg screens)
  - Right column: Task list and stats (2/3 width on lg screens)
- Footer with copyright information

**Components**:
- **Top Bar**:
  - App logo/title on left
  - User profile with initials avatar and logout button on right
- **Left Column**:
  - Task creation form in card container
  - Title "Create New Task" with icon
  - Input fields for title and description
  - Primary "Add Task" button
- **Right Column**:
  - Task statistics cards showing totals
  - Task list with pending/completed sections
  - Empty state when no tasks exist

**States**:
- Loading: Skeleton loader with spinner animation
- Error: Error message card with icon
- Empty: Friendly empty state with tips
- Normal: Task list with checkboxes and actions

## Responsive Behavior

### Mobile (up to 1024px)
- Single column layout
- Top bar remains sticky
- Task creation form above task list
- Logout button compact (icon only)

### Desktop (1024px and above)
- Two-column layout as described above
- Full user information visible in top bar
- More space for task details and actions

## Navigation Flow
1. Unauthenticated user → `/login` or `/register`
2. Successful authentication → `/dashboard`
3. From dashboard → logout returns to home/login
4. Error states → appropriate error messages without navigation

## Accessibility
- Proper semantic HTML structure
- Sufficient color contrast ratios
- Keyboard navigable components
- ARIA labels for interactive elements
- Focus states for keyboard users
- Screen reader friendly content structure

## Visual States
- **Hover**: Subtle background changes and transitions
- **Focus**: Visible focus rings around interactive elements
- **Active**: Pressed states for buttons
- **Loading**: Spinner animations and disabled states
- **Error**: Red border and text for invalid fields
- **Success**: Green indicators for successful actions