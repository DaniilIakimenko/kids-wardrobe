<template>
  <div class="home-container">
    <h1>Добро пожаловать в Детский Гардероб!</h1>
    <p>Вы успешно авторизованы.</p>
    <button @click="logout">Выйти</button>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();

function logout() {
  userStore.logout();
  router.push('/login');
}
</script>

<style scoped>
.home-container {
  padding: 2rem;
  text-align: center;
}
button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>