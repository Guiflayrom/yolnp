<template>
  <v-row justify="center" align="center">
    <!-- Create Dialog -->
    <v-dialog v-model="dialogCreate" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">
            <h3>New Camera</h3>
          </span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  v-model="cameraObject.name"
                  label="Camera name*"
                  required
                  hint="Street Lorem... My storage..."
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  v-model="cameraObject.rtsp"
                  label="RTSP*"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-currency-field
                  v-model="cameraObject.fps"
                  label="FPS"
                  required
                  :max="maxFPS"
                ></v-currency-field>
              </v-col>
            </v-row>
          </v-container>
          <small> *indicates required field </small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="dialogCreate = false">
            <h4>Close</h4>
          </v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="
              dialogCreate = false
              addNewCamera()
            "
          >
            <h4>Create</h4>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Loading -->

    <v-sheet class="mx-auto" elevation="8" :min-width="max_width">
      <v-row align="center" justify="center">
        <v-slide-group
          v-model="slide"
          class="pa-4 mx-5"
          show-arrows
          center-active
        >
          <v-row>
            <div>
              <v-card height="300"> </v-card>
            </div>
            <v-slide-item width="10">
              <v-hover v-slot="{ hover }" open-delay="50">
                <v-card
                  color="accent"
                  class="d-flex align-center justify-center ma-4 pointer"
                  height="189"
                  width="200"
                  :elevation="hover ? 32 : 10"
                  @click="dialogCreate = true"
                >
                  <v-icon dark> mdi-plus </v-icon>
                </v-card>
              </v-hover>
            </v-slide-item>
            <v-slide-item
              v-for="i in cameras"
              :key="i.id"
              v-slot="{ active, toggle }"
              width="10"
              style="border"
            >
              <v-hover v-slot="{ hover }" open-delay="50">
                <v-card
                  color="primary"
                  class="ma-4"
                  :height="active ? 250 : 189"
                  width="200"
                  :elevation="hover ? 32 : 10"
                  @click="toggle"
                >
                  <v-img
                    height="184"
                    :src="i['frame_url']"
                    :gradient="i['hover'] || active ? '' : gradient"
                    @mouseenter="
                      () => {
                        i['hover'] = !i['hover']
                      }
                    "
                    @mouseleave="
                      () => {
                        i['hover'] = !i['hover']
                      }
                    "
                  >
                  </v-img>
                  <v-expand-transition>
                    <v-row
                      v-if="active"
                      class="d-flex justify-center mt-1 mx-1 mr-4"
                    >
                      <v-col cols="3">
                        <v-dialog v-model="dialogRun" width="500">
                          <template #activator="{ on, attrs }">
                            <v-btn
                              icon
                              v-bind="attrs"
                              @click="runProcessCamera(i)"
                              v-on="on"
                            >
                              <v-icon color="white" size="36">
                                {{ i.active ? "mdi-pause" : "mdi-play" }}
                              </v-icon>
                            </v-btn>
                          </template>

                          <v-card>
                            <v-card-title>
                              <span class="text-h5">
                                <h3>Camera Processing</h3>
                              </span>
                            </v-card-title>
                            <v-card-text>
                              <v-container>
                                <h4>
                                  Currently this camera is being processed. You
                                  going to be notified when it stops for have
                                  external problems.
                                </h4>
                              </v-container>
                            </v-card-text>

                            <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn
                                color="red darken-1"
                                text
                                @click="dialogRun = false"
                              >
                                <h4>Ok</h4>
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                      </v-col>
                      <v-col cols="3">
                        <v-dialog
                          v-model="dialogEdit"
                          max-width="600px"
                          persistent
                        >
                          <template #activator="{ on, attrs }">
                            <v-btn
                              icon
                              v-bind="attrs"
                              v-on="on"
                              @click="openConfig()"
                            >
                              <v-icon color="white" size="36"> mdi-cog </v-icon>
                            </v-btn>
                          </template>
                          <v-card>
                            <v-card-title>
                              <span class="text-h5">
                                <h3>Camera Configuration</h3>
                              </span>
                            </v-card-title>
                            <v-card-text>
                              <v-container>
                                <v-row>
                                  <v-col cols="12" sm="6" md="6">
                                    <v-text-field
                                      v-model="cameraObject.name"
                                      label="Camera name*"
                                      required
                                      hint="Street Lorem... My storage..."
                                    ></v-text-field>
                                  </v-col>
                                  <v-col cols="12" sm="6" md="6">
                                    <v-text-field
                                      v-model="cameraObject.rtsp"
                                      label="RTSP*"
                                      required
                                    ></v-text-field>
                                  </v-col>
                                  <v-col cols="6" sm="6" md="6">
                                    <v-switch
                                      v-model="cameraObject.alert_stolen_cars"
                                      label="Alert stolen cars"
                                    />
                                  </v-col>
                                  <v-col cols="6" sm="6" md="6">
                                    <v-switch
                                      disabled
                                      label="Alert cars with traffic ticket"
                                    />
                                  </v-col>
                                </v-row>
                              </v-container>
                              <small> *indicates required field </small>
                            </v-card-text>
                            <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn
                                color="red darken-1"
                                text
                                @click="dialogEdit = false"
                              >
                                <h4>Close</h4>
                              </v-btn>
                              <v-btn
                                color="red darken-1"
                                text
                                @click="
                                  dialogEdit = false
                                  editCamera()
                                "
                              >
                                <h4>Save</h4>
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                      </v-col>
                      <v-col cols="3">
                        <v-dialog
                          v-model="dialogDelete"
                          transition="dialog-bottom-transition"
                          max-width="600"
                        >
                          <template #activator="{ on, attrs }">
                            <v-btn icon v-bind="attrs" v-on="on">
                              <v-icon color="white" size="36">
                                mdi-delete
                              </v-icon>
                            </v-btn>
                          </template>
                          <v-card>
                            <v-card-title class="text-h5">
                              <h3>Are you sure you want to delete?</h3>
                            </v-card-title>
                            <v-card-text>
                              <h3>
                                This process is irreversible and you will lose
                                all your data.
                              </h3>
                            </v-card-text>
                            <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn
                                color="red darken-1"
                                text
                                @click="dialogDelete = false"
                              >
                                <h4>Cancel</h4>
                              </v-btn>
                              <v-btn
                                color="red darken-1"
                                text
                                @click="
                                  dialogDelete = false
                                  deleteCamera()
                                "
                              >
                                <h4>Yes, delete</h4>
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                      </v-col>
                    </v-row>
                  </v-expand-transition>
                </v-card>
              </v-hover>
            </v-slide-item>
          </v-row>
        </v-slide-group>
      </v-row>
      <IndexCameraDetails :slide="slide" />
    </v-sheet>
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
  </v-row>
</template>

<script>
import api from "@/plugins/api.js"

export default {
  layout: "default",
  middleware: "guest",

  data() {
    return {
      maxFPS: 120,
      textLoading: "Loading informations",
      dialogLoading: false,
      dialogCreate: false,
      dialogRun: false,
      dialogEdit: false,
      dialogDelete: false,
      items: ["Dashboard", "Real Time", "Alerts", "Plates"],
      tab: null,
      gradient: "to top right, rgba(0,0,0,.33), rgba(0,0,0,.7)",
      cameraObject: { name: "", rtsp: "", alert_stolen_cars: false, fps: 0 },
      cameras: [],
      slide: null,
      max_width: 0,
    }
  },

  beforeMount() {
    this.max_width = window.innerWidth
  },

  mounted() {
    this.updateUserData()
  },

  methods: {
    callSnack(text, color) {
      this.$store.dispatch("snackbarx/triggerSnackbar", {
        text: text,
        color: color,
      })
    },
    getCameraAlertsBySlide() {
      return this.cameras[this.slide - 1].alert
    },

    getCameraIdBySlide() {
      return this.cameras[this.slide - 1].id
    },
    showLoader(status, text = "Loading informations") {
      this.textLoading = text
      this.dialogLoading = status
    },
    updateUserData() {
      this.showLoader(true)
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
          this.showLoader(false)
        })
    },
    getCookie(name) {
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${name}=`)
      if (parts.length === 2) return parts.pop().split(";").shift()
    },
    addNewCamera() {
      api
        .post("/camera/", {
          user: this.$store.state.localStorage.user.id,
          name: { ...this.cameraObject }.name,
          fps: { ...this.cameraObject }.fps,
          rtsp: { ...this.cameraObject }.rtsp,
        })
        .then((res) => {
          if (res.status == 201) {
            this.callSnack("Camera created successfully!", "green")
            this.updateUserData()
          }
        })

      this.resetCamObject()
    },
    runProcessCamera(ctx) {
      if (ctx.active) {
        this.stopProcessCamera(ctx.id)
      } else {
        const payload = {
          camera_id: ctx.id,
          camera_fps: ctx.fps,
          camera_source: ctx.rtsp,
        }
        api.post("/cva/start/", payload).then((res) => {})
      }
      ctx.active = !ctx.active
    },
    stopProcessCamera(id) {
      api.get(`/cva/stop/${id}/`)
    },
    openConfig() {
      this.cameraObject.name = this.cameras[this.slide - 1].name
      this.cameraObject.rtsp = this.cameras[this.slide - 1].rtsp
      this.cameraObject.fps = this.cameras[this.slide - 1].fps
      this.cameraObject.alert_stolen_cars =
        this.cameras[this.slide - 1].alert_stolen_cars
    },
    editCamera() {
      const post = { ...this.cameraObject }

      api
        .patch(`/camera/${this.cameras[this.slide - 1].id}/`, post)
        .then((res) => {
          if (res.status == 200) {
            this.resetCamObject()
            this.callSnack("Camera edited successfully!", "green")
            this.updateUserData()
          }
        })
    },

    deleteCamera() {
      let id = this.cameras[this.slide - 1].id
      api.delete(`/camera/${id}`).then((res) => {
        if (res.status == 204) {
          this.callSnack("Camera deleted successfully!", "green")
          this.slide = null
          this.updateUserData()
        }
      })
    },
    resetCamObject() {
      this.cameraObject = {
        name: "",
        rtsp: "",
        alert_stolen_cars: false,
        fps: 0,
      }
    },
  },
}
</script>

<style>
.card {
  height: 100px;
}

::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #bf1720;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #bf1720;
}

.pointer {
  cursor: pointer;
}
</style>
