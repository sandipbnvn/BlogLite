<template>
  <div class="feed">
    <div class="fixed">
      <Header2 />
    </div>
    <h2 v-cloak class="welcome-user">Welcome to your feed, {{ user.username }}</h2>
    <div class="cotainer no-posts" v-if="posts.length == 0">
      <h1 class="no-post-prompt">No Posts Yet, Follow Users to See their posts here</h1>
      <button class="btn btn-warning add-post" @click="goToSearch">Add People</button>
    </div>
    <Post :post_data="posts" />
  </div>
</template>

<script>
// @ is an alias to /src
import Header2 from '@/components/Header2.vue'
import Post from '@/components/Post.vue'
import CommonFetch from '../CommonFetch'

export default {
  name: 'FeedView',
  components: {
    Header2,
    Post,
  },
  data() {
    return {
      "posts": {},
      "user": {},
    }
  },
  methods: {
    goToSearch() {
      this.$router.push({ name: 'Search' })
    }
  },
  beforeCreate() {
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) {
      this.$router.push({ name: 'Home' })
    }
    else {
      CommonFetch(`http://127.0.0.1:5000/api/extra/all_post_short/0`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.posts = data;
          localStorage.setItem("userPosts", JSON.stringify(data))
        })
        .catch((err) => {
          // console.log(err.message)
          this.errorData = err.message;
          alert(err.message)
        })

      CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/0`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.user = data;
          localStorage.setItem("user", JSON.stringify(data))
          localStorage.setItem("user_id", JSON.stringify(data.id))
          // localStorage.setItem("username", JSON.stringify(data.username))
        })
        .catch((err) => {
          // console.log(err.message)
          this.errorData = err.message;
          // alert(err.message)
        })
    }
  },
  beforeMount() {
    // console.log("feed mounted")
    let cred = localStorage.getItem('Authentication-Token')
    let user = localStorage.getItem('user')
    let posts = localStorage.getItem('userPosts')
    if (!cred) { this.$router.push({ name: 'Home' }) }
    else if (user && posts) {
      this.user = JSON.parse(user)
      this.posts = JSON.parse(posts)
    }
    else {
      CommonFetch(`http://127.0.0.1:5000/api/extra/all_post_short/0`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.posts = data;
          localStorage.setItem("userPosts", JSON.stringify(data))
        })
        .catch((err) => {
          // console.log(err.message)
          this.errorData = err.message;
          alert(err.message)
        })

      CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/0`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.user = data;
          localStorage.setItem("user", JSON.stringify(data))
        })
        .catch((err) => {
          // console.log(err.message)
          this.errorData = err.message;
          alert(err.message)
        })
    }
  }
}
</script>

<style>
[v-clock] {
  display: none;
}

.fixed {
  position: fixed;
  top: 0;
  width: 100%;
}

.welcome-user {
  margin-top: 90px;
  text-transform: capitalize;
  font-family: poppins;
  width: 100%;
  text-align: left;
  padding-left: 20px;
  font-weight: 100;

}

.no-posts {
  display: grid;
  align-items: center;
  place-content: center;
  position: relative;
  height: 100%;
}

.no-post-prompt {
  margin-top: 150px;
  font-family: poppins;
  font-weight: 300;
}

.add-post {
  font-weight: 300 !important;
  width: 40%;
  margin-left: 30%;
  margin-right: 30%;
  border-radius: 10px;
  font-family: poppins;
  margin-top: 20px;
}
</style>
