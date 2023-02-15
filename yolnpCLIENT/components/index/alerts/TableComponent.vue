<template>
  <div>
    <div v-if="isLoading" align="center" class="mt-5">
      <v-progress-circular color="primary" size="50" indeterminate />
    </div>
    <div v-else>
      <v-data-table
        :headers="headers"
        :items="alerts"
        :items-per-page="5"
        class="elevation-1"
      >
        <template #top>
          <v-toolbar flat color="accent">
            <v-toolbar-title>Plate Alerts</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="500px" persistent>
              <template #activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  dark
                  class="mb-2"
                  v-bind="attrs"
                  v-on="on"
                >
                  <h3>New Alert</h3>
                </v-btn>
              </template>
              <v-form v-model="form">
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field
                            v-model="editedItem.plate"
                            label="Plate"
                            counter="7"
                            :rules="requiredRules"
                          ></v-text-field>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="red darken-1" text @click="close">
                      Cancel
                    </v-btn>
                    <v-btn
                      color="red darken-1"
                      text
                      @click="save"
                      :disabled="!form"
                    >
                      Save
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-form>
            </v-dialog>
            <v-dialog v-model="dialogDelete" max-width="500px">
              <v-card>
                <v-card-title class="text-h5"
                  >Are you sure you want to delete this item?</v-card-title
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="red darken-1" text @click="closeDelete"
                    >Cancel</v-btn
                  >
                  <v-btn color="red darken-1" text @click="deleteItemConfirm"
                    >OK</v-btn
                  >
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template #[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
        </template>
      </v-data-table>
    </div>
  </div>
</template>
<script>
import api from "@/plugins/api.js"

export default {
  props: {
    camera_id: { type: String, required: true },
    alerts: { type: Array, required: true },
  },
  data() {
    return {
      form: false,
      requiredRules: [
        (v) => !!v || "Plate is required",
        (v) => v.length <= 10 || "Max 10 characters",
      ],

      formTitle: "New Alert",
      isLoading: false,
      dialog: false,
      dialogDelete: false,
      editedIndex: -1,
      editedItem: {
        id: "",
        plate: "",
      },
      defaultItem: {
        id: "",
        plate: "",
      },
      headers: [
        {
          text: "Plate",
          align: "center",
          sortable: true,
          value: "plate",
        },
        { text: "Actions", align: "center", value: "actions", sortable: false },
      ],
    }
  },

  methods: {
    editItem(item) {
      this.formTitle = "Edit Alert"
      this.editedIndex = this.alerts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem(item) {
      this.editedIndex = this.alerts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm() {
      this.$emit("loader", true, "Processing your request...")
      api
        .delete(`/alert/${this.editedItem.id}`)
        .then((res) => {
          if (res.status == 204) {
            this.$emit("loader", false, "Processing your request...")
            this.$emit("update")
          }
        })
        .catch((err) => {
          console.log(err)
        })
      this.closeDelete()
    },

    close() {
      this.dialog = false
      this.formTitle = "New Alert"
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save() {
      this.$emit("loader", true, "Processing your request...")
      if (this.editedIndex > -1) {
        api
          .patch(`/alert/${this.editedItem.id}`, this.editedItem)
          .then((res) => {
            if (res.status == 200) {
              this.$store.dispatch("snackbarx/triggerSnackbar", {
                text: "Alert Edited Successfuly",
                color: "green",
              })
              this.$emit("loader", false, "Processing your request...")
              this.$emit("update")
            } else if (res.status == 400) {
              this.$store.dispatch("snackbarx/triggerSnackbar", {
                text: "Plate Number Cannot Exceeded 10 Characters",
                color: "error",
              })
            }
          })
          .catch((err) => {
            console.log(err)
          })
      } else {
        delete this.editedItem.id
        this.editedItem["camera"] = this.camera_id
        api
          .post(`/alert/`, this.editedItem)
          .then((res) => {
            if (res.status == 201) {
              this.$store.dispatch("snackbarx/triggerSnackbar", {
                text: "Alert Created Successfuly",
                color: "green",
              })
              this.$emit("update")
            } else if (res.status == 400) {
              this.$store.dispatch("snackbarx/triggerSnackbar", {
                text: "Plate Number Cannot Exceeded 10 Characters",
                color: "error",
              })
            }
          })
          .catch((err) => {
            console.log(err)
          })
      }

      this.close()
    },
  },
}
</script>
