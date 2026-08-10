import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { User, UserRole } from '../types/auth';

interface AuthStoreState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  activeRole: UserRole;
  login: (user: User, token: string) => Promise<void>;
  logout: () => Promise<void>;
  setActiveRole: (role: UserRole) => void;
  updateUser: (partial: Partial<User>) => void;
  loadAuth: () => Promise<void>;
}

const DEMO_USER: User = {
  id: 'usr_demo_123',
  name: 'Thaha Hussain',
  email: 'thaha@camcrew.in',
  phone: '+91 9876543210',
  role: 'customer',
  avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=400',
  createdAt: '2024-01-01',
};

export const useAuthStore = create<AuthStoreState>((set, get) => ({
  user: DEMO_USER,
  token: 'mock_jwt_token_camcrew',
  isAuthenticated: true,
  isLoading: false,
  activeRole: 'customer',

  login: async (user: User, token: string) => {
    set({ user, token, isAuthenticated: true, activeRole: user.role });
    await AsyncStorage.setItem('@camcrew_token', token);
    await AsyncStorage.setItem('@camcrew_user', JSON.stringify(user));
  },

  logout: async () => {
    set({ user: null, token: null, isAuthenticated: false, activeRole: 'customer' });
    await AsyncStorage.removeItem('@camcrew_token');
    await AsyncStorage.removeItem('@camcrew_user');
  },

  setActiveRole: (role: UserRole) => {
    set({ activeRole: role });
  },

  updateUser: (partial: Partial<User>) => {
    const current = get().user;
    if (current) {
      const updated = { ...current, ...partial };
      set({ user: updated });
      AsyncStorage.setItem('@camcrew_user', JSON.stringify(updated));
    }
  },

  loadAuth: async () => {
    try {
      const token = await AsyncStorage.getItem('@camcrew_token');
      const userStr = await AsyncStorage.getItem('@camcrew_user');
      if (token && userStr) {
        const user = JSON.parse(userStr);
        set({ token, user, isAuthenticated: true, activeRole: user.role });
      }
    } catch (e) {
      console.warn('Failed to load auth session');
    }
  },
}));
