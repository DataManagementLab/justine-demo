<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>

<template>
  <div class="offcanvas offcanvas-end w-75" tabindex="-1" id="tableOffcanvas" aria-labelledby="tableOffcanvasLabel">
    <div v-if="tb != null" class="overflow-y-auto">
      <div class="offcanvas-header">
        <h3 class="offcanvas-title" id="tableOffcanvasLabel">
          <font-awesome-icon :icon="['fas', 'table']"/>
          {{ tb.name }}
        </h3>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <h5 class="font-monospace">{{ tb.columns.length }} columns, {{ tb.row_count }} rows</h5>
        <table class="table table-striped mt-4">
          <thead>
          <tr>
            <th v-for="c in tb.columns">{{ c }}</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="r in tb.data">
            <td v-for="cell in r.split(';')">{{ cell }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else>
      <div class="offcanvas-header">
        <h3>No table selected</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TablePreviewSidebar',
  props: {
    tb: Array
  }
}
</script>