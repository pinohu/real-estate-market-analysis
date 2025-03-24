import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface Property {
  id: number;
  title: string;
  address: string;
  price: number;
  type: string;
  status: string;
  bedrooms: number;
  bathrooms: number;
  squareFeet: number;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

export interface PropertyCreate {
  title: string;
  address: string;
  price: number;
  type: string;
  status: string;
  bedrooms: number;
  bathrooms: number;
  squareFeet: number;
  description?: string;
}

export interface PropertyUpdate extends Partial<PropertyCreate> {}

export interface PropertyFilters {
  type?: string;
  status?: string;
  minPrice?: number;
  maxPrice?: number;
  location?: string;
}

export const propertyApi = {
  // Get all properties with optional filters
  getProperties: async (filters?: PropertyFilters) => {
    const response = await api.get<Property[]>('/properties', { params: filters });
    return response.data;
  },

  // Get a single property by ID
  getProperty: async (id: number) => {
    const response = await api.get<Property>(`/properties/${id}`);
    return response.data;
  },

  // Create a new property
  createProperty: async (property: PropertyCreate) => {
    const response = await api.post<Property>('/properties', property);
    return response.data;
  },

  // Update an existing property
  updateProperty: async (id: number, property: PropertyUpdate) => {
    const response = await api.put<Property>(`/properties/${id}`, property);
    return response.data;
  },

  // Delete a property
  deleteProperty: async (id: number) => {
    await api.delete(`/properties/${id}`);
  },

  // Analyze a property
  analyzeProperty: async (id: number) => {
    const response = await api.post(`/properties/${id}/analyze`);
    return response.data;
  },

  // Get market analysis
  getMarketAnalysis: async (location: string, propertyType: string) => {
    const response = await api.get('/analysis/market', {
      params: { location, propertyType },
    });
    return response.data;
  },

  // Get investment opportunities
  getInvestmentOpportunities: async (filters?: PropertyFilters) => {
    const response = await api.get('/analysis/opportunities', {
      params: filters,
    });
    return response.data;
  },
};

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export const authApi = {
  // Login user
  login: async (credentials: LoginCredentials) => {
    const response = await api.post<AuthResponse>('/auth/login', credentials);
    return response.data;
  },

  // Register new user
  register: async (data: RegisterData) => {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },
};

export default api; 