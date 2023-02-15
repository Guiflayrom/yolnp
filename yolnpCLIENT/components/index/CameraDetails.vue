<template>
  <v-sheet tile>
    <v-row class="fill-height" align="center" justify="center">
      <v-container grid-list-xs class="mx-10 mb-10">
        <!-- <v-divider></v-divider> -->
        <v-fade-transition transition="fab-transition">
          <v-card v-if="slide != null" elevation="0">
            <v-tabs v-model="tab" grow align="center" color="white">
              <v-tabs-slider color="primary"></v-tabs-slider>

              <v-tab v-for="item in items" :key="item + 1">
                <h3>
                  {{ item }}
                </h3>
              </v-tab>
            </v-tabs>

            <div align="center" class="mt-3">
              <h3 class="text-h6">{{ cameras[slide - 1].name }}</h3>
            </div>
            <v-tabs-items v-model="tab">
              <v-tab-item v-for="item in items" :key="item + 2">
                <v-card v-if="item == 'Dashboard'" flat>
                  <IndexDashboardBoardComponent :id="cameras[slide - 1]" />
                </v-card>
                <v-card v-if="item == 'Real Time'" flat>
                  <IndexStreamIframeComponent
                    :camera_id="getCameraIdBySlide()"
                  />
                </v-card>
                <v-card v-if="item == 'Alerts'" flat>
                  <IndexAlertsTableComponent
                    :alerts="getCameraAlertsBySlide()"
                    :camera_id="getCameraIdBySlide()"
                    @update="updateUserData"
                    @loader="showLoader"
                  />
                </v-card>
                <v-card v-if="item == 'Plates'" flat>
                  <IndexPlatesTabsComponent :camera="cameras[slide - 1]" />
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-fade-transition>
      </v-container>
    </v-row>
    <v-dialog v-model="dialogLoading" hide-overlay persistent width="300">
      <v-card color="primary" dark>
        <v-card-text>
          {{ textLoading }}
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-sheet>
</template>

<script>
export default {
  props: {
    slide: { type: Number, required: false },
  },

  beforeMount() {
    this.updateUserData()
  },

  watch: {
    slide() {
      this.updateUserData()
    },
  },

  data() {
    return {
      tab: null,
      dialogLoading: false,
      textLoading: "",
      //   cameras: [],
      items: ["Dashboard", "Real Time", "Alerts", "Plates"],
    }
  },

  methods: {
    showLoader(status, text = "Loading informations") {
      this.textLoading = text
      this.dialogLoading = status
    },
    updateUserData() {
      //   this.showLoader(true)
      this.$store
        .dispatch("localStorage/getUser")
        .then((status) => {
          if (status == 200) {
            this.cameras = JSON.parse(
              JSON.stringify(this.$store.state.localStorage.user.camera)
            )
            this.cameras.forEach((element) => {
              element[
                "frame_url"
              ] = `http://localhost:8000/api/v1/cva/camera/${element.id}/thumbnail/`
            })
          }
        })
        .finally(() => {
          //   this.showLoader(false)
        })
    },
    getCameraAlertsBySlide() {
      return this.cameras[this.slide - 1].alert
    },

    getCameraIdBySlide() {
      return this.cameras[this.slide - 1].id
    },
  },
}
</script>
