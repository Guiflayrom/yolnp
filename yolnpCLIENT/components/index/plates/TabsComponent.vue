<template>
  <div>
    <v-expansion-panels class="rounded-lg elevation-0">
      <v-expansion-panel v-for="(item, i) in dropDown" :key="i">
        <v-expansion-panel-header>
          <span class="primary--text">
            <h3>
              {{ item.title }}
            </h3>
          </span>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <div v-if="item.title == 'All Plates'">
            <IndexPlatesAllTable :plates="allPlates" />
          </div>
          <div v-if="item.title == 'Alerts'">
            <IndexPlatesAlertsTable :plates="alertsPlates" />
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>
<script>
import api from "@/plugins/api.js"

export default {
  props: {
    camera: { type: Object, required: true },
  },
  beforeMount() {
    this.loadData()
  },

  watch: {
    camera() {
      this.loadData()
    },
  },

  data() {
    return {
      allPlates: [],
      alertsPlates: [],
      dropDown: [{ title: "All Plates" }, { title: "Alerts" }],
    }
  },
  methods: {
    loadData() {
      this.isLoading = true
      api.get(`/dashboard/${this.camera.id}/`).then((res) => {
        this.alertsPlates = res.data.alerts
        this.allPlates = res.data.lasted_plates
        console.log(this.alertsPlates)
      })
      this.isLoading = false
    },
  },
}
</script>
