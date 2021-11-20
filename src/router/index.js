import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Auth from '@/components/Auth'
import MovieList from '@/components/MovieList'
import MovieCreate from '@/components/MovieCreate'


Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/movie-list',
      name: 'MovieList',
      component: MovieList
    },
    {
      path: '/movie-list/:msg',
      name: 'MovieUpdatedList',
      component: MovieList
    },
    {
      path: '/movie-create',
      name: 'MovieCreate',
      component: MovieCreate
    },
    {
      path: '/movie-create/:pk',
      name: 'MovieUpdate',
      component: MovieCreate
    },

    {
      path: '/auth',
      name: 'Auth',
      component: Auth
    }
  ]
})
