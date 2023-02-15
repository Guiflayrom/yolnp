<template>
  <div>
    <v-row class="d-flex">
      <v-col cols="6">
        <div>
          <v-col cols="12">
            <v-img
              src="https://i.ibb.co/rxbp9Mz/logo.png"
              contain
              height="300"
            ></v-img>
          </v-col>
          <v-col cols="12" class="d-flex justify-center">
            <h1>Welcome</h1>
          </v-col>
          <v-col cols="12" class="d-flex justify-center">
            <h3>Enter your account here</h3>
          </v-col>
        </div>
      </v-col>
      <v-col cols="6" class="mt-10 align-self-center">
        <v-row justify="center" align="center">
          <v-form v-model="valid">
            <v-container grid-list-xs>
              <p>Email</p>
              <v-text-field
                v-model="formData.email"
                label="Email"
                outlined
                :rules="requiredRules"
                filled
                required
                solo
                hint="Insert your email"
              >
                <template #prepend>
                  <v-tooltip bottom>
                    <template #activator="{ on }">
                      <v-icon v-on="on"> mdi-email </v-icon>
                    </template>
                    E-mail
                  </v-tooltip>
                </template>
              </v-text-field>
              <p>Password</p>
              <v-text-field
                v-model="formData.password"
                label="Password"
                outlined
                filled
                required
                :rules="requiredRules"
                @keyup.enter="
                  loading = true
                  login()
                "
                solo
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                :type="show ? 'text' : 'password'"
                hint="Insert your password"
                counter
                @click:append="show = !show"
              >
                <template #prepend>
                  <v-tooltip bottom>
                    <template #activator="{ on }">
                      <v-icon v-on="on"> mdi-lock </v-icon>
                    </template>
                    Password
                  </v-tooltip>
                </template>
              </v-text-field>
              <div class="d-flex justify-center mt-5">
                <v-btn
                  color="normal"
                  :loading="loading"
                  :disabled="!valid"
                  @keyup.enter="
                    loading = true
                    login()
                  "
                  @click="
                    loading = true
                    login()
                  "
                >
                  Login
                </v-btn>
              </div>
            </v-container>
          </v-form>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  layout: "login",

  data() {
    return {
      loading: false,
      show: false,
      requiredRules: [(v) => !!v || "Name is required"],
      valid: false,
      formData: {
        email: "",
        password: "",
      },
    }
  },
  methods: {
    callSnack(text, color) {
      this.$store.dispatch("snackbarx/triggerSnackbar", {
        text: text,
        color: color,
      })
    },
    login() {
      this.$store.dispatch("login", this.formData).then((status) => {
        if (status == 200) {
          this.$store.dispatch("localStorage/getUser").then((status) => {
            if (status == 200) {
              this.callSnack("Logged Successfuly", "green")
              this.$router.push("/")
            }
          })
        } else if (status == 401) {
          this.callSnack(
            "401E: Authentication error, verify your credencials.",
            "error"
          )
          this.loading = false
        }
      })
    },
  },
}
</script>

<style lang="scss">
@import "~/assets/variables.scss";

.primaryC {
  color: $primary;
}
</style>
