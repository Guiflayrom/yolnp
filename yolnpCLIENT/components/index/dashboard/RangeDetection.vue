<template>
  <div class="cont">
    <h3 class="lastDetect">{{ range }} Plates</h3>
    <h3 class="subtitle">for each {{ time }}</h3>
  </div>
</template>

<script>
export default {
  props: {
    range: { type: String | Number, required: false, default: "0" },
    time: { type: String, required: false, default: "minute" },
  },
}
</script>

<style scoped>
.cont {
  opacity: 0.2;
  transition: 0.5s;
}

.cont:hover {
  opacity: 1;
}

h3 {
  user-select: none;
}
</style>
