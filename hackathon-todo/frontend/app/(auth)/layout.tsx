/**
 * Layout for authentication pages in the Todo App.
 *
 * This layout provides a consistent structure for login and registration pages.
 */
'use client';

import React from 'react';
import Link from 'next/link';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="py-4">
        <div className="container mx-auto px-4 flex justify-center">
          <Link href="/" className="text-2xl font-bold text-foreground">
            Todo App
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="py-6 mt-auto">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}