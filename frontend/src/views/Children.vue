<template>
  <div :class="$style.page">
    <h1 :class="$style.title">Мои дети</h1>

    <div :class="$style.list">
      <div v-for="child in childrenStore.children" :key="child.id" :class="$style.card">
        <img 
          :src="getImageUrl(child.avatar)" 
          :class="$style.avatar"
          alt="Avatar"
        />
        <div :class="$style.info">
          <h3>{{ child.name }}</h3>
          <p>{{ calculateAge(child.birth_date) }}</p>
        </div>
      </div>
      
      <button @click="showModal = true" :class="$style.addButton">
        + Добавить ребенка
      </button>
    </div>

    <div v-if="showModal" :class="$style.modalOverlay" @click.self="closeModal">
      <div :class="$style.modal">
        <h2>Новый ребенок</h2>
        <form @submit.prevent="handleSubmit">
          <div :class="$style.formGroup">
            <label>Имя</label>
            <input v-model="form.name" type="text" required />
          </div>

          <div :class="$style.formGroup">
            <label>Дата рождения</label>
            <input v-model="form.birth_date" type="date" required />
          </div>

          <div :class="$style.formGroup">
            <label>Пол</label>
            <select v-model="form.gender" required>
              <option value="boy">Мальчик</option>
              <option value="girl">Девочка</option>
            </select>
          </div>

          <div :class="$style.formGroup">
            <label>Фото</label>
            <input type="file" @change="handleFileChange" accept="image/*" />
            <div v-if="previewImage" :class="$style.preview">
              <img :src="previewImage" alt="Preview" />
            </div>
          </div>

          <div :class="$style.actions">
            <button type="button" @click="closeModal" :class="$style.cancelBtn">Отмена</button>
            <button type="submit" :class="$style.submitBtn">Сохранить</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useChildrenStore } from '@/stores/children';

const childrenStore = useChildrenStore();

onMounted(() => {
  childrenStore.fetchChildren();
});

const showModal = ref(false);
const previewImage = ref(null);
const form = ref({
  name: '',
  birth_date: '',
  gender: 'boy',
  avatar: null
});

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    form.value.avatar = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const handleSubmit = async () => {
  try {
    await childrenStore.addChild(form.value);
    closeModal();
  } catch (e) {
    alert('Ошибка при сохранении');
  }
};

const closeModal = () => {
  showModal.value = false;
  previewImage.value = null;
  form.value = { name: '', birth_date: '', gender: 'boy', avatar: null };
};

const calculateAge = (birthDate) => {
  const today = new Date();
  const birth = new Date(birthDate);
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  return `${age} лет`;
};

const getImageUrl = (path) => {
  if (!path) return 'https://via.placeholder.com/80x80?text=No+Photo';

  if (path.startsWith('http')) return path;
  
  return path; 
};
</script>

<style module>
.page {
  padding-bottom: 20px;
}

.title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #333;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  gap: 15px;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  background-color: #eee;
}

.info h3 {
  margin: 0;
  font-size: 1.1rem;
}

.info p {
  margin: 5px 0 0;
  color: #666;
  font-size: 0.9rem;
}

.addButton {
  width: 100%;
  padding: 15px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.addButton:hover {
  background-color: #3aa876;
}

/* Modal Styles */
.modalOverlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  width: 90%;
  max-width: 400px;
  box-sizing: border-box;
}

.formGroup {
  margin-bottom: 1rem;
}

.formGroup label {
  display: block;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
  color: #555;
}

.formGroup input, .formGroup select {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.preview {
  margin-top: 10px;
  text-align: center;
}

.preview img {
  max-width: 100px;
  max-height: 100px;
  border-radius: 8px;
  object-fit: cover;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.cancelBtn, .submitBtn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

.cancelBtn {
  background: #eee;
  color: #333;
}

.submitBtn {
  background: #42b883;
  color: white;
}
</style>