# Authentication Feature Specification

## User Stories
- As a user, I want to register with email and password so that I can create an account
- As a user, I want to log in with my credentials so that I can access my tasks
- As a user, I want my sessions to be secure so that unauthorized users cannot access my data
- As a user, I want to log out so that others cannot access my account from shared devices
- As a system, I want to ensure data isolation so that users can only access their own data

## Acceptance Criteria
1. **Registration Flow**
   - User can register with valid email and password (min 8 chars)
   - System validates email format and password strength
   - User receives confirmation email (if verification enabled)
   - User is automatically logged in after registration

2. **Login Flow**
   - User can log in with registered email and password
   - System validates credentials against Better Auth service
   - Valid JWT token is issued upon successful authentication
   - Token is stored securely in the frontend

3. **Session Management**
   - JWT tokens have configurable expiration (default 7 days)
   - Tokens are automatically refreshed before expiration
   - Invalid/expired tokens are handled gracefully
   - Concurrent sessions are supported

4. **Security Requirements**
   - No custom authentication logic (only Better Auth)
   - JWT tokens are validated by calling Better Auth service
   - User ID from token is used for data isolation
   - All authenticated endpoints reject invalid tokens

5. **Data Isolation**
   - Users can only access their own tasks
   - User ID from JWT token is compared with requested user ID
   - 403 Forbidden returned for unauthorized access attempts

## Technical Specifications

### Frontend Authentication
- **Better Auth Client**: Use Better Auth's official client library
- **JWT Storage**: Store tokens in secure httpOnly cookies or secure localStorage
- **Token Refresh**: Automatic token refresh before expiration
- **Error Handling**: Clear error messages for authentication failures
- **Loading States**: Visual feedback during auth operations

### Backend Authentication
- **JWT Validation**: Call Better Auth service to validate tokens (no manual decoding)
- **User Extraction**: Extract user ID from validated token
- **Middleware**: Authentication middleware for protected routes
- **Dependency Injection**: Clean dependency injection for auth validation

### API Endpoints
- **Registration**: POST /api/auth/register (handled by Better Auth)
- **Login**: POST /api/auth/login (handled by Better Auth)
- **Protected Routes**: All /api/tasks/* endpoints require valid JWT
- **Session Validation**: Backend validates JWT by calling Better Auth service

## Security Rules
1. **No Custom Auth**: Must use Better Auth exclusively, no custom authentication logic
2. **Token Validation**: Backend validates tokens by calling Better Auth service, not manual JWT decoding
3. **User Isolation**: Always validate that authenticated user ID matches requested resource owner
4. **Secure Storage**: JWT tokens must be stored securely with proper security headers
5. **Proper Errors**: Return appropriate HTTP status codes (401, 403) for auth failures

## Error Scenarios
- **Invalid Credentials**: Return 401 Unauthorized with clear message
- **Expired Token**: Return 401 Unauthorized, trigger re-authentication
- **Invalid Token**: Return 401 Unauthorized, clear stored tokens
- **Unauthorized Resource Access**: Return 403 Forbidden
- **Network Issues**: Graceful degradation with appropriate error messages

## JWT Flow Explanation
1. User registers/logs in via Better Auth client on frontend
2. Better Auth issues JWT token to frontend
3. Frontend stores token securely
4. For protected API requests, frontend attaches token to Authorization header
5. Backend receives request and validates JWT by calling Better Auth service
6. Better Auth service confirms token validity and returns user info
7. Backend extracts user ID and enforces data isolation
8. Backend processes request and returns response

## Integration Points
- **Frontend ↔ Better Auth**: Direct communication for login/register
- **Frontend ↔ Backend**: JWT tokens passed in Authorization header
- **Backend ↔ Better Auth**: API calls to validate tokens and get user info
- **Backend ↔ Database**: User ID from token used for data queries