<script setup>
import Header from "../../components/AppHeader.vue";
import DatasetPicker from "../../components/AppDatasetPicker.vue";
import Footer from "../../components/AppFooter.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
</script>

<script>
export default {
  components: {
  },

  data() {
    return {
      datasets: null,
      runs: null,
      datasets_by_id: {},
    }
  },

  watch: {
    datasets() {
      this.datasets_by_id = this.datasets.reduce((acc, dataset) => {
        acc[dataset.id] = dataset.name
        return acc
      }, {})
    }
  },

  methods: {
    async loadDatasets() {
      this.datasets = null
      const res = await fetch('http://localhost:8000/datasets/')
      this.datasets = await res.json()
    },
    async loadRunList() {
      this.runs = null
      const res = await fetch('http://localhost:8000/runs/')
      this.runs = await res.json()
    }
  },

  mounted() {
    this.loadDatasets()
    this.loadRunList()
  },
};
</script>


<template>
  <div class="container py-4 px-3 mx-auto">
    <Header />

    <div class="col-lg-8 px-0">
      <p class="fs-4">Welcome to our demo. Interact live with one of our sample databases or (re-)watch batch insertions</p>
    </div>

    <hr class="col-1 my-5 mx-0">

    <DatasetPicker :datasets="datasets" />

    <hr class="col-1 my-5 mx-0">

    <h2><font-awesome-icon :icon="['fas', 'circle-play']" /> Replay previous runs</h2>

    <div v-if="runs">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Dataset</th>
            <th>Settings</th>
            <th>Num Iterations</th>
            <th>Replay</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="run in runs" :key="run.id">
            <td>{{ datasets_by_id[run.dataset] }}</td>
            <td>
              <font-awesome-icon :icon="['fas', 'table']" class="text-muted" /> {{ run.missingTableNames }} %&nbsp;
              <font-awesome-icon :icon="['fas', 'table-columns']" class="text-muted" /> {{ run.missingColumnNames }} %&nbsp;
            </td>
            <td>
              {{ run.num_iterations }}
            </td>
            <td>
              <router-link :to="{ name: 'play', params: { mode: 'replay' }, query: { id: run.id }}">
              <font-awesome-icon :icon="['fas', 'circle-play']" />
            </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>

    <Footer />
  </div>
</template>

<style scoped>

</style>
