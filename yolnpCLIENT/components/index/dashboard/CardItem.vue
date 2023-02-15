<template>
  <v-tooltip top>
    <template #activator="{ on, attrs }">
      <v-card
        color="primary"
        height="204"
        class="pr-1"
        elevation="10"
        align="center"
        v-bind="attrs"
        v-on="on"
      >
        <div class="card">
          <div class="face face1">
            <div class="content">
              <v-img
                :src="image"
                height="110"
                contain
                width="130"
                class="mt-3"
              />

              <h3>{{ value }}</h3>
            </div>
          </div>
        </div>
      </v-card>
    </template>

    <span>{{ tooltip }}</span>
  </v-tooltip>
</template>

<script>
export default {
  props: {
    image: { type: String, required: true },
    tooltip: { type: String, required: true },
    value: { type: String | Number, required: true },
  },
}
</script>

<style>
.card {
  cursor: pointer;
  height: 150px;
  padding-bottom: 30px;
  border-radius: 10px;
}

.card .face.face1 {
  background: #424242;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
}

.card .face.face1 .content {
  opacity: 0.2;
  transition: 0.5s;
}

.card:hover .face.face1 .content {
  opacity: 1;
}

.card .face.face1 .content img {
  max-width: 150px;
}

.card .face.face1 .content h3 {
  margin: 10px 0 0;
  padding: 0;
  color: #fff;
  text-align: center;
  font-size: 3em;
}
</style>
