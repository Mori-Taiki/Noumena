import { Configuration, PublicClientApplication } from '@azure/msal-browser';

// MSAL configuration
const msalConfig: Configuration = {
  auth: {
    clientId: process.env.NEXT_PUBLIC_AZURE_B2C_CLIENT_ID || '',
    authority: `https://${process.env.NEXT_PUBLIC_AZURE_B2C_TENANT_NAME}.b2clogin.com/${process.env.NEXT_PUBLIC_AZURE_B2C_TENANT_NAME}.onmicrosoft.com/${process.env.NEXT_PUBLIC_AZURE_B2C_POLICY_NAME}`,
    knownAuthorities: [`${process.env.NEXT_PUBLIC_AZURE_B2C_TENANT_NAME}.b2clogin.com`],
    redirectUri: typeof window !== 'undefined' ? window.location.origin : '/',
  },
  cache: {
    cacheLocation: 'sessionStorage', // This configures where your cache will be stored
    storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
  },
};

// Create the main instance of MSAL
export const msalInstance = new PublicClientApplication(msalConfig);

// Login request
export const loginRequest = {
  scopes: ['openid', 'profile'],
};