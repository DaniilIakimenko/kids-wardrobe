<template>
  <div :class="$style.container">
    <h1>Профиль</h1>
    <div :class="$style.info">
      <p><strong>Пользователь:</strong> {{ userStore.user?.username }}</p>
      <p><strong>Email:</strong> {{ userStore.user?.email || 'Не указан' }}</p>
    </div>
    
    <button @click="logout" :class="$style.logoutBtn">
      Выйти из аккаунта
    </button>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();

const logout = () => {
  userStore.logout();
  router.push('/login');
};
</script>

<style module>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2rem;
}

.info {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  width: 100%;
  max-width: 300px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.info p {
  margin: 0.5rem 0;
  font-size: 1rem;
  color: #333;
}

.logoutBtn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.logoutBtn:hover {
  background-color: #e60000;
}
</style>