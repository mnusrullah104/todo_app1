/**
 * Dashboard page for the Todo App.
 *
 * This page displays the user's tasks and provides functionality to manage them.
 * It requires authentication and shows a task management interface.
 */
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthContext } from '@/components/AuthProvider';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { TaskForm } from '@/components/tasks/TaskForm';
import { TaskList } from '@/components/tasks/TaskList';
import { TaskStats } from '@/components/tasks/TaskStats';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { taskApi } from '@/lib/api';
import { Task } from '@/lib/api';

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout } = useAuthContext();
  const [taskRefreshTrigger, setTaskRefreshTrigger] = useState(0);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loadingStats, setLoadingStats] = useState(true);

  // Load tasks for stats when the page loads or refresh is triggered
  useEffect(() => {
    const loadTasksForStats = async () => {
      try {
        setLoadingStats(true);
        const response = await taskApi.getTasks();
        setTasks(response.tasks);
      } catch (error) {
        console.error('Error loading tasks for stats:', error);
      } finally {
        setLoadingStats(false);
      }
    };

    loadTasksForStats();
  }, [taskRefreshTrigger]);

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  const handleTaskCreated = () => {
    // Trigger a refresh of the task list and stats
    setTaskRefreshTrigger(prev => prev + 1);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-background">
        {/* Navigation */}
        <nav className="border-b border-border bg-card">
          <div className="container mx-auto px-4 py-3 flex justify-between items-center">
            <div className="text-2xl font-bold text-foreground">Todo App</div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-muted-foreground hidden sm:inline">
                Welcome, {user?.name || user?.email}
              </span>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                Log out
              </Button>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="container mx-auto px-4 py-8">
          <div className="max-w-3xl mx-auto">
            <div className="mb-8 text-center">
              <h1 className="text-3xl font-bold text-foreground mb-2">Your Tasks</h1>
              <p className="text-muted-foreground">Manage your tasks efficiently</p>
            </div>

            {/* Task Stats */}
            {loadingStats ? (
              <div className="flex justify-center items-center py-4">
                <div className="loading-spinner w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                <span className="ml-2 text-sm text-muted-foreground">Loading stats...</span>
              </div>
            ) : (
              <TaskStats tasks={tasks} />
            )}

            <Card className="mb-8">
              <CardHeader>
                <CardTitle>Create New Task</CardTitle>
              </CardHeader>
              <CardContent>
                <TaskForm onTaskCreated={handleTaskCreated} />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Your Task List</CardTitle>
              </CardHeader>
              <CardContent>
                <TaskList refreshTrigger={taskRefreshTrigger} />
              </CardContent>
            </Card>
          </div>
        </main>

        {/* Footer */}
        <footer className="border-t border-border py-6 mt-12">
          <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
            <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </ProtectedRoute>
  );
}