'use client';

import { useIsAuthenticated, useMsal } from '@azure/msal-react';
import LoginButton from './LoginButton';
import LogoutButton from './LogoutButton';

export default function AuthStatus() {
  const isAuthenticated = useIsAuthenticated();
  const { accounts } = useMsal();

  if (isAuthenticated && accounts.length > 0) {
    const account = accounts[0];
    return (
      <div className="flex flex-col items-center gap-4">
        <div className="text-center">
          <p className="text-sm">Welcome,</p>
          <p className="font-bold">{account.name || account.username}</p>
          <p className="text-xs text-gray-600">{account.username}</p>
        </div>
        <LogoutButton />
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center gap-4">
      <p className="text-center">Please sign in to continue</p>
      <LoginButton />
    </div>
  );
}