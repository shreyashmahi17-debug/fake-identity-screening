/**
 * Backend configuration with automatic fallback
 * Works without any environment variable setup
 */

export const getBackendUrl = () => {
  // Priority:
  // 1. Build-time env variable (if set in Vercel)
  // 2. Runtime global (from config.js)
  // 3. Hardcoded fallback (always works)
  
  const backendUrl = import.meta.env.VITE_API_URL || 
                     (typeof window !== 'undefined' && window.VITE_API_URL) || 
                     "https://fake-identity-screening.onrender.com";
  
  console.log("🔧 Backend URL:", backendUrl);
  
  return backendUrl;
};

export const API_CONFIG = {
  timeout: 120000, // 120 seconds for cold start
  retries: 3,
  retryDelay: 2000,
};
