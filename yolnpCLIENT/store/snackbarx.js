export const state = () => ({
  snackbar: {
    show: true,
    text: "",
    color: "",
  },
})

export const mutations = {
  setSnackbar(state, payload) {
    state.snackbar.text = payload.text
    state.snackbar.color = payload.color
    state.snackbar.show = true
  },
  setSnackbarHide(state) {
    state.snackbar.show = false
  },
}

export const actions = {
  triggerSnackbar({ commit }, payload) {
    commit("setSnackbar", payload)
  },
  hinderSnackbar({ commit }) {
    commit("setSnackbarHide")
  },
}

export const getters = {}
