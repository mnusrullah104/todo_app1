/**
 * Home/Landing page for the Hackathon Todo App.
 *
 * This page serves as the entry point for unauthenticated users,
 * providing information about the app and a call-to-action to get started.
 */
"use client";

import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6">
        <div className="text-2xl font-bold text-foreground">Todo App</div>
        <div className="flex items-center space-x-4">
          <Link href="/login">
            <Button variant="ghost">Log in</Button>
          </Link>
          <Link href="/register">
            <Button variant="primary">Get Started</Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6">
            Manage Your Tasks Effortlessly
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            A modern, secure todo application with seamless authentication and intuitive task management.
            Get started in seconds and boost your productivity today.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4 mb-16">
            <Link href="/register">
              <Button size="lg" className="px-8 py-3 text-base">
                Create Account
              </Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg" className="px-8 py-3 text-base">
                Sign In
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <Card className="p-6">
            <div className="text-primary text-3xl mb-4">✓</div>
            <h3 className="text-xl font-semibold mb-2">Secure Authentication</h3>
            <p className="text-muted-foreground">
              Powered by Better Auth for secure, reliable user management with JWT tokens.
            </p>
          </Card>

          <Card className="p-6">
            <div className="text-primary text-3xl mb-4">✓</div>
            <h3 className="text-xl font-semibold mb-2">Task Management</h3>
            <p className="text-muted-foreground">
              Create, update, and organize your tasks with an intuitive interface.
            </p>
          </Card>

          <Card className="p-6">
            <div className="text-primary text-3xl mb-4">✓</div>
            <h3 className="text-xl font-semibold mb-2">Data Isolation</h3>
            <p className="text-muted-foreground">
              Your data is isolated and secure, accessible only to you.
            </p>
          </Card>
        </div>

        {/* CTA Section */}
        <div className="max-w-2xl mx-auto text-center mt-16">
          <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-4">
            Ready to get started?
          </h2>
          <p className="text-muted-foreground mb-8">
            Join thousands of users who trust our platform for their daily task management needs.
          </p>
          <Link href="/register">
            <Button size="lg" className="px-8 py-3 text-base">
              Sign up for free
            </Button>
          </Link>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-8 mt-16">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}