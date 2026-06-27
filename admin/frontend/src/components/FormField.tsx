'use client';

import { ReactNode, SelectHTMLAttributes, TextareaHTMLAttributes, InputHTMLAttributes } from 'react';

interface BaseProps {
  label: string;
  error?: string;
  helperText?: string;
  required?: boolean;
}

interface InputFieldProps extends BaseProps, InputHTMLAttributes<HTMLInputElement> {
  type?: 'text' | 'email' | 'password' | 'number' | 'url' | 'date' | 'file';
}

interface SelectFieldProps extends BaseProps, SelectHTMLAttributes<HTMLSelectElement> {
  type: 'select';
  options: { value: string; label: string }[];
  placeholder?: string;
}

interface TextareaFieldProps extends BaseProps, TextareaHTMLAttributes<HTMLTextAreaElement> {
  type: 'textarea';
}

interface ToggleFieldProps extends BaseProps {
  type: 'toggle';
  checked: boolean;
  onChange: (checked: boolean) => void;
}

type FormFieldProps = InputFieldProps | SelectFieldProps | TextareaFieldProps | ToggleFieldProps;

export default function FormField(props: FormFieldProps) {
  const { label, error, helperText, required, type = 'text' } = props;

  const inputClasses = `input ${error ? 'input-error' : ''}`;

  const renderField = () => {
    switch (type) {
      case 'select': {
        const { label: _, error: _e, helperText: _h, required: _r, type: _t, options, placeholder, ...rest } = props as SelectFieldProps;
        return (
          <select className={inputClasses} {...rest}>
            {placeholder && <option value="">{placeholder}</option>}
            {options.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        );
      }
      case 'textarea': {
        const { label: _, error: _e, helperText: _h, required: _r, type: _t, ...rest } = props as TextareaFieldProps;
        return <textarea className={inputClasses} {...rest} />;
      }
      case 'toggle': {
        const { label: _l, error: _e, helperText: _h, required: _r, type: _t, checked, onChange, ...rest } = props as ToggleFieldProps;
        return (
          <button
            type="button"
            onClick={() => onChange(!checked)}
            className={`relative w-11 h-6 rounded-full transition-colors ${
              checked ? 'bg-admin-600' : 'bg-slate-300 dark:bg-slate-600'
            }`}
          >
            <span
              className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${
                checked ? 'translate-x-5' : ''
              }`}
            />
          </button>
        );
      }
      default: {
        const { label: _, error: _e, helperText: _h, required: _r, type: _t, ...rest } = props as InputFieldProps;
        return <input type={type} className={`${inputClasses} ${type === 'file' ? 'file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-admin-50 file:text-admin-700 dark:file:bg-admin-900/30 dark:file:text-admin-300 hover:file:bg-admin-100' : ''}`} {...rest} />;
      }
    }
  };

  return (
    <div className="space-y-1">
      <label className="label">
        {label}
        {required && <span className="text-red-500 ml-0.5">*</span>}
      </label>
      {renderField()}
      {error && <p className="text-xs text-red-500 mt-0.5">{error}</p>}
      {helperText && !error && <p className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">{helperText}</p>}
    </div>
  );
}
