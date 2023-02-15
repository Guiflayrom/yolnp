<template>
  <v-simple-table dark fixed-header height="300px">
    <template #default>
      <thead>
        <tr>
          <th class="text-left">Plate</th>
          <th class="text-left">Datetime</th>
          <th class="text-left">In Frames</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.id">
          <td>{{ item.content }}</td>
          <td>{{ item.detected_at }}</td>
          <td>{{ item.in_frames }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
export default {
  props: {
    data: { type: Array, required: true },
  },
}
</script>
