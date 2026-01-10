/**
 * Protected Route component for the Todo App.
 *
 * Renders the child component only if the user is authenticated.
 * Otherwise, redirects to the login page.
 */
'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuthContext } from '@/components/AuthProvider';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center">
        <div className="loading-spinner w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="mt-2 text-muted-foreground">Checking authentication...</p>
      </div>
    </div>
  )
}) => {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuthContext();

  if (isLoading) {
    return fallback;
  }

  if (!isAuthenticated) {
    // Redirect to login page
    router.push('/login');
    return null;
  }

  return <>{children}</>;
};

export { ProtectedRoute };