import api from "@/plugins/login.js"

function setCookie(cname, cvalue, durationInSeconds) {
  const d = new Date()
  d.setTime(d.getTime() + durationInSeconds * 1000)
  let expires = "expires=" + d.toUTCString()
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/"
}

export const state = () => ({
  accessToken: null,
  refreshToken: null,
})

export const mutations = {
  setAccessToken(state, accessToken) {
    state.accessToken = accessToken
    setCookie("access", accessToken, 60 * 2)
  },

  setRefreshToken(state, refreshToken) {
    state.refreshToken = refreshToken
    setCookie("refresh", refreshToken, 24 * 60 * 60)
  },
}

export const actions = {
  async login({ commit }, formData) {
    return new Promise((resolve) => {
      api
        .post("/token/", JSON.stringify(formData))
        .then(async (res) => {
          if (res.status == 200) {
            commit("setAccessToken", res.data.access)
            commit("setRefreshToken", res.data.refresh)
          }
          return resolve(res.status)
        })
        .catch((err) => {
          return resolve(err.response.status)
        })
    })
  },
}

export const getters = {}
