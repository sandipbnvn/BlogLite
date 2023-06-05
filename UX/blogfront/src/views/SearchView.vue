<template>
  <div class="search">
    <div class="fixed">
      <header2 />
    </div>


    <div class="search">
      <div class="wrapper" style="margin-bottom:0px !important;">
        <form class="p-0 mt-0">
          <div class="form-field d-flex align-items-center">
            <span class="far fa-user"></span>
            <input type="text" name="userSearch" id="userSearch" placeholder="Search User by Name"
              v-model="search_text">
          </div>
        </form>
      </div>
    </div>




    <div style="margin-top:40px;">
      <div v-for="user in filteredUsers" :key="user.id">
        <UserSummaryShort v-if="search_text.length > 0" :user="user" @unfollowed_user="updateUserUnfollowed"
          @followed_user="updateUserFollowed" />
      </div>
      <!-- <h1 v-if="search_text.length == 0">Search Results Will Populate Here As You Start Typing</h1> -->

      <div class="search"  v-if="search_text.length == 0">
        <!-- <div class="wrapper" style="margin-bottom:0px !important;"> -->
              <span class="far fa-user"></span>
              <h4 style="font-family:poppins;">Search Results Will Populate Here As You Start Typing</h4>
            <!-- </div> -->
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
  name: 'SearchView',
  components: {
    Header2,
    UserSummaryShort
  },
  data() {
    return {
      users: {},
      search_text: '',
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
  computed: {
    filteredUsers() {
      return Object.values(this.users).filter(user => user.username.toLowerCase().includes(this.search_text.toLowerCase()))
    }
  },
  beforeMount() {
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) { this.$router.push({ name: 'Home' }) }
    CommonFetch(`http://127.0.0.1:5000/api/extra/all_user_info_short`, {
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
    margin-top: 90px !important;
    /* padding: 40px 0px 15px 0px !important; */
  }
}

.wrapper {
  max-width: 800px !important;
}
</style>
