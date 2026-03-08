<template>
  <div :class="$style.container">
    <div :class="$style.card">
      <h1 :class="$style.title">Детский Гардероб</h1>
      
      <form @submit.prevent="handleRegister">
        <div :class="$style.formGroup">
          <label>Логин</label>
          <input 
            v-model="username" 
            type="text" 
            placeholder="Придумайте логин"
            required
          />
        </div>
        
        <div :class="$style.formGroup">
          <label>Пароль</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="Минимум 6 символов"
            required
          />
        </div>

        <div :class="$style.formGroup">
          <label>Повторите пароль</label>
          <input 
            v-model="password2" 
            type="password" 
            placeholder="Повторите пароль"
            required
          />
        </div>

        <div v-if="error" :class="$style.error">{{ error }}</div>

        <button type="submit" :class="$style.button">Зарегистрироваться</button>
      </form>

      <router-link to="/login" :class="$style.link">
        Уже есть аккаунт? Войти
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
const password2 = ref('');
const error = ref('');

async function handleRegister() {
  // Проверка на клиенте перед отправкой
  if (password.value !== password2.value) {
    error.value = 'Пароли не совпадают';
    return;
  }

  error.value = '';
  
  try {
    // Вызываем action регистрации из Pinia store
    await userStore.register({ 
      username: username.value, 
      password: password.value,
      password2: password2.value 
    });
    
    // Если успешно, пушим на главную
    router.push('/');
  } catch (err) {
    // Обработка ошибок от бэкенда
    const data = err.response?.data;
    if (data) {
      // Собираем все ошибки в одну строку
      const messages = Object.values(data).flat().join(' ');
      error.value = messages;
    } else {
      error.value = 'Ошибка регистрации. Попробуйте позже.';
    }
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
  box-sizing: border-box;
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
  background-color: #fdf0f0;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #f5c6cb;
}
</style>