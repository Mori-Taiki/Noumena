'use client';

import { useMsal } from '@azure/msal-react';

export default function LogoutButton() {
  const { instance } = useMsal();

  const handleLogout = () => {
    instance.logoutRedirect({
      postLogoutRedirectUri: '/',
    }).catch((e) => {
      console.error('Logout failed:', e);
    });
  };

  return (
    <button
      onClick={handleLogout}
      className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
    >
      Logout
    </button>
  );
}