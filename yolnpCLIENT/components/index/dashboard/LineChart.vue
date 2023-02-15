<template>
  <div class="p-2 border border-gray-500">
    <client-only>
      <LineChart :data="chartData" height="300" />
    </client-only>
  </div>
</template>

<script>
export default {
  props: {
    labels: {
      required: true,
      type: Array,
    },
    dataset: {
      required: true,
      type: Array,
    },
  },
  computed: {
    chartData() {
      return {
        labels: this.labels,
        datasets: this.dataset,
      }
    },
  },
}
</script>
