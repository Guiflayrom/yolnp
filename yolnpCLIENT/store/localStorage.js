import api from "@/plugins/api.js"
import jwt_decode from "jwt-decode"

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(";").shift()
}

export const state = () => ({
  user: {},
})

export const mutations = {
  setUser(state, userObj) {
    state.user = userObj
  },
}

export const actions = {
  async getUser({ commit }) {
    return new Promise((resolve, reject) => {
      api
        .get(`/user/${jwt_decode(getCookie("refresh")).user_id}`)
        .then((res) => {
          if (res.status == 200) {
            commit("setUser", res.data)
          }
          return resolve(res.status)
        })
        .catch((err) => {
          console.error("Critical error:", err)
          reject(err)
        })
    })
  },
}
