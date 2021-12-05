<template>
  <v-container id-list-md>
    <v-row align="center" justify="center">
      <v-col class="align-center">
        <v-row class="align-center" justify="center">
          <v-col cols="12" sm="10" md="10" lg="6" class="align-center">
            <v-alert v-if="showMsg === 'error'"
                     dismissible
                     :value="true"
                     type="error"
            >
              Please verify Task information.
            </v-alert>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="10" md="10" lg="6" class="align-center">
            <v-card class="login-card">
              <v-card-title>
                <span class="headline">{{pageTitle}}</span>
              </v-card-title>
              <v-spacer/>

              <v-card-text>
                <v-form ref="form" lazy-validation>
                  <v-container>

                    <v-text-field
                      v-model="movie.task_number"
                      label="Number"
                      required
                    />
                    <v-text-field
                      v-model="movie.task_name"
                      label="Name"
                      required
                    />
                    <v-text-field
                      v-model="movie.task_description"
                      label="Description"
                      required
                    />
                    <v-text-field
                      v-model="movie.deadline"
                      label="Deadline"
                      required
                    />
                  </v-container>
                  <v-btn v-if="!isUpdate" class="cyan darken-4 white--text" @click="createMovie">Save</v-btn>
                  <v-btn v-if="isUpdate" class="cyan darken-4 white--text" @click="updateMovie">Update</v-btn>
                  <v-btn class="white black--text" @click="cancelOperation">Cancel</v-btn>

                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>  
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
  import router from '../router';
  import {APIService} from '../http/APIService';
  const apiService = new APIService();

  export default {
    name: 'MovieCreate',
    components: {},
    data() {
      return {
        showError: false,
        movie: {},
        pageTitle: "Add New Task",
        isUpdate: false,
        showMsg: '',
      };
    },
    methods: {
      createMovie() {
        apiService.addNewMovie(this.movie).then(response => {
          if (response.status === 201) {
            this.movie = response.data;
            this.showMsg = "";
            router.push('/movie-list/new');
          }else{
            this.showMsg = "error";
          }
        }).catch(error => {
          if (error.response.status === 401) {
            router.push("/auth");
          }else if (error.response.status === 400) {
            this.showMsg = "error";
          }
        });
      },
      cancelOperation(){
        router.push("/movie-list");
      },
      updateMovie() {
        apiService.updateMovie(this.movie).then(response => {
          if (response.status === 200) {
            this.movie = response.data;
            router.push('/movie-list/update');
          }else{
            this.showMsg = "error";
          }
        }).catch(error => {
          if (error.response.status === 401) {
            router.push("/auth");
          }else if (error.response.status === 400) {
            this.showMsg = "error";
          }
        });
      }
    },
    mounted() {
      if (this.$route.params.pk) {
        this.pageTitle = "Edit Task";
        this.isUpdate = true;
        apiService.getMovie(this.$route.params.pk).then(response => {
          this.movie = response.data;
        }).catch(error => {
          if (error.response.status === 401) {
            router.push("/auth");
          }
        });
      }
    },
  }
</script>
<style scoped>
  .aform {
    margin-left: auto;
    width: 60%;
  }
</style>
