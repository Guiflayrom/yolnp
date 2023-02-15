<template>
  <div aling="center">
    <v-row>
      <v-col cols="12">
        <iframe
          :src="`http://localhost:8061/cva/camera/${camera_id}/stream/`"
          frameborder="0"
          width="100%"
          height="500px"
        ></iframe>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  props: {
    camera_id: { type: String, required: false },
  },
}
</script>
