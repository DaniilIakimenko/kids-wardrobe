import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';

export const useClothesStore = defineStore('clothes', () => {
  const clothes = ref([]);
  const categories = ref([]);

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

  async function fetchCategories() {
    try {
      const response = await api.get('/categories/');
      categories.value = response.data;
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  }

  async function fetchItem(id) {
    try {
      const response = await api.get(`/clothes/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch item:', error);
      return null;
    }
  }

  async function addClothingItem(data) {
    const formData = new FormData();

    formData.append('child', data.child);
    formData.append('category', data.category);
    formData.append('name', data.name);
    formData.append('size', data.size);
    formData.append('season', data.season);
    formData.append('condition', data.condition);
    formData.append('status', data.status);
    
    if (data.notes) formData.append('notes', data.notes);
    if (data.purchase_price) formData.append('purchase_price', data.purchase_price);
    
    if (data.photo && data.photo instanceof File) {
      formData.append('photo', data.photo);
    }

    try {
      const response = await api.post('/clothes/', formData);
      clothes.value.unshift(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to add item:', error);
      throw error;
    }
  }

  async function updateClothingItem(id, data) {
    const formData = new FormData();
    
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined && data[key] !== '') {
         if (key === 'photo') {
           if (data[key] instanceof File) {
             formData.append(key, data[key]);
           }
         } else {
           formData.append(key, data[key]);
         }
      }
    });

    try {
      const response = await api.patch(`/clothes/${id}/`, formData);
      const index = clothes.value.findIndex(c => c.id === id);
      if (index !== -1) clothes.value[index] = response.data;
      return response.data;
    } catch (error) {
      console.error('Failed to update item:', error);
      throw error;
    }
  }

  async function deleteClothingItem(id) {
    try {
      await api.delete(`/clothes/${id}/`);
      clothes.value = clothes.value.filter(c => c.id !== id);
    } catch (error) {
      console.error('Failed to delete item:', error);
    }
  }

  return { 
    clothes, categories, 
    fetchClothes, fetchCategories, fetchItem,
    addClothingItem, updateClothingItem, deleteClothingItem 
  };
});