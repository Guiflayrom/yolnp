import colors from "vuetify/es5/util/colors"

export default {
  // Target: https://go.nuxtjs.dev/config-target
  target: "static",

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: "%s - yolnp_client",
    title: "yolnp_client",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
      { name: "format-detection", content: "telephone=no" },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: ["@/plugins/chart.js"],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/vuetify
    "@nuxtjs/vuetify",
    // https://google-fonts.nuxtjs.org/setup
  ],
  ssr: true,
  target: "server",
  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    "@nuxtjs/axios",
    "cookie-universal-nuxt",
    "nuxt-vuex-localstorage",
    [
      "v-currency-field/nuxt",
      {
        locale: "en-US",
        decimalLength: 2,
        autoDecimalMode: true,
        min: null,
        max: null,
        defaultValue: 0,
        valueAsInteger: false,
        allowNegative: true,
      },
    ],
    // https://go.nuxtjs.dev/content
  ],

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: "en",
    },
  },

  // Content module configuration: https://go.nuxtjs.dev/config-content
  content: {},

  axios: {
    baseURL: "http://127.0.0.1:8060/",
    headers: {
      common: {
        Accept: "application/json, text/plain, */*",
        "Content-Type": "application/json",
      },
    },
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ["~/assets/variables.scss"],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: "#bf1720",
          secondary: "#DE0939",
          accent: colors.grey.darken3,
          info: "#592A2A",
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    transpile: ["chart.js"],
  },
}
