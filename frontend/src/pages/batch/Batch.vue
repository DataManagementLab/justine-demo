<script setup>
import Header from "../../components/AppHeader.vue";
import Footer from "../../components/AppFooter.vue";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>

<script>
export default {
  computed: {
    dataset() {
      return this.$route.params.id;
    },
    query() {
      // Create a dict of all parameters that need to be encoded
      return {
        missingTableNames: this.missingTableNames,
        missingColumnNames: this.missingColumnNames,
        tableSynonyms: this.tableSynonyms,
        columnsSynonyms: this.columnsSynonyms,
        startWithSchema: this.startWithSchema,
        fixSchema: this.fixSchema,
        dataset: this.dataset,
      }
    }
  },

  methods: {
    run() {
      // Change to play view in live mode passing the selected params
      this.$router.push({ name: 'play', params: { mode: 'live' }, query: this.query });
    },
    update() {
      // Update the URL after every change of params to make sure their state is preserved when using the browser navigation
      this.$router.replace({ query: this.query });
    },
    async loadDatasetDetails() {
      this.datasetDetails = null
      const res = await fetch('http://localhost:8000/datasets/' + this.dataset)
      this.datasetDetails = await res.json()
    }
  },

  data() {
    return {
      // Restore slider values from URL (if present) or use default values
      missingTableNames: this.$route.query && "missingTableNames" in this.$route.query ? this.$route.query.missingTableNames : 50,
      missingColumnNames: this.$route.query && "missingColumnNames" in this.$route.query ? this.$route.query.missingColumnNames : 20,
      tableSynonyms: this.$route.query && "tableSynonyms" in this.$route.query ? this.$route.query.tableSynonyms : 0,
      columnsSynonyms: this.$route.query && "columnsSynonyms" in this.$route.query ? this.$route.query.columnsSynonyms : 0,
      startWithSchema: this.$route.query && "startWithSchema" in this.$route.query ? this.$route.query.startWithSchema : false,
      fixSchema: this.$route.query && "fixSchema" in this.$route.query ? this.$route.query.fixSchema : false,
      datasetDetails: null,
    };
  },

  mounted() {
    this.loadDatasetDetails()
  },
};
</script>

<template>
  <div class="container py-4 px-3 mx-auto">
    <Header />

    <p>Modify settings for this batch run:</p>

    <form class="mt-3">
        <fieldset>
          <legend>Info</legend>

          <div class="row">
            <div class="col-md-5 ms-2">
              <table class="table">
                <tr>
                  <td>Dataset:</td>
                  <td>{{ datasetDetails ? datasetDetails.name : 'Loading...' }}</td>
                </tr>
                  <tr>
                    <td>Description:</td>
                    <td>{{ datasetDetails ? datasetDetails.description : '' }}</td>
                  </tr>
              </table>
            </div>
          </div>
        </fieldset>

        <fieldset class="mt-3">
          <legend>Modify batch settings</legend>
          <div class="row mb-3">
            <label for="missingTableNames" class="form-label col-md-3">{{ missingTableNames }} % table names missing</label>
            <input type="range" class="form-range col-md-3" min="0" max="100" step="10" id="missingTableNames" v-model="missingTableNames" @change="update" />
          </div>

          <div class="row mb-3">
            <label for="missingColumnNames" class="form-label col-md-3">{{ missingColumnNames }} % column names missing</label>
            <input type="range" class="form-range col-md-3" min="0" max="100" step="10" id="missingColumnNames" v-model="missingColumnNames" @change="update" />
          </div>

          <div class="row mb-3">
            <label for="tableSynonyms" class="form-label col-md-3">{{ tableSynonyms }} % table synonyms</label>
            <input type="range" class="form-range col-md-3" min="0" max="100" step="10" id="tableSynonyms" v-model="tableSynonyms" @change="update" />
          </div>

          <div class="row mb-3">
            <label for="columnSynonyms" class="form-label col-md-3">{{ columnsSynonyms }} % column synonyms</label>
            <input type="range" class="form-range col-md-3" min="0" max="100" step="10" id="columnSynonyms" v-model="columnsSynonyms" @change="update" />
          </div>

          <div class="row mb-3">
            <label for="startWithSchema" class="form-label col-md-3">Start with schema?</label>
            <input type="checkbox" class="col-md-3" id="startWithSchema" v-model="startWithSchema" @change="update" />
          </div>

          <div class="row mb-3">
            <label for="fixSchema" class="form-label col-md-3">Fix schema?</label>
            <input type="checkbox" class="col-md-3" id="fixSchema" v-model="fixSchema" @change="update" />
          </div>
        </fieldset>
        <div class="row mt-3">
          <button @click="run" class="btn btn-primary col-md-6 ms-2"><font-awesome-icon :icon="['fas', 'play']" /> Run</button>
        </div>
    </form>

    <Footer />
  </div>
</template>

<style scoped>

</style>
