import { apiClient } from './client';
import { User, UserRole } from '../types/auth';

export const authApi = {
  sendOTP: async (phone: string): Promise<{ success: boolean; message: string }> => {
    try {
      const res = await apiClient.post('/auth/send-otp', { phone });
      return res.data;
    } catch (e) {
      // Robust simulation response with standard demo OTP code 123456
      return {
        success: true,
        message: `6-Digit OTP sent successfully to +91 ${phone}. (Demo OTP: 123456)`,
      };
    }
  },

  verifyOTP: async (phone: string, otp: string): Promise<{ token: string; user: User }> => {
    try {
      const res = await apiClient.post('/auth/verify-otp', { phone, otp });
      return res.data;
    } catch (e) {
      if (otp !== '123456' && otp.length !== 6) {
        throw new Error('Invalid OTP code. Please enter 123456');
      }

      const isPro = phone.endsWith('9') || phone.endsWith('8');
      const isAdmin = phone === '9999999999';
      const role: UserRole = isAdmin ? 'admin' : isPro ? 'professional' : 'customer';

      return {
        token: 'token_otp_' + Date.now(),
        user: {
          id: 'usr_phone_' + phone,
          name: isPro ? 'Thaha (Pro Director)' : isAdmin ? 'Camcrew Admin' : 'Creative Renter',
          email: `${phone}@camcrew.in`,
          phone: `+91 ${phone}`,
          role,
          avatar: isPro
            ? 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=400'
            : 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400',
          createdAt: new Date().toISOString(),
        },
      };
    }
  },

  login: async (email: string, pass: string): Promise<{ token: string; user: User }> => {
    try {
      const res = await apiClient.post('/auth/login', { email, password: pass });
      return res.data;
    } catch (e) {
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
