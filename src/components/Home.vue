<template>
  <v-main>
    <!-- Welcome -->
    <v-container fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" align="center" justify="center">
          <blockquote>
            Welcome! <br> <br>
            Here is a preview of your task list. Click the task tab for more details.
            <footer>
              <small>
                
              </small>
            </footer>
          </blockquote>
        </v-col>
        <v-col  cols="12" md="10" lg="10" align="center" justify="center">
          <v-alert v-if="showMsg === 'new'"
                   dismissible
                   :value="true"
                   type="success"
          >
            New task has been added.
          </v-alert>
          <v-alert v-if="showMsg === 'update'" dismissible
                   :value="true"
                   type="success"
          >
            Task information has been updated.
          </v-alert>
          <v-alert v-if="showMsg === 'deleted'" dismissible
                   :value="true"
                   type="success"
          >
            Selected Task has been deleted.
          </v-alert>
        </v-col>
      </v-row>

      <!-- Data table -->
      <v-row align="center" justify="center">
        <v-col cols="12" md="10" v-resize="onResize">
            <v-data-table
              :headers="headers"
              :items="movies"
              class="elevation-1"
              style="max-height: 300px; overflow-y: auto"
              v-if="isMobile"
            >
                    <template v-slot:item="props">
                      <tr>
                        <td align="left">{{ props.item.task_number }}</td>
                        <td align="left">{{ props.item.task_name }}</td>
                        <td align="left">{{ props.item.task_description }}</td>
                        <td align="left">{{ props.item.deadline }}</td>
                        <td align="center"><v-icon @click="updateMovie(props.item)">mdi-pencil</v-icon></td>
                        <td align="center"><v-icon @click="deleteMovie(props.item)">mdi-delete</v-icon></td>
                      </tr>  
                    </template>
              </v-data-table>
              <v-data-iterator 
                :items="movies"
                hide-default-footer
                v-else
              >
                <template v-slot:default="{ items, isExpanded, expand }">
                  <v-row>
                    <v-col
                      v-for="item in items"
                      :key="item.name"
                      cols="12"
                    >
                      <v-card>
                        <v-card-title class="pb-0 pt-0 pl-0">
                          <v-col cols="9" class="text-left body-2 text-truncate">{{ item.name }}</v-col>
                          <v-col cols="3" class="text-center">
                            <v-card-actions>
                              <v-icon @click="updateMovie(item)" class="small">mdi-pencil</v-icon>
                              <v-icon @click="deleteMovie(item)" class="small">mdi-delete</v-icon>
                              <v-icon @click.native="expand(item, !isExpanded(item))" class="small">mdi-dots-horizontal</v-icon>
                            </v-card-actions>
                          </v-col>
                        </v-card-title>
                        <v-divider></v-divider>

                        <v-list v-show="isExpanded(item)" dense>
                          <v-list-item>
                            <v-list-item-content class="align-end">{{ item.description }}</v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>Description:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.year }}</v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>Deadline:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.rating }}</v-list-item-content>
                          </v-list-item>
                        </v-list>
                      </v-card>
                    </v-col>
                  </v-row>
                </template>     
              </v-data-iterator>  
        </v-col>  

            
      </v-row>
    </v-container>  
  </v-main>
</template>


<script>

  import router from '../router';
  import {APIService} from '../http/APIService';
  const apiService = new APIService();

  export default {
    name: "MovieList",
    data: () => ({
      movies: [],
      validUserName: "Guest",
      movieSize: 0,
      showMsg: '',
      isMobile: false,
      headers: [
        {text: 'Number', sortable: false, align: 'left'},
        {text: 'Name', sortable: false, align: 'left',},
        {text: 'Description', sortable: false, align: 'left',},
        {text: 'Deadline', sortable: false, align: 'left',},
        {text: 'Update', sortable: false, align: 'center',},
        {text: 'Delete', sortable: false, align: 'center',},
      ],

    }),
    mounted() {
      this.getMovies();
      this.showMessages();
    },
    methods: {
      onResize() {
          if (window.innerWidth > 600)
            this.isMobile = true;
          else  
            this.isMobile = false;
        },
      showMessages(){
        console.log(this.$route.params.msg)
        if (this.$route.params.msg) {
          this.showMsg = this.$route.params.msg;
        }
      },
      getMovies() {
        apiService.getMovieList().then(response => {
          this.movies = response.data.data;
          console.log(response.data.data);
          console.log(response.data);
          this.movieSize = this.movies.length;
          if (localStorage.getItem("isAuthenticates")
            && JSON.parse(localStorage.getItem("isAuthenticates")) === true) {
            this.validUserName = JSON.parse(localStorage.getItem("log_user"));
          }
        }).catch(error => {
          if (error.response.status === 401) {
            localStorage.removeItem('isAuthenticates');
            localStorage.removeItem('log_user');
            localStorage.removeItem('token');
            router.push("/auth");
          }
        });
      },
      addNewMovie() {
        if (localStorage.getItem("isAuthenticates")
          && JSON.parse(localStorage.getItem("isAuthenticates")) === true) {
          router.push('/movie-create');
        } else {
          router.push("/auth");
        }
      },
      updateMovie(movie) {
        router.push('/movie-create/' + movie.pk);
      },
      deleteMovie(movie) {
        apiService.deleteMovie(movie.pk).then(response => {
          if (response.status === 204) {
            router.push('/movie-list/deleted/')
            this.getMovies()
          }
        }).catch(error => {
          if (error.response.status === 401) {
            localStorage.removeItem('isAuthenticates');
            localStorage.removeItem('log_user');
            localStorage.removeItem('token');
            router.push("/auth");
          }
        });
      }
    }
  };
</script>
