<template>
  <v-container grid-list-md>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="6" md="4" lg="4">
        <v-card class="mx-auto elevation-6">
          <v-card-title>
            <span class="headline">Login</span>
          </v-card-title>
          <v-alert v-if="showMsg === 'error'"
              dismissible
              close-icon="mdi-close-circle"
              :value="true"
              type="error"
              icon="mdi-alert"
              dense
          >
            Invalid username or password. Please Try again.
          </v-alert>
          <v-spacer/>
          <v-card-text>
            <v-row
              align="center" 
              justify="center"
              v-if="loading"
            >
              <v-progress-circular
                :size="50"
                color="primary"
                indeterminate
              />
            </v-row>
            <v-form v-else ref="form" v-model="valid" lazy-validation>
              <v-container>
                <v-text-field
                  v-model="credentials.username"
                  :counter="70"
                  label="Username"
                  :rules="rules.username"
                  maxlength="70"
                  required
                  prepend-icon="mdi-account-circle"
                />

                <v-text-field
                  :type="showPassword ? 'text' : 'Password'"
                  v-model="credentials.password"
                  :counter="20"
                  label="Password"
                  :rules="rules.password"
                  maxlength="20"
                  required
                  prepend-icon="mdi-lock"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append="showPassword = ! showPassword"
                />

              </v-container>
              <v-btn class="info" :disabled="!valid" @click="login">Login</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

  import router from '../router';
  import {APIService} from '../http/APIService';
  const apiService = new APIService();

  export default {
    name: 'Auth',

    data: () => ({
      credentials: {},
      valid: true,
      showMsg: '',
      loading: false,
      rules: {
        username: [
          v => !!v || "Username is required",
          v => (v && v.length > 3) || "A username must be more than 3 characters long",
          v => /^[a-z0-9_]+$/.test(v) || "A username can only contain letters and digits"
        ],
        password: [
          v => !!v || "Password is required",
          v => (v && v.length > 7) || "The password must be longer than 7 characters"
        ]
      },
      showPassword: false,
    }),
    methods: {
      login() {
        // checking if the input is valid
        if (this.$refs.form.validate()) {
          this.loading = true;
            apiService.authenticateLogin(this.credentials).then((res)=>{
            localStorage.setItem('token', res.data.token);
            localStorage.setItem('isAuthenticates', JSON.stringify(true));
            localStorage.setItem('log_user', JSON.stringify(this.credentials.username));
            //router.push("/");
            //router.go(-1);
             window.location = "/"
          }).catch(e => {
            this.loading = false;
            localStorage.removeItem('isAuthenticates');
            localStorage.removeItem('log_user');
            localStorage.removeItem('token');
           // router.go(-1);
            this.showMsg = 'error';
          })
        }
      }
    }
  }
</script>
