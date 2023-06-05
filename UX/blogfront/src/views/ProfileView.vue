<template>
  <div class="feed">
    <div class="fixed">
      <Header2 style="z-index: 2 !important" />
    </div>
    <div class="welcome-user">
      <h2 v-if="this.$route.params.id == 0 && user.username != null" style="font-weight:200;">Welcome to your Profile,
        {{
          user.username
        }}</h2>
    </div>
    <UserSummary :user="user" style="padding-top:10px !important;" @unfollowed_user="updateUserUnfollowed"
      @followed_user="updateUserFollowed" />

    <div class="no-posts" v-if="posts && posts.length != 0" style="z-index: 1 !important">
      <!-- <h1 class="post-prompt" v-if="posts && posts.length!=0" style="z-index: 1 !important">Posts</h1> -->
    </div>
    <div class="no-posts" v-if="posts && posts.length == 0">
      <h1 class="no-post-prompt">No Posts Yet</h1>
      <button class="btn btn-warning add-post" v-if="this.$route.params.id === 0" @click="writeFirst">Write First
        Post</button>
    </div>
    <Post :post_data="posts" @postDeleteReceived="deletePost" />
  </div>
</template>

<script>
// @ is an alias to /src
import Header2 from '@/components/Header2.vue'
import Post from '@/components/Post.vue'
import UserSummary from '@/components/UserSummary.vue'
import CommonFetch from '../CommonFetch'

export default {
  name: 'ProfileView',
  components: {
    Header2,
    UserSummary,
    Post,
  },
  data() {
    return {
      "user": {},
      "user_id": null,
      "posts": null,
      "errorData": ""
    }
  },
  methods: {
    deletePost(postId) {
      console.log('ProfileView heard the event and triggered deletePost method')
      this.posts = this.posts.filter(function (item) {
        return item.id != postId
      });
      // console.log('parent data modified')
    },
    updateUserFollowed(id) {
      this.user.user_following = true;
    }
    ,
    updateUserUnfollowed(id) {
      this.user.user_following = false;
    }
  },

  beforeCreate() {
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) { this.$router.push({ name: 'Home' }) }
    else {
      if (this.$route.params.id === "0") {
        user_stored = localStorage.getItem('user')
        if (user_stored) {
          this.user_id = JSON.parse(user_stored).id
        }
        else {
          CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/0`, {
            method: 'GET',
            headers: {
              'authentication_token': cred,
            },
          })
            .then((data) => {
              this.user = data;
              this.user_id = data.user_d;
              localStorage.setItem("user", JSON.stringify(data))
            })
            .catch((err) => {
              // console.log(err.message)
              this.errorData = err.message;
            })
        }
      }
      else {
        this.user_id = parseInt(this.$route.params.id)
      }

      CommonFetch(`http://127.0.0.1:5000/api/extra/all_post_short/${this.user_id
        }`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.posts = data;
        })
        .catch((err) => {
          this.errorData = err.message;
        })


      CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/${this.user_id}`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.user = data;
        })
        .catch((err) => {
          this.errorData = err.message;
        })

      CommonFetch(`http://127.0.0.1:5000/api/extra/all_user_info_short`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.user_short = data;
        })
        .catch((err) => {
          // console.log(err.message)
          this.errorData = err.message;
          alert(err.message)
        })

    }
  },
  beforeMount() {
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) { this.$router.push({ name: 'Home' }) }
    else {
      if (this.$route.params.id === "0") {
        user_stored = localStorage.getItem('user')
        if (user_stored) {
          this.user_id = JSON.parse(user_stored).id
        }
        else {
          CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/0`, {
            method: 'GET',
            headers: {
              'authentication_token': cred,
            },
          })
            .then((data) => {
              this.user = data;
              this.user_id = data.user_d;
              localStorage.setItem("user", JSON.stringify(data))
            })
            .catch((err) => {
              // console.log(err.message)
              this.errorData = err.message;
              alert(err.message)
            })
        }
      }
      else {
        this.user_id = parseInt(this.$route.params.id)
      }

      CommonFetch(`http://127.0.0.1:5000/api/extra/all_post_short/${this.user_id
        }`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.posts = data;
        })
        .catch((err) => {
          this.errorData = err.message;
        })

      if (this.user == {}) {
        CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/${this.user_id}`, {
          method: 'GET',
          headers: {
            'authentication_token': cred,
          },
        })
          .then((data) => {
            this.user = data;
          })
          .catch((err) => {
            this.errorData = err.message;
          })
      }
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
  margin-top: 70px;
  text-transform: capitalize;
  font-family: poppins;
  width: 100%;
  text-align: left;
  padding-left: 20px;
  font-weight: 100;
  margin-bottom: 10px !important;

}

.no-posts {
  display: grid;
  align-items: center;
  place-content: center;
  position: relative;
  height: 100%;
}

.no-post-prompt {
  margin-top: 10px;
  font-family: poppins;
  font-weight: 300;
}

.post-prompt {
  margin-top: 0px !important;
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
