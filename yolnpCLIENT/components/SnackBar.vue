<template>
  <v-snackbar
    timeout="-1"
    bottom
    :color="snackbar.color"
    outlined
    v-model="snackbar.show"
  >
    {{ snackbar.text }}

    <template v-slot:action="{ attrs }">
      <v-btn :color="snackbar.color" text v-bind="attrs" @click="closeSnack()">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  computed: {
    snackbar() {
      return this.$store.state.snackbarx.snackbar
    },
  },

  beforeCreate() {
    this.$store.dispatch("snackbarx/hinderSnackbar")
  },

  updated() {
    setTimeout(() => {
      this.$store.dispatch("snackbarx/hinderSnackbar")
    }, 3000)
  },

  methods: {
    closeSnack() {
      this.$store.dispatch("snackbarx/hinderSnackbar")
    },
  },
}
</script>
>
