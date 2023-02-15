<template>
  <div>
    <div v-if="isLoading" align="center" class="mt-5">
      <v-progress-circular color="primary" size="50" indeterminate />
    </div>
    <v-container v-else>
      <v-btn @click="loadData" color="primary" class="mb-5" align="right">
        <v-icon>mdi-refresh</v-icon>
        Refresh
      </v-btn>
      <v-row>
        <v-col cols="6" sm="6" md="3">
          <IndexDashboardCardItem
            tooltip="Plates Detected"
            :value="total_plates"
            :image="require('@/assets/images/plate_icon.png')"
          />
        </v-col>
        <v-col cols="6" sm="6" md="3">
          <IndexDashboardCardItem
            tooltip="Median Frames"
            :value="median_frame"
            :image="require('@/assets/images/stopwatch.png')"
          />
        </v-col>
        <v-col cols="6" sm="6" md="3">
          <IndexDashboardCardItem
            tooltip="Recurring Plates"
            :value="recurring_plates"
            :image="require('@/assets/images/taxi.png')"
          />
        </v-col>
        <v-col cols="6" sm="6" md="3">
          <IndexDashboardCardItem
            tooltip="Alerts"
            :value="total_alerts"
            :image="require('@/assets/images/alert-small.png')"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" xs="4" sm="6" md="4">
          <IndexDashboardComumCard title="Lasted Plates" bar="false">
            <IndexDashboardHistoricTableItem :data="lasted_plates" />
          </IndexDashboardComumCard>
        </v-col>
        <v-col cols="12" xs="4" sm="6" md="5">
          <IndexDashboardComumCard title="Recurring States">
            <IndexDashboardLineChart
              :labels="chartLineStatesLabels"
              :dataset="chartLineStatesDataset"
            />
          </IndexDashboardComumCard>
        </v-col>
        <v-col>
          <div class="mb-6">
            <IndexDashboardComumCard height="156" title="Street Moviment Rate">
              <IndexDashboardStreetMovimentRate
                class="mt-3"
                :list="street_moviment_list"
              />
            </IndexDashboardComumCard>
          </div>
          <div>
            <IndexDashboardComumCard height="156" title="">
              <IndexDashboardRangeDetection
                :range="street_moviment_rate"
                time="minute"
                class="mt-3"
              />
            </IndexDashboardComumCard>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import api from "@/plugins/api.js"

export default {
  props: {
    id: { type: Object, required: true },
  },

  beforeMount() {
    this.loadData()
  },

  watch: {
    id() {
      this.loadData()
    },
  },

  data() {
    return {
      recurring_plates: 0,
      street_moviment_rate: 0,
      street_moviment_list: [],
      total_alerts: 0,
      total_plates: 0,
      median_frame: 0,
      isLoading: false,
      card1Op: true,
      card2Op: true,
      chartLineStatesLabels: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        // "Jun",
        // "Jul",
        // "Aug",
        // "Sep",
        // "Oct",
        // "Nov",
        // "Dec",
      ],
      chartLineStatesDataset: [
        {
          label: "São Paulo",
          fill: true,
          data: [2, 12, 16, 34, 46, 11, 44, 89],
          backgroundColor: "#fgj979",
        },
        {
          label: "Rio de Janeiro",
          fill: true,

          data: [10, 18, 4, 24, 43, 56, 88, 11],
          backgroundColor: "#f87259",
        },
        {
          label: "Bahia",
          fill: true,

          data: [16, 7, 9, 78, 23, 54, 99, 99],
          backgroundColor: "#f89979",
        },
      ],
      lasted_plates: [],
    }
  },
  methods: {
    loadData() {
      this.isLoading = true
      api.get(`/dashboard/${this.id.id}/`).then((res) => {
        this.median_frame = res.data.median_frame
        this.lasted_plates = res.data.lasted_plates
        this.total_plates = res.data.total_plates.toString()
        this.total_alerts = res.data.total_alerts.toString()
        this.recurring_plates = res.data.recurring_plates.toString()
        this.street_moviment_rate = res.data.street_moviment_rate.toString()
        this.street_moviment_list = res.data.street_moviment_list
      })
      this.isLoading = false
    },
  },
}
</script>

<style>
.lastDetect {
  color: #fff;
  text-align: center;
  font-size: 3em;
}
</style>
