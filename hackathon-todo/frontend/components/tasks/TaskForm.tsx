/**
 * Task Form component for the Todo App.
 *
 * Provides a form for creating new tasks.
 */
'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { taskApi } from '@/lib/api';
import { useToast } from '@/components/ToastProvider';

interface TaskFormProps {
  onTaskCreated: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ onTaskCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const { addToast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      addToast('Title is required', 'error');
      return;
    }

    setLoading(true);

    try {
      await taskApi.createTask({
        title: title.trim(),
        description: description.trim() || undefined,
      });

      // Reset form
      setTitle('');
      setDescription('');

      // Notify parent component
      onTaskCreated();

      // Show success message
      addToast('Task created successfully', 'success');
    } catch (error: any) {
      console.error('Error creating task:', error);
      addToast('Failed to create task', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="space-y-4">
        <div>
          <Input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title"
            className="w-full"
            disabled={loading}
          />
        </div>
        <div>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Task description (optional)"
            className="w-full p-2 border border-input bg-background rounded-md text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 min-h-[80px]"
            disabled={loading}
          />
        </div>
        <Button
          type="submit"
          variant="primary"
          loading={loading}
          className="w-full"
        >
          Add Task
        </Button>
      </div>
    </form>
  );
};

export { TaskForm };

// Create Textarea component as it's referenced but not created