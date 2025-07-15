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

hljs.registerLanguage('sql', sql);
</script>
<style>
.queryBox {
  height: 10vh;
  overflow-y: scroll;
  background-color: #fcfde5;
  padding: 1rem
}
</style>
<script>
export default {
  components: {
  },

  computed: {
    mode() {
      return this.$route.params.mode;
    },
    query() {
      return this.$route.query;
    },
    islive() {
      return this.mode === 'live';
    },
    done() {
      // No loading when server indicated that there is nothing more, always load after run creation
      return this.last_step !== null && !this.last_step.more
    },
    currentProgress() {
      if (this.last_step === null) {
        return 0
      }
      return this.last_step.iteration / this.run_details.num_iterations * 100
    },
    selected_table() {
      // Select which table will be previewed in offcanvas sidebar
      if (this.selected_table_index === -1) {
        return null
      }
      return this.last_step.tables[this.selected_table_index]
    },
  },

  methods: {
    async startRun() {
      // Create a new run on the server
      this.run_id = null
      const res = await fetch('http://localhost:8000/batch/', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.query)}
      )
      this.run_details = await res.json()
    },
    async getRunInfo() {
      // Get Run Info for replay mode
      const res = await fetch('http://localhost:8000/runs/' + this.run_id + '/')
      this.run_details = await res.json()
    },
    async batch_next() {
      // Load next step results from server (if still work to do)
      if (!this.done) {
        const res = await fetch('http://localhost:8000/batch/' + this.run_id + '/next')
        this.step = await res.json()
      }
    },
    async load_step(iteration) {
        const res = await fetch('http://localhost:8000/runs/' + this.run_id + '/iteration/' + iteration)
        this.step = await res.json()
    },
    next() {
      // Load next step results from server (if still work to do)
      if(this.islive) {
        this.batch_next()
      }
      else if(!this.done && !this.paused) {
        this.load_step(this.iteration + 1)
      }
    },
    selectTableForPreview(index) {
      // Select which table will be previewed in offcanvas sidebar
      this.selected_table = this.last_step.tables[index]
    },
    togglePaused() {
      // Toggle paused state and restart if unpaused
      this.paused = !this.paused
      if (!this.paused) {
        this.next()
      }
    },
    selectStep(e) {
      this.paused = true
      this.load_step(e.target.value)
    }
  },

  watch : {
    run_details() {
      // Wait for run creation on the server and perform first step once it is ready
      this.run_id = this.run_details.id

      if(!this.islive) {
        // In replay mode, set system delay factor in a way that the replay takes 30 seconds at single speed
        this.systemDelayFactor = 30000 / this.run_details.num_iterations
      }

      this.next()
    },
    step(newStep) {
      // React to step answer from server
      // by replacing current preview
      // and calling next step if not paused
      this.last_step = newStep
      this.iteration = newStep.iteration
      if(!this.paused) {
        setTimeout(() => this.next(), this.systemDelayFactor * (1 / this.speed))
      }
    }
  },

  mounted() {
    if(this.islive) {
      // New Run? Initiate it on the server
      this.startRun()
    }
    else {
      // Start replay
      this.run_id = this.query.id
      // Set speedup to 1, can be changed with buttons
      this.userDelayFactor = 1
      this.getRunInfo()
    }
  },

  beforeRouteLeave(to, from) {
    // called when the route that renders this component is about to be navigated away from.
    // Stop current run if necessary
    if(!this.done) {
      this.paused = true
    }
  },

  data() {
    return {
      run_id: null,
      run_details: null,
      last_step: null,
      step: null,
      selected_table_index: -1,
      paused: false,
      speed: 1,
      systemDelayFactor: 0,
      iteration: 0,
    };
  },
};
</script>

<template>
  <div class="container py-4 px-3 mx-auto">
    <Header />

    <div v-if="run_details !== null">
      <div class="row mt-3 p-2">
        <ConfigDetail name="Dataset" :value="run_details.dataset_name" />
        <ConfigDetail name="Missing Table Names" :value="run_details.missingTableNames + ' %'" />
        <ConfigDetail name="Missing Column Names" :value="run_details.missingColumnNames + ' %'" />
        <ConfigDetail name="Table Name Synonyms" :value="run_details.tableSynonyms + ' %'" v-if="run_details.tableSynonyms" />
        <ConfigDetail name="Column Name Synonyms" :value="run_details.columnsSynonyms + ' %'" v-if="run_details.columnsSynonyms" />
      </div>
    </div>

    <div v-if="last_step != null" class="mt-4">
      <TablePreviewSidebar :tb="selected_table" />

      <h2 class="text-end">{{ iteration }}</h2>
      <div v-if="islive">
        <div class="progress">
          <div class="progress-bar progress-bar-striped bg-warning" :class="{'progress-bar-animated': !done}" role="progressbar" :style="'width: ' + currentProgress + '%;'" :aria-valuenow="currentProgress" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
        <div v-if="done" class="text-center mt-3">
          <router-link :to="{ name: 'play', params: { mode: 'replay' }, query: { id: run_id }}" class="btn btn-warning">
              <font-awesome-icon :icon="['fas', 'circle-play']" /> Replay
          </router-link>
        </div>
      </div>
      <div v-else>
        <input type="range" class="form-range w-100" min="1" :max="run_details.num_iterations" step="1" :value="iteration" id="stepRange" @change="selectStep">
      </div>

      <div class="text-center mt-3">
        <button v-if="!done" class="btn btn-light btn-lg" @click="togglePaused">
          <font-awesome-icon :icon="['fas', paused ? 'play' : 'pause']" />
        </button>
        <button v-else-if="!islive" class="btn btn-light btn-lg" @click="paused=false;load_step(1)">
          <font-awesome-icon :icon="['fas', 'redo']" />
        </button>
        <span v-if="!islive" class="ms-5">
          Speed: {{ speed}} x&nbsp;
          <button class="btn btn-light" @click="speed = speed / 2">
            <font-awesome-icon :icon="['fas', 'circle-minus']" />
          </button>&nbsp;
          <button class="btn btn-light" @click="speed = speed * 2">
            <font-awesome-icon :icon="['fas', 'circle-plus']" />
          </button>
        </span>
      </div>

      <h5 class="mt-5">Last Query:</h5>
      <div class="queryBox">
        <Query :query="last_step.query" />
      </div>
      <div class="text-center text-large mt-2 mb-2">
        <h2><font-awesome-icon :icon="['fas', 'circle-down']" /></h2>
      </div>
      <div class="queryBox">
        <Query :query="last_step.adjusted_query" />
      </div>

      <DatabasePreview :tables="last_step.tables" v-if="last_step" @change-index="(index) => selected_table_index = index" />
    </div>

    <h2></h2>

    <Footer />
  </div>
</template>
