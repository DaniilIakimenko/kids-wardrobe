import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || null);
  const user = ref(null);

  async function login(credentials) {
    try {
      const response = await api.post('/token/', credentials);
      token.value = response.data.access;
      localStorage.setItem('token', response.data.access);
      
      await fetchUser();
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  }

  async function register(credentials) {
    try {
      await api.post('/register/', credentials);
      return await login(credentials);
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  }

  async function fetchUser() {
    if (!token.value) return;
    try {
      const response = await api.get('/me/');
      user.value = response.data;
    } catch (error) {
      logout();
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
  }

  return { token, user, login, register, fetchUser, logout };
});