// API configuration - points to FastAPI backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = {
  projects: {
    list: {
      path: `${API_BASE_URL}/api/projects`,
    },
    create: {
      path: `${API_BASE_URL}/api/projects`,
    },
  },
  skills: {
    list: {
      path: `${API_BASE_URL}/api/skills`,
    },
  },
  messages: {
    create: {
      path: `${API_BASE_URL}/api/messages`,
    },
  },
};

export default api;
