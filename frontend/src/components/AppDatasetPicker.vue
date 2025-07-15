<script setup>
import DatasetPreview from './AppDatasetPreview.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>

<script>
export default {
  props: {
    datasets: Array
  },
  computed: {
    datasets_sorted() {
      if (!this.datasets) return []

      let sorted = this.datasets
      return sorted.sort((a, b) => {
        if (this.sortBy === 'name') {
          return (a.name > b.name ? 1 : -1) * this.asc
        }
        else if (this.sortBy === 'Table Count') {
          return (a.table_count - b.table_count) * this.asc
        }
        else
          return (a.num_inserts - b.num_inserts) * this.asc
      })
    }
  },
  data() {
    return {
      sortBy: 'Name',
      asc: 1,
    }
  }
}
</script>

<template>
  <div class="float-end">
    Sort by&nbsp;
    <div class="btn-group" role="group">
      <button type="button" class="btn btn-success">{{ sortBy }}</button>
      <div class="btn-group" role="group">
        <button id="btnGroupDrop1" type="button" class="btn btn-success dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>
        <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
          <a class="dropdown-item" @click="sortBy='Name'" href="#">Name</a>
          <a class="dropdown-item" @click="sortBy='Table Count'" href="#">Table Count</a>
          <a class="dropdown-item" @click="sortBy='Insert Count'" href="#">Insert Count</a>
        </div>
      </div>
    </div>
    &nbsp;
  <button class="btn btn-success" @click="asc *= -1">{{ asc === 1 ? 'ASC' : 'DESC' }}</button>
  </div>

  <h2><font-awesome-icon :icon="['fas', 'cubes-stacked']" /> Databases &amp; Workloads</h2>

  <div class="row mt-4">
    <!-- Interactive mode with empty databse -->
    <div class="col-md-3 pe-3 mb-5">
    <div class="card bg-success text-white h-100">
      <div class="card-header"><font-awesome-icon :icon="['fas', 'plus']" /></div>
        <div class="card-body">
          <h4 class="card-title">Empty Database</h4>
          <p class="card-text">Start with an empty database</p>
        </div>
        <div class="card-footer text-center">
          <router-link :to="{ name: 'interactive_empty'}" class="btn bg-white text-success"><font-awesome-icon :icon="['fas', 'user-pen']" /></router-link>&nbsp;
        </div>
      </div>
    </div>

    <!-- One card per database/workload -->
    <DatasetPreview
      v-for="ds in datasets_sorted"
      :id="ds.id"
      :title="ds.name"
      :description="ds.description"
      :table_count="ds.table_count"
      :tables="ds.tables"
      :num_inserts="ds.num_inserts"
    />
  </div>
</template>
