import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';

export const useClothesStore = defineStore('clothes', () => {
  const clothes = ref([]);

  async function fetchClothes(childId = null) {
    try {
      let url = '/clothes/';
      if (childId) {
        url += `?child_id=${childId}`;
      }
      const response = await api.get(url);
      clothes.value = response.data;
    } catch (error) {
      console.error('Failed to fetch clothes:', error);
    }
  }

  return { clothes, fetchClothes };
});