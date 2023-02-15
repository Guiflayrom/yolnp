<template>
  <v-card>
    <v-card-title>
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="plates"
      item-key="id"
      class="elevation-1"
      :search="search"
    >
      <template #[`item.image`]="{ item }">
        <v-img :src="item.image"></v-img>
      </template> </v-data-table
  ></v-card>
</template>

<script>
export default {
  props: {
    plates: { type: Array, required: true },
  },

  data() {
    return {
      search: "",
    }
  },

  computed: {
    headers() {
      return [
        {
          text: "Plate",
          sortable: true,
          value: "content",
        },
        {
          text: "In Frames",
          sortable: true,
          value: "in_frames",
        },
        {
          text: "Detected At",
          sortable: true,
          value: "detected_at",
        },
        { text: "State", value: "state", align: "center" },
        { text: "City", value: "city", align: "center" },
        { text: "Image", value: "image", align: "center" },
      ]
    },
  },
}
</script>
