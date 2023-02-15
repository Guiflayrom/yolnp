<template>
  <v-app dark>
    <SnackBar />
    <v-main>
      <v-container class="mb-10">
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer :absolute="!fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>
<script>
export default {
  data() {
    return {
      fixed: true,
    }
  },
}
</script>
