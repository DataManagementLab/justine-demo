<script setup>
import Header from "../../components/AppHeader.vue";
import Footer from "../../components/AppFooter.vue";
import hljs from 'highlight.js/lib/core';
import sql from 'highlight.js/lib/languages/sql';
import TablePreviewSidebar from "../../components/TablePreviewSidebar.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import ConfigDetail from "../../components/ConfigDetail.vue";
import DatabasePreview from "../../components/DatabasePreview.vue";
import Query from "../../components/Query.vue";
import QueryHistoryOffcanvas from "../../components/QueryHistoryOffcanvas.vue";

hljs.registerLanguage('sql', sql);
</script>

<script>
export default {
  components: {
  },

  computed: {
    empty() {
      return !("id" in this.$route.params) || this.$route.params.id === '';
    },
    db_id() {
      return !this.empty ? this.$route.params.id : ''
    },
    selected_table() {
      // Select which table will be previewed in offcanvas sidebar
      if (this.selected_table_index === -1 || this.state === null) {
        return null
      }
      return this.state.tables[this.selected_table_index]
    },
  },

  methods: {
    async startInteraction() {
      // Create a new run on the server
      this.interaction_id = null
      console.log(this.db_id)
      let url = 'http://localhost:8000/interaction/'
      if (!this.empty) {
        url += '?database_id=' + this.db_id
      }
      const res = await fetch(url, {
            method: 'POST',
            headers: {"Content-Type": "application/json"}
          }
      )
      this.interaction_details = await res.json()
    },
    async load_state() {
        const res = await fetch('http://localhost:8000/interaction/' + this.interaction_id + '/state/')
        this.state = await res.json()
    },
    async add_queries() {
      // TODO Visualize that API call is being processed
      const res = await fetch('http://localhost:8000/interaction/' + this.interaction_id + '/add-queries/', {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({'queries': this.input_queries})
          }
      )
      this.input_queries = ''
      this.server_response = await res.json()
    }
  },

  watch : {
    interaction_details() {
      // Wait for interaction setup on the server and load initial database state once everything is ready
      this.interaction_id = this.interaction_details.id
      this.load_state()
    },
    server_response() {
      // Load new database state after query execution
      if (this.server_response !== null) {
        this.last_query = this.server_response.query
        this.adjusted_query = this.server_response.adjusted_query
        this.input_queries = ''
        this.load_state()
      }
    },
  },

  mounted() {
    this.startInteraction()
  },

  beforeRouteLeave(to, from) {

  },

  data() {
    return {
      interaction_id: null,
      interaction_details: null,
      selected_table_index: -1,
      state: null,
      last_queries: null,
      last_query: null,
      adjusted_query: null,
      input_queries: null,
      server_response: null,
    };
  },
};
</script>

<template>
  <div class="container py-4 px-3 mx-auto">
    <Header />

    <div v-if="interaction_details">
      <div class="row mt-3 mb-4 p-2">
        <ConfigDetail name="Database" :value="interaction_details.db" />
        <ConfigDetail name="Number of Tables" v-if="state" :value="state.tables.length" />
      </div>

      <div id="newQuery">
        <label for="query">Query:</label>
        <textarea v-model="input_queries" id="queryInput" name="query" class="w-100 font-monospace"></textarea>

        <div class="row mt-2">
          <div class="col-3"></div>
          <div class="col-6 text-center">
            <button class="btn btn-primary btn-lg" @click="add_queries">Insert</button>
          </div>
          <div class="col-3 text-end">
            <a href="#" class="text-dark text-decoration-none" data-bs-toggle="offcanvas" data-bs-target="#queryOffcanvas">
              View Query History <font-awesome-icon :icon="['fas', 'arrow-rotate-right']" />
            </a>
          </div>
        </div>
      </div>

      <div id="queryFeedback" v-if="last_query">
        <h5 class="mt-5">Last Query:</h5>
      <div class="queryBox">
        <Query :query="last_query" />
      </div>
      <div class="text-center text-large mt-2 mb-2">
        <h2><font-awesome-icon :icon="['fas', 'circle-down']" /></h2>
      </div>
      <div class="queryBox">
        <Query :query="adjusted_query" />
      </div>
        <!--
        <Query :query="'INSERT INTO table VALUES(a, b, c);'" />

        <h6 class="mt-4">Insert into:</h6>

        <div class="row mb-0 p-2">
          <div class="col-3 shadow p-0 me-4 ms-auto">
            <div class="border-start border-5 border-primary p-3 h-100">
              <h4 class="m-0">TABLE NAME?</h4>
            </div>
          </div>

          <div class="col-3 shadow p-0 me-4">
            <div class="border-start border-5 border-secondary p-3 h-100">
              <h4 class="m-0">TABLE NAME?</h4>
            </div>
          </div>

          <div class="col-3 shadow p-0 me-auto">
            <div class="border-start border-5 border-secondary p-3 h-100">
              <h4 class="m-0">TABLE NAME?</h4>
            </div>
          </div>
        </div>

        <div class="mt-3">
          CONTENT
          <table class="table table-striped"></table>
        </div>

        -->

        <div class="clearer"></div>
      </div>
    </div>
    <div v-else>
      <h2>Preparing...</h2>
    </div>

    <TablePreviewSidebar :tb="selected_table" />
    <DatabasePreview :tables="state.tables" v-if="state" @change-index="(index) => selected_table_index = index" />

    <QueryHistoryOffcanvas :queries="last_queries" />

    <Footer />
  </div>
</template>
