/**
 * Better Auth client configuration for the Todo App.
 *
 * Sets up the Better Auth client for frontend authentication.
 */
import { createAuthClient } from "@better-auth/react";

// Initialize the Better Auth client
export const auth = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3001",
});