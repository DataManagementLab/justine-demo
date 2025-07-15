<template>
  <div class="col-3 shadow p-0 me-3 mb-4">
    <div class="border-start border-5 border-success p-2 h-100">
      <h6>{{ name }}</h6>
      <h5>{{ value }}</h5>
    </div>
  </div>
</template>
<script>
export default {
  name: 'ConfigDetail',
  props: {
    name: String,
    value: String,
  }
}
</script>
