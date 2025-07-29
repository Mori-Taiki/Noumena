'use client';

import { useMsal } from '@azure/msal-react';
import { loginRequest } from '@/lib/msal-config';

export default function LoginButton() {
  const { instance } = useMsal();

  const handleLogin = () => {
    instance.loginRedirect(loginRequest).catch((e) => {
      console.error('Login failed:', e);
    });
  };

  return (
    <button
      onClick={handleLogin}
      className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
    >
      Login
    </button>
  );
}