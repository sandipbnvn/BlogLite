import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import FeedView from '../views/FeedView.vue'
import SearchView from '../views/SearchView.vue'
import CreateView from '../views/CreateView.vue'
import ProfileView from '../views/ProfileView.vue'
import SelfProfileView from '../views/SelfProfileView.vue'
import UpdateView from '../views/UpdateView.vue'
import FollowView from '../views/FollowView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'Resigster',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/RegisterView.vue')
    component: RegisterView
  },
  {
    path: '/feed',
    name: 'Feed',
    component: FeedView
  },
  {
    path: '/search',
    name: 'Search',
    component: SearchView
  },
  {
    path: '/create',
    name: 'Create',
    component: CreateView
  },
  {
    path: '/profile/:id',
    name: 'Profile',
    component: ProfileView
  },
  {
    path: '/update',
    name: 'Update',
    component: UpdateView
  },
  {
    path: '/selfprofile',
    name: 'SelfProfile',
    component: SelfProfileView
  },
  {
    path: '/follow/:list/:id/:username',
    name: 'FollowView',
    component: FollowView,

  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
