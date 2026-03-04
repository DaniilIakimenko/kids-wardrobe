import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '@/layouts/MainLayout.vue';

import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import Wardrobe from '@/views/Wardrobe.vue';
import Children from '@/views/Children.vue';
import Profile from '@/views/Profile.vue';

const routes = [
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/wardrobe'
      },
      {
        path: 'wardrobe',
        name: 'Wardrobe',
        component: Wardrobe
      },
      {
        path: 'children',
        name: 'Children',
        component: Children
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile // Заглушка
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guest: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  if (to.meta.requiresAuth && !token) {
    next('/login');
  }
  else if (to.meta.guest && token) {
    next('/');
  } 
  else {
    next();
  }
});

export default router;