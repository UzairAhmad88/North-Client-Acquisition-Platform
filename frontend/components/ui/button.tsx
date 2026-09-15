import React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = "", variant = "default", size = "md", children, ...props }, ref) => {
    let baseStyles = "inline-flex items-center justify-center font-medium rounded-lg transition-colors disabled:opacity-50 disabled:pointer-events-none";
    let variantStyles = "bg-indigo-600 text-white hover:bg-indigo-700";

    if (variant === "outline") {
      variantStyles = "border border-gray-300 dark:border-gray-700 bg-transparent text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800";
    } else if (variant === "ghost") {
      variantStyles = "bg-transparent text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800";
    } else if (variant === "destructive") {
      variantStyles = "bg-rose-600 text-white hover:bg-rose-700";
    }

    let sizeStyles = "px-4 py-2 text-xs";
    if (size === "sm") sizeStyles = "px-2.5 py-1.5 text-[11px]";
    if (size === "lg") sizeStyles = "px-5 py-3 text-sm";

    return (
      <button ref={ref} className={`${baseStyles} ${variantStyles} ${sizeStyles} ${className}`} {...props}>
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
