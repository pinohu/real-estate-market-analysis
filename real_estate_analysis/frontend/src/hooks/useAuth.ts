import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
  });
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setAuthState({
        user: JSON.parse(localStorage.getItem('user') || 'null'),
        token,
        isAuthenticated: true,
      });
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post('/api/v1/auth/login', {
        username: email,
        password,
      });
      const { access_token } = response.data;
      const userResponse = await axios.get('/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${access_token}` },
      });
      const user = userResponse.data;

      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));

      setAuthState({
        user,
        token: access_token,
        isAuthenticated: true,
      });

      navigate('/properties');
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string, full_name: string) => {
    try {
      const response = await axios.post('/api/v1/auth/register', {
        email,
        password,
        full_name,
      });
      const user = response.data;

      // Auto login after registration
      await login(email, password);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setAuthState({
      user: null,
      token: null,
      isAuthenticated: false,
    });
    navigate('/login');
  };

  return {
    user: authState.user,
    isAuthenticated: authState.isAuthenticated,
    login,
    register,
    logout,
  };
}; 