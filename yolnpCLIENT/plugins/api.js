import axios from "axios"

const API_URL = "http://127.0.0.1:8000/api/v1/"

function setCookie(cname, cvalue, durationInSeconds) {
  const d = new Date()
  d.setTime(d.getTime() + durationInSeconds * 1000)
  let expires = "expires=" + d.toUTCString()
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/"
}

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(";").shift()
}

const api = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
  baseURL: API_URL,
})

const refresh = (refresh) => {
  return new Promise((resolve, reject) => {
    axios
      .post(
        `${API_URL}token/refresh/`,
        {
          refresh: refresh,
        },
        {
          headers: {
            "content-type": "application/json",
          },
        }
      )
      .then((response) => {
        try {
          resolve(response.data)
        } catch (error) {
          window.location.href = "/login/"
        }
      })
      .catch((error) => {
        reject(error)
      })
  })
}

api.interceptors.request.use(
  (config) => {
    const token = getCookie("access")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (err) => {
    return Promise.reject(err)
  }
)

api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      const { url, method, data } = error.response.config
      return refresh(getCookie("refresh"))
        .then((token) => {
          setCookie("access", token.access, 60 * 2)

          return api({
            headers: {
              Authorization: `Bearer ${token.access}`,
              "content-type": "application/json",
            },
            method,
            url,
            data,
          }).then((response) => {
            return Promise.resolve(response)
          })
        })
        .catch((error) => {
          setCookie("refresh", null)
          Promise.reject(error)
          window.location.href = "/login/"
        })
    } else {
      return Promise.resolve(error.response)
    }
  }
)

export default api
