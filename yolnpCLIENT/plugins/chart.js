import Vue from "vue"
import { Line } from "vue-chartjs"

Vue.component("LineChart", {
  extends: Line,
  props: {
    data: {
      type: Object,
      required: true,
    },
    height: { type: String, required: true },
    options: {
      type: Object,
      required: false,
      default: () => ({
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: true,
        },
      }),
    },
  },
  watch: {
    data() {
      this.renderChart(this.data, this.options)
    },
  },
  mounted() {
    this.renderChart(this.data, this.options)
  },
})
