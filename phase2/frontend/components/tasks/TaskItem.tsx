"use client";

import { useState } from "react";
import type { Task } from "@/lib/types";
import { api } from "@/lib/api-client";
import { Button } from "@/components/ui/Button";

interface TaskItemProps {
  task: Task;
  onUpdate: () => Promise<void>;
  userId: string;
}

export function TaskItem({ task, onUpdate, userId }: TaskItemProps) {
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleToggleComplete = async () => {
    try {
      setIsUpdating(true);
      setError(null);
      await api.patch(`/users/${userId}/tasks/${task.id}`, {
        completed: !task.completed,
      });
      await onUpdate();
    } catch (err) {
      console.error("Failed to update task:", err);
      setError("Failed to update task");
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    try {
      setIsUpdating(true);
      setError(null);
      await api.delete(`/users/${userId}/tasks/${task.id}`);
      await onUpdate();
    } catch (err) {
      console.error("Failed to delete task:", err);
      setError("Failed to delete task");
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggleComplete}
          disabled={isUpdating}
          className={`mt-1 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
            task.completed
              ? "bg-green-500 border-green-500"
              : "border-gray-300 hover:border-green-500"
          } ${isUpdating ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
          aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.completed && (
            <svg
              className="w-3 h-3 text-white"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M5 13l4 4L19 7"></path>
            </svg>
          )}
        </button>

        {/* Task Content */}
        <div className="flex-grow min-w-0">
          <h3
            className={`text-base font-medium ${
              task.completed
                ? "line-through text-gray-500"
                : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.completed ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}
          <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
            <span>
              Created: {new Date(task.created_at).toLocaleDateString()}
            </span>
            {task.completed && (
              <span className="text-green-600 font-medium">Completed</span>
            )}
          </div>
          {error && (
            <p className="mt-2 text-sm text-red-600">{error}</p>
          )}
        </div>

        {/* Actions */}
        <div className="flex-shrink-0">
          <Button
            variant="danger"
            size="sm"
            onClick={handleDelete}
            disabled={isUpdating}
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
}
