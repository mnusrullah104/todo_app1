/**
 * Reusable Input component with Tailwind CSS styling.
 */
import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({
  label,
  error,
  className = "",
  ...props
}: InputProps) {
  const inputClassName = `
    w-full px-3 py-2 border rounded-lg
    focus:outline-none focus:ring-2 focus:ring-blue-500
    ${error ? "border-red-500" : "border-gray-300"}
    ${className}
  `.trim();

  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <input className={inputClassName} {...props} />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}
