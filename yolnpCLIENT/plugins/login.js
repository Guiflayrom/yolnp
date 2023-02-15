import axios from "axios"
const API_URL = "http://127.0.0.1:8000/api/v1/"

const api = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
  baseURL: API_URL,
})

export default api
