<template>
  <div class="auth-container">
    <h2>Регистрация</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="username" placeholder="Логин" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <input v-model="password2" type="password" placeholder="Повторите пароль" required />
      <button type="submit">Зарегистрироваться</button>
    </form>
    <router-link to="/login">Уже есть аккаунт? Войти</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();
const username = ref('');
const password = ref('');
const password2 = ref('');

async function handleRegister() {
  if (password.value !== password2.value) {
    alert('Пароли не совпадают');
    return;
  }
  try {
    await userStore.register({ 
      username: username.value, 
      password: password.value,
      password2: password2.value 
    });
    router.push('/');
  } catch (e) {
    alert('Ошибка регистрации');
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}
input {
  display: block;
  margin: 10px 0;
  padding: 8px;
}
</style>