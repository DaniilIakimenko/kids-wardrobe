<!-- src/layouts/MainLayout.vue -->
<template>
  <div :class="$style.layout">
    <main :class="$style.content">
      <router-view />
    </main>
    
    <nav :class="$style.navBar">
      <router-link 
        v-for="item in navItems" 
        :key="item.path" 
        :to="item.path"
        :class="[$style.navItem, route.path === item.path && $style.active]"
      >
        <component :is="item.icon" :class="$style.icon" />
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { h } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// Иконки вынесены отдельно. Используем обратные кавычки (`) для безопасности строк.

const HomeIcon = {
  render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
    h('path', { d: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z' }),
    h('polyline', { points: '9 22 9 12 15 12 15 22' })
  ])
};

const ChildIcon = {
  render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
    h('path', { d: `M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 
      7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z` })
  ])
};

const UserIcon = {
  render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
    h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }),
    h('circle', { cx: 12, cy: 7, r: 4 })
  ])
};

const navItems = [
  { path: '/wardrobe', label: 'Гардероб', icon: HomeIcon },
  { path: '/children', label: 'Дети', icon: ChildIcon },
  { path: '/profile', label: 'Профиль', icon: UserIcon },
];
</script>

<style module>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f9f9f9;
  padding-bottom: 70px;
}

.content {
  flex: 1;
  padding: 1rem;
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

.navBar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: white;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  z-index: 1000;
}

.navItem {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #999;
  font-size: 0.75rem;
  transition: color 0.2s;
}

.navItem.active {
  color: #42b883;
  font-weight: bold;
}

.icon {
  margin-bottom: 4px;
}
</style>