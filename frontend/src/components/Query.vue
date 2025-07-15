<script setup>
import hljs from 'highlight.js/lib/core';
import sql from 'highlight.js/lib/languages/sql';

hljs.registerLanguage('sql', sql);
</script>
<template>
  <p class="font-monospace" v-html="hljs.highlight(query, { language: 'sql' }).value"></p>
</template>
<script>
export default {
  name: 'Query',
  props: {
    query: {}
  }
}
</script>