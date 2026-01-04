import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-gray-900">Todo App</h1>
        </div>
      </header>

      <main className="flex-grow flex items-center justify-center bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
              Manage your tasks
            </h2>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              A secure, multi-user todo application built with Next.js and
              FastAPI. Keep track of your tasks with ease.
            </p>
            <div className="mt-10 flex justify-center gap-4">
              <Link href="/register">
                <Button size="lg">Get Started</Button>
              </Link>
              <Link href="/login">
                <Button variant="secondary" size="lg">
                  Sign In
                </Button>
              </Link>
            </div>
          </div>

          <div className="mt-16">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
              <div className="text-center">
                <div className="text-blue-600 text-4xl mb-4">🔒</div>
                <h3 className="text-lg font-medium text-gray-900">
                  Secure Authentication
                </h3>
                <p className="mt-2 text-base text-gray-500">
                  JWT-based authentication keeps your data safe and isolated.
                </p>
              </div>
              <div className="text-center">
                <div className="text-blue-600 text-4xl mb-4">📝</div>
                <h3 className="text-lg font-medium text-gray-900">
                  Task Management
                </h3>
                <p className="mt-2 text-base text-gray-500">
                  Create, update, and complete tasks with a clean interface.
                </p>
              </div>
              <div className="text-center">
                <div className="text-blue-600 text-4xl mb-4">📱</div>
                <h3 className="text-lg font-medium text-gray-900">
                  Responsive Design
                </h3>
                <p className="mt-2 text-base text-gray-500">
                  Works seamlessly on desktop and mobile devices.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            Phase II Todo Web Application - Built with Next.js and FastAPI
          </p>
        </div>
      </footer>
    </div>
  );
}
