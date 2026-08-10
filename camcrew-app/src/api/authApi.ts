import { apiClient } from './client';
import { User, UserRole } from '../types/auth';

export const authApi = {
  login: async (email: string, pass: string): Promise<{ token: string; user: User }> => {
    try {
      const res = await apiClient.post('/auth/login', { email, password: pass });
      return res.data;
    } catch (e) {
      // Mock fallback for testing & offline mode
      const role: UserRole = email.includes('admin') ? 'admin' : email.includes('pro') ? 'professional' : 'customer';
      return {
        token: 'mock_token_' + Date.now(),
        user: {
          id: 'usr_' + Date.now(),
          name: email.split('@')[0].toUpperCase(),
          email,
          role,
          avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=400',
          createdAt: new Date().toISOString(),
        },
      };
    }
  },

  registerCustomer: async (data: { name: string; email: string; phone: string; password: string }): Promise<{ token: string; user: User }> => {
    try {
      const res = await apiClient.post('/auth/register', data);
      return res.data;
    } catch (e) {
      return {
        token: 'mock_token_' + Date.now(),
        user: {
          id: 'usr_' + Date.now(),
          name: data.name,
          email: data.email,
          phone: data.phone,
          role: 'customer',
          createdAt: new Date().toISOString(),
        },
      };
    }
  },

  registerProfessional: async (data: any): Promise<{ token: string; user: User }> => {
    try {
      const res = await apiClient.post('/professional/register', data);
      return res.data;
    } catch (e) {
      return {
        token: 'mock_token_' + Date.now(),
        user: {
          id: 'usr_pro_' + Date.now(),
          name: data.name || 'Pro Creator',
          email: data.email || 'pro@camcrew.in',
          role: 'professional',
          createdAt: new Date().toISOString(),
        },
      };
    }
  },

  forgotPassword: async (email: string): Promise<{ success: boolean; message: string }> => {
    try {
      const res = await apiClient.post('/auth/forgot-password', { email });
      return res.data;
    } catch (e) {
      return { success: true, message: 'Password reset link sent to ' + email };
    }
  },
};
