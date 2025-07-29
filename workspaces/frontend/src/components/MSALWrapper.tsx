'use client';

import { MsalProvider } from '@azure/msal-react';
import { msalInstance } from '@/lib/msal-config';

interface MSALWrapperProps {
  children: React.ReactNode;
}

export function MSALWrapper({ children }: MSALWrapperProps) {
  return (
    <MsalProvider instance={msalInstance}>
      {children}
    </MsalProvider>
  );
}