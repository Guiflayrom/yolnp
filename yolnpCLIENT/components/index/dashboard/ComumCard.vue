<template>
  <v-tooltip v-if="tooltip.length" top>
    <template #activator="{ on, attrs }">
      <v-card
        color="primary"
        :class="bar == 'true' ? 'pr-1' : ''"
        v-bind="attrs"
        :height="height"
        v-on="on"
      >
        <v-card color="accent" :height="height">
          <div
            align="center"
            @mouseenter="cardOp = !cardOp"
            @mouseleave="cardOp = !cardOp"
          >
            <h3 :class="cardOp ? 'cardTitle py-1' : 'cardTitleOp py-1'">
              {{ title }}
            </h3>
            <slot />
          </div>
        </v-card>
      </v-card>
    </template>
    <span>{{ tooltip }}</span>
  </v-tooltip>
  <v-card
    v-else
    color="primary"
    :class="bar == 'true' ? 'pr-1' : ''"
    :height="height"
  >
    <v-card color="accent" :height="height">
      <div
        align="center"
        @mouseenter="cardOp = !cardOp"
        @mouseleave="cardOp = !cardOp"
      >
        <h3 :class="cardOp ? 'cardTitle py-1' : 'cardTitleOp py-1'">
          {{ title }}
        </h3>
        <slot />
      </div>
    </v-card>
  </v-card>
</template>

<script>
export default {
  props: {
    tooltip: { type: String, required: false, default: "" },
    title: { type: String, required: true },
    height: { type: String, required: false, default: "" },
    bar: { type: String, required: false, default: "true" },
  },
  data() {
    return {
      cardOp: true,
    }
  },
}
</script>

<style>
.cardTitle {
  opacity: 0.2;
  transition: 0.5s;
}

.cardTitle:hover {
  opacity: 1;
}

.cardTitleOp {
  opacity: 1;
  transition: 0.5s;
}
h3 {
  user-select: none;
}
</style>
