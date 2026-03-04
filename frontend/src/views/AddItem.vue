<template>
  <div :class="$style.container">
    <div :class="$style.header">
      <button @click="router.back()" :class="$style.backBtn">←</button>
      <h2>{{ isEdit ? 'Редактировать' : 'Новая вещь' }}</h2>
    </div>

    <form @submit.prevent="handleSubmit">
      <div :class="$style.photoSection" @click="triggerFileInput">
        <img v-if="previewImage" :src="previewImage" :class="$style.preview" />
        <div v-else :class="$style.placeholder">
          <span>+</span>
          <p>Добавить фото</p>
        </div>
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileChange" 
          accept="image/*" 
          capture="environment" 
          hidden 
        />
      </div>

      <div :class="$style.formGroup">
        <label>Название *</label>
        <input v-model="form.name" type="text" placeholder="Например: Синяя куртка" required />
      </div>

      <div :class="$style.row">
        <div :class="$style.formGroup">
          <label>Ребенок *</label>
          <select v-model="form.child" required>
            <option v-for="child in childrenStore.children" :key="child.id" :value="child.id">
              {{ child.name }}
            </option>
          </select>
        </div>
        <div :class="$style.formGroup">
          <label>Размер (рост) *</label>
          <input v-model="form.size" type="text" placeholder="98" required />
        </div>
      </div>

      <div :class="$style.formGroup">
        <label>Категория *</label>
        <select v-model="form.category" required>
          <option v-for="cat in clothesStore.categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>

      <div :class="$style.row">
        <div :class="$style.formGroup">
          <label>Сезон</label>
          <select v-model="form.season">
            <option value="winter">Зима</option>
            <option value="summer">Лето</option>
            <option value="demi">Деми</option>
            <option value="all_season">Всесезон</option>
          </select>
        </div>
        <div :class="$style.formGroup">
          <label>Состояние</label>
          <select v-model="form.condition">
            <option value="new">Новое</option>
            <option value="excellent">Отличное</option>
            <option value="used">Б/у</option>
          </select>
        </div>
      </div>

      <div :class="$style.formGroup">
        <label>Статус</label>
        <select v-model="form.status">
          <option value="wearing">Носим</option>
          <option value="small">Мало</option>
          <option value="sell_give">Продать/Отдать</option>
        </select>
      </div>

      <div :class="$style.formGroup">
        <label>Цена покупки</label>
        <input v-model="form.purchase_price" type="number" placeholder="0.00" step="0.01" />
      </div>

      <div :class="$style.formGroup">
        <label>Примечания</label>
        <textarea v-model="form.notes" rows="2" placeholder="Пятно на рукаве, подарок от бабушки..."></textarea>
      </div>

      <div :class="$style.actions">
        <button type="button" @click="router.back()" :class="$style.cancelBtn">Отмена</button>
        <button type="submit" :class="$style.saveBtn">{{ isEdit ? 'Обновить' : 'Сохранить' }}</button>
      </div>
      
      <button v-if="isEdit" @click="handleDelete" type="button" :class="$style.deleteBtn">
        Удалить вещь
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useChildrenStore } from '@/stores/children';
import { useClothesStore } from '@/stores/clothes';

const route = useRoute();
const router = useRouter();
const childrenStore = useChildrenStore();
const clothesStore = useClothesStore();

const itemId = computed(() => route.params.id);
const isEdit = computed(() => !!itemId.value);

const fileInput = ref(null);
const previewImage = ref(null);
const form = ref({
  name: '',
  child: '',
  category: '',
  size: '',
  season: 'demi',
  condition: 'new',
  status: 'wearing',
  purchase_price: '',
  notes: '',
  photo: null
});

onMounted(async () => {
  await childrenStore.fetchChildren();
  await clothesStore.fetchCategories();

  if (isEdit.value) {
    const item = await clothesStore.fetchItem(itemId.value);
    if (item) {
      form.value = { ...item, photo: null };
      if (typeof item.child === 'object') form.value.child = item.child.id;
      if (typeof item.category === 'object') form.value.category = item.category.id;
      
      previewImage.value = item.photo ? item.photo : null;
    }
  } else {
    if (childrenStore.children.length > 0) {
      form.value.child = childrenStore.children[0].id;
    }
    if (clothesStore.categories.length > 0) {
      form.value.category = clothesStore.categories[0].id;
    }
  }
});

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    form.value.photo = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await clothesStore.updateClothingItem(itemId.value, form.value);
    } else {
      await clothesStore.addClothingItem(form.value);
    }
    router.push('/wardrobe');
  } catch (error) {
    alert('Ошибка при сохранении. Проверьте поля.');
  }
};

const handleDelete = async () => {
  if (confirm('Вы уверены, что хотите удалить вещь?')) {
    await clothesStore.deleteClothingItem(itemId.value);
    router.push('/wardrobe');
  }
};
</script>

<style module>
.container {
  padding: 1rem;
  padding-bottom: 2rem;
  background: white;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.backBtn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding-right: 15px;
  color: #333;
}

.header h2 {
  margin: 0;
  font-size: 1.2rem;
}

.photoSection {
  width: 100%;
  height: 200px;
  background-color: #f0f0f0;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px dashed #ccc;
}

.preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  text-align: center;
  color: #888;
}

.placeholder span {
  font-size: 3rem;
  font-weight: bold;
  display: block;
  line-height: 1;
}

.formGroup {
  margin-bottom: 1rem;
}

.formGroup label {
  display: block;
  font-size: 0.85rem;
  color: #555;
  margin-bottom: 0.3rem;
  font-weight: 500;
}

.formGroup input, .formGroup select, .formGroup textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  background: #fafafa;
}

.row {
  display: flex;
  gap: 1rem;
}

.row .formGroup {
  flex: 1;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.cancelBtn, .saveBtn {
  flex: 1;
  padding: 14px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  border: none;
}

.cancelBtn {
  background: #eee;
  color: #333;
}

.saveBtn {
  background: #42b883;
  color: white;
}

.deleteBtn {
  width: 100%;
  margin-top: 1rem;
  background: none;
  border: 1px solid #ff4d4d;
  color: #ff4d4d;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
}
</style>