// API origin. Dev: "" (Vite proxies /api → :8000). Prod: set VITE_API_URL
// to the backend origin (bare host is fine, https:// is prepended).
const RAW = import.meta.env.VITE_API_URL || "";
export const API_BASE =
  RAW && !RAW.includes("://") ? `https://${RAW}` : RAW.replace(/\/$/, "");
