<script setup>
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
</script>

<template>
  <h5 class="mt-5">Database Structure:</h5>
  <div class="row mt-3">
    <div class="col-md-4 pe-3 mb-4" v-for="(t, index) in tables">
      <div class="card border-primary shadow h-100">
        <div class="card-header">
          <font-awesome-icon :icon="['fas', 'table']"/>
        </div>
        <div class="card-body">
          <h4 class="card-title"> {{ t.name }}</h4>
          <div class="card-text">
            <font-awesome-icon :icon="['fas', 'table-columns']" class="text-muted"/>
            {{ t.columns.length }} columns:
            <p class="font-monospace">
              {{ t.columns.join(', ') }}
            </p>
            <font-awesome-icon :icon="['fas', 'bars']" class="text-muted"/> &nbsp;
            <a href="#" class="text-primary" data-bs-toggle="offcanvas" data-bs-target="#tableOffcanvas"
               @click="changeTableIndex(index)">
              {{ t.row_count }} rows&nbsp;
              <font-awesome-icon :icon="['fas', 'arrow-up-right-from-square']"/>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'DatabasePreview',
  props: {
    tables: {
      type: Array,
      required: true
    }
  },
  methods: {
    changeTableIndex(index) {
      this.$emit('change-index', index);
    }
  },
  emits: ['change-index'],
}
</script>
