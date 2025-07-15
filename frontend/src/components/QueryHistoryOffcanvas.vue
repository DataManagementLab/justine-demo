<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Query from "./Query.vue";
</script>

<template>
  <div class="offcanvas offcanvas-bottom h-50" tabindex="-1" id="queryOffcanvas" aria-labelledby="queryOffcanvasLabel">
    <div class="overflow-y-auto">
      <div class="offcanvas-header">
        <h3 class="offcanvas-title" id="queryOffcanvasLabel">
          <font-awesome-icon :icon="['fas', 'arrow-rotate-right']" />
          Query History
        </h3>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <Query :query="q" v-for="q in last_queries" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QueryHistoryOffcanvas',
  props: {
    last_queries: Array
  }
}
</script>