"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { getCurrentUser, isAuthenticated, logout } from "@/lib/auth";
import { api } from "@/lib/api-client";
import type { Task, User } from "@/lib/types";
import { TaskList } from "@/components/tasks/TaskList";
import { TaskForm } from "@/components/tasks/TaskForm";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [createError, setCreateError] = useState<string | null>(null);

  useEffect(() => {
    // Check authentication
    if (!isAuthenticated()) {
      router.push("/login");
      return;
    }

    const currentUser = getCurrentUser();
    if (!currentUser) {
      router.push("/login");
      return;
    }

    setUser(currentUser);
    loadTasks(currentUser.id);
  }, [router]);

  const loadTasks = async (userId: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get<{ tasks: Task[]; total: number }>(
        `/users/${userId}/tasks`
      );
      setTasks(response.tasks);
    } catch (err) {
      console.error("Failed to load tasks:", err);
      setError("Failed to load tasks. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.push("/");
  };

  const handleTaskUpdate = async () => {
    // Reload tasks after update
    if (user) {
      await loadTasks(user.id);
    }
  };

  const handleCreateTask = async (title: string, description: string) => {
    if (!user) return;

    try {
      setIsCreating(true);
      setCreateError(null);

      await api.post(`/users/${user.id}/tasks`, {
        title,
        description: description || undefined,
      });

      // Refresh task list to show new task
      await loadTasks(user.id);
    } catch (err: any) {
      console.error("Failed to create task:", err);

      // Handle authentication errors
      if (err.status === 401 || err.status === 403) {
        logout();
        router.push("/login");
        return;
      }

      setCreateError(err.message || "Failed to create task. Please try again.");
      throw err; // Re-throw so form knows it failed
    } finally {
      setIsCreating(false);
    }
  };

  if (!user) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
            <p className="text-sm text-gray-600 mt-1">
              Welcome back, {user.name || user.email}
            </p>
          </div>
          <Button variant="secondary" onClick={handleLogout}>
            Log Out
          </Button>
        </div>
      </header>

      <main className="flex-grow max-w-7xl w-full mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="space-y-6">
          {/* Task Creation Form */}
          <TaskForm onSubmit={handleCreateTask} isSubmitting={isCreating} />

          {createError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {createError}
            </div>
          )}

          {/* Task List */}
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="text-gray-600">Loading tasks...</div>
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          ) : (
            <TaskList tasks={tasks} onTaskUpdate={handleTaskUpdate} userId={user.id} />
          )}
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            Phase II Todo Web Application
          </p>
        </div>
      </footer>
    </div>
  );
}
