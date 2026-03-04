<template>
  <div :class="$style.container">
    <div :class="$style.card">
      <h1 :class="$style.title">Детский Гардероб</h1>
      
      <form @submit.prevent="handleLogin">
        <div :class="$style.formGroup">
          <label>Логин</label>
          <input 
            v-model="username" 
            type="text" 
            placeholder="Введите логин"
            required
          />
        </div>
        
        <div :class="$style.formGroup">
          <label>Пароль</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="Введите пароль"
            required
          />
        </div>

        <div v-if="error" :class="$style.error">{{ error }}</div>

        <button type="submit" :class="$style.button">Войти</button>
      </form>

      <router-link to="/register" :class="$style.link">
        Нет аккаунта? Зарегистрироваться
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const userStore = useUserStore();

const username = ref('');
const password = ref('');
const error = ref('');

async function handleLogin() {
  error.value = '';
  try {
    await userStore.login({ 
      username: username.value, 
      password: password.value 
    });
    router.push('/');
  } catch (err) {
    error.value = 'Неверный логин или пароль';
  }
}
</script>

<style module>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.title {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.formGroup {
  margin-bottom: 1.2rem;
}

.formGroup label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-size: 0.9rem;
}

.formGroup input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.formGroup input:focus {
  outline: none;
  border-color: #42b883;
}

.button {
  width: 100%;
  padding: 0.9rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 0.5rem;
}

.button:hover {
  background-color: #3aa876;
}

.link {
  display: block;
  text-align: center;
  margin-top: 1.5rem;
  color: #42b883;
  text-decoration: none;
  font-size: 0.9rem;
}

.error {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  text-align: center;
}
</style>