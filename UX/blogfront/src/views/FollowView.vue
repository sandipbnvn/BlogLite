<template>
  <div class="search">
    <div class="fixed">
      <header2 />
    </div>


    <div class="search">
      <div class="wrapper" style="margin-bottom:0px !important;">
            <h4 style="text-transform: capitalize;font-family: poppins;">{{ username }} {{ list }}</h4>
      </div>
    </div>




    <div style="margin-top:40px;">
      <div v-for="user in users" :key="user.id">
        <UserSummaryShort :user="user" @unfollowed_user="updateUserUnfollowed" @followed_user="updateUserFollowed"/>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import Loginform from '@/components/Loginform.vue'
// import Header from '@/components/Header.vue'
import Header2 from '@/components/Header2.vue'
import UserSummaryShort from '@/components/UserSummaryShort.vue'
import CommonFetch from '../CommonFetch'

export default {
  name: 'FollowView',
  components: {
    Header2,
    UserSummaryShort
  },
  data() {
    return {
      users: {},
      user_id:'',
      list:'',
      username:'',
    }
  },
  methods: {
    updateUserFollowed(id) {
      for (let i = 0; i < this.users.length; i++) {
            if (this.users[i].id === id) {
              this.users[i].user_following = true;
            }
          }
    },
    updateUserUnfollowed(id) {
      for (let i = 0; i < this.users.length; i++) {
            if (this.users[i].id === id) {
              this.users[i].user_following = false;
            }
          }
    }
  },

  beforeMount() {
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) { this.$router.push({ name: 'Home' }) }
    this.user_id = this.$route.params.id
    this.list = this.$route.params.list
    this.username = this.$route.params.username
    CommonFetch(`http://127.0.0.1:5000//api/extra/all_user_info_short_follow/${this.list}/${this.user_id}`, {
      method: 'GET',
      headers: {
        'authentication_token': cred,
      },
    })
      .then((data) => {
        this.users = data;
      })
      .catch((err) => {
        // console.log(err.message)
        this.errorData = err.message;
        alert(err.message)
      })
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

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
@media(max-width: 380px) {
  .wrapper {
    margin-left: 10px !important;
    margin-right: 10px !important;
    margin-top:90px !important;
    /* padding: 40px 0px 15px 0px !important; */
  }
}

.wrapper {
  max-width: 800px !important;
}
</style>
