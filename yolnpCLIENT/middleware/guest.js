import api from "@/plugins/login.js"

export default function ({ app, redirect, next }) {
  let refresh = app.$cookies.get("refresh")
  if (!refresh) {
    redirect("/login")
  } else {
    return api
      .post("/token/refresh/", JSON.stringify({ refresh: refresh }))
      .then((result) => {})
      .catch((err) => {
        redirect("/login")
      })
  }
}
