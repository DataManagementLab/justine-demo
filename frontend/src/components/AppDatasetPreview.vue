<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>

<script>
export default {
  props: {
    id: Number,
    title: String,
    description: String,
    table_count: Number,
    tables: Array,
    num_inserts: Number,
  }
}
</script>

<template>
  <div class="col-md-3 pe-3 mb-5">
    <div class="card bg-primary text-white h-100">
      <div class="card-header"><font-awesome-icon :icon="['far', 'folder-open']" /></div>
      <div class="card-body">
        <h4 class="card-title">{{ title }}</h4>
        <p class="card-text">{{ description }}</p>

        <font-awesome-icon :icon="['fas', 'table']" /> {{ table_count }} tables:
            <p class="font-monospace">
              {{ tables.join(', ') }}
            </p>

        <font-awesome-icon :icon="['fas', 'arrow-right-to-bracket']" /> {{ num_inserts }} inserts
      </div>
        <div class="card-footer text-center">
          <router-link :to="{ name: 'interactive', params: { id: id }}" class="btn bg-white text-primary"><font-awesome-icon :icon="['fas', 'user-pen']" /></router-link>&nbsp;
          <router-link :to="{ name: 'batch', params: { id: id }}" class="btn bg-white text-primary"><font-awesome-icon :icon="['fas', 'play']" /></router-link>
        </div>

    </div>
  </div>

</template>
