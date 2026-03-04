<template>
  <div :class="$style.page">
    <h1 :class="$style.title">Гардероб</h1>

    <div :class="$style.filter">
      <select v-model="selectedChildId" @change="loadClothes">
        <option :value="null">Все дети</option>
        <option v-for="child in childrenStore.children" :key="child.id" :value="child.id">
          {{ child.name }}
        </option>
      </select>
    </div>

    <div v-if="clothesStore.clothes.length === 0" :class="$style.empty">
      <p>Добавьте первую вещь</p>
    </div>

    <div v-else :class="$style.grid">
      <div v-for="item in clothesStore.clothes" :key="item.id" :class="$style.card">
        <img 
          :src="getImageUrl(item.photo)" 
          :class="$style.image"
          alt="Clothing"
        />
        <div :class="$style.cardBody">
          <h3>{{ item.name }}</h3>
          <p>Размер: {{ item.size }}</p>
          <span :class="[$style.status, $style[item.status]]">
            {{ item.status_display }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useChildrenStore } from '@/stores/children';
import { useClothesStore } from '@/stores/clothes';

const childrenStore = useChildrenStore();
const clothesStore = useClothesStore();

const selectedChildId = ref(null);

onMounted(async () => {
  await childrenStore.fetchChildren();
  loadClothes();
});

const loadClothes = () => {
  clothesStore.fetchClothes(selectedChildId.value);
};

const getImageUrl = (path) => {
  if (!path) return 'https://via.placeholder.com/100x100?text=Cloth';
  return `http://127.0.0.1:8000${path}`;
};
</script>

<style module>
.page {
  padding-bottom: 20px;
}

.title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  text-align: center;
}

.filter select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  background: white;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.image {
  width: 100%;
  height: 120px;
  object-fit: cover;
  background-color: #f0f0f0;
}

.cardBody {
  padding: 10px;
}

.cardBody h3 {
  font-size: 0.95rem;
  margin: 0 0 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cardBody p {
  font-size: 0.8rem;
  color: #666;
  margin: 0;
}

.status {
  display: inline-block;
  font-size: 0.7rem;
  padding: 3px 8px;
  border-radius: 12px;
  margin-top: 8px;
  background-color: #eee;
}

.status.wearing {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status.small {
  background-color: #fff3e0;
  color: #f57c00;
}

.status.sell_give {
  background-color: #e8f5e9;
  color: #388e3c;
}

.empty {
  text-align: center;
  margin-top: 3rem;
  color: #888;
}
</style>