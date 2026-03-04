import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';

export const useChildrenStore = defineStore('children', () => {
  const children = ref([]);
  const currentChild = ref(null);

  async function fetchChildren() {
    try {
      const response = await api.get('/children/');
      children.value = response.data;
      
      if (children.value.length > 0 && !currentChild.value) {
        currentChild.value = children.value[0];
      }
    } catch (error) {
      console.error('Failed to fetch children:', error);
    }
  }

  async function addChild(data) {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('birth_date', data.birth_date);
    formData.append('gender', data.gender);
    
    if (data.avatar && data.avatar instanceof File) {
      formData.append('avatar', data.avatar);
    }

    try {
      const response = await api.post('/children/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      children.value.push(response.data);
      return true;
    } catch (error) {
      console.error('Failed to add child:', error);
      throw error;
    }
  }

  async function deleteChild(id) {
    try {
      await api.delete(`/children/${id}/`);
      children.value = children.value.filter(c => c.id !== id);
      if (currentChild.value && currentChild.value.id === id) {
        currentChild.value = children.value[0] || null;
      }
    } catch (error) {
      console.error('Failed to delete child:', error);
    }
  }

  function setCurrentChild(child) {
    currentChild.value = child;
  }

  return { children, currentChild, fetchChildren, addChild, deleteChild, setCurrentChild };
});