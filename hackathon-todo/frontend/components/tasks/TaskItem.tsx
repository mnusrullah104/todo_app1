/**
 * Task Item component for the Todo App.
 *
 * Displays a single task with options to edit, delete, and mark as complete.
 */
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { taskApi } from '@/lib/api';
import { useToast } from '@/components/ToastProvider';
import { Task } from '@/lib/api';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: (updatedTask: Task) => void;
  onTaskDeleted: (taskId: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskUpdated, onTaskDeleted }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const { addToast } = useToast();

  const handleToggleComplete = async () => {
    try {
      const updatedTask = await taskApi.toggleTaskCompletion(task.id, !task.completed);
      onTaskUpdated(updatedTask);
      addToast(
        `Task marked as ${updatedTask.completed ? 'complete' : 'incomplete'}`,
        'success'
      );
    } catch (error: any) {
      console.error('Error toggling task completion:', error);
      addToast('Failed to update task status', 'error');
    }
  };

  const handleSaveEdit = async () => {
    try {
      const updatedTask = await taskApi.updateTask(task.id, {
        title,
        description: description || undefined,
      });
      onTaskUpdated(updatedTask);
      setIsEditing(false);
      addToast('Task updated successfully', 'success');
    } catch (error: any) {
      console.error('Error updating task:', error);
      addToast('Failed to update task', 'error');
    }
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await taskApi.deleteTask(task.id);
      onTaskDeleted(task.id);
      addToast('Task deleted successfully', 'success');
    } catch (error: any) {
      console.error('Error deleting task:', error);
      addToast('Failed to delete task', 'error');
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div
      className={`task-item card p-4 mb-3 border rounded-lg ${
        task.completed ? 'task-completed bg-muted' : 'bg-card'
      }`}
    >
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-2 border rounded-md"
            placeholder="Task title"
            autoFocus
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-2 border rounded-md"
            placeholder="Task description (optional)"
            rows={3}
          />
          <div className="flex space-x-2">
            <Button
              variant="primary"
              size="sm"
              onClick={handleSaveEdit}
              className="flex-1"
            >
              Save
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setIsEditing(false);
                setTitle(task.title);
                setDescription(task.description || '');
              }}
              className="flex-1"
            >
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-start">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={handleToggleComplete}
                className="mt-1 mr-3 h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
              />
              <div>
                <h3 className={`task-title text-lg font-medium ${task.completed ? 'line-through text-muted-foreground' : ''}`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className={`mt-1 ${task.completed ? 'line-through text-muted-foreground' : 'text-muted-foreground'}`}>
                    {task.description}
                  </p>
                )}
                <p className="text-xs text-muted-foreground mt-2">
                  Created: {formatDate(task.createdAt)}
                  {task.updatedAt !== task.createdAt && ` • Updated: ${formatDate(task.updatedAt)}`}
                </p>
              </div>
            </div>
          </div>
          <div className="flex space-x-2 ml-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsEditing(true)}
              aria-label="Edit task"
            >
              ✏️
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleDelete}
              loading={isDeleting}
              aria-label="Delete task"
            >
              🗑️
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export { TaskItem };