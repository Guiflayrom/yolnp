import axios from "axios"
const API_URL = "http://127.0.0.1:8000/api/v1/"

const api_logout = axios.create({
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
            Authorization: `Bearer ${localStorage.getItem("token")}`,
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

api_logout.interceptors.request.use(
  (config) => {
    const token = localStorage.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (err) => {
    return Promise.reject(err)
  }
)

api_logout.interceptors.response.use(
  (response) => {
    window.location.href = "/login/"
    return response
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      const { url, method, data } = error.response.config
      refresh(localStorage.refresh)
        .then((token) => {
          localStorage.setItem("token", token.access)
          return api({
            headers: {
              Authorization: `Bearer ${token.access}`,
              "content-type": "application/json",
            },
            method,
            url,
            data,
          }).then((response) => {
            window.location.href = "/login/"

            return Promise.resolve(response)
          })
        })
        .catch((error) => {
          Promise.reject(error)
        })
    } else {
      return Promise.resolve(error.response)
    }
  }
)

export default api_logout
