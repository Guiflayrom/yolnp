<template>
  <v-app dark>
    <SnackBar />

    <v-navigation-drawer
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      left
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon :to="item.to">{{ item.icon }}</v-icon>
          </v-list-item-action>
        </v-list-item>
        <v-list-item>
          <v-list-item-action>
            <v-progress-circular
              v-if="loading"
              indeterminate
              color="white"
            ></v-progress-circular>
            <v-icon v-else @click="logout()">mdi-logout</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer :absolute="!fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import api from "@/plugins/api.js"

export default {
  name: "DefaultLayout",

  data() {
    return {
      loading: false,
      clipped: true,
      drawer: false,
      fixed: true,
      items: [
        {
          icon: "mdi-apps",
          title: "Index",
          to: "/",
        },
      ],
      miniVariant: true,
      right: true,
      rightDrawer: false,
      title: "YOLNP",
    }
  },
  methods: {
    callSnack(text, color) {
      this.$store.dispatch("snackbarx/triggerSnackbar", {
        text: text,
        color: color,
      })
    },
    getCookie(name) {
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${name}=`)
      if (parts.length === 2) return parts.pop().split(";").shift()
    },
    logout() {
      setInterval(() => {
        this.loading = true
      }, 100)
      api
        .post("/auth/logout/", {
          refresh: this.getCookie("refresh"),
        })
        .then((res) => {
          this.$store.commit("setAccessToken", "")
          this.$store.commit("setRefreshToken", "")
          window.location.href = "/login/"
        })
    },
  },
}
</script>
