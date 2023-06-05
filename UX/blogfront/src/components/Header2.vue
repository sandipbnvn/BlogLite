<template>
  <!-- <nav class="navbar bg-body-tertiary"> -->
  <nav class="navbar bg-body-tertiary1 fixed-top navbar-expand-lg">
    <!-- <nav class="navbar" style="background-color: #e3f2fd;"> -->
    <div class="container-fluid">
      <img alt="Vue logo" src="../assets/BlogLite_short.png" class="blogo">
      <h5 class="welcome-username">Welcome {{ username }}</h5>
      <!-- <button @click="call_celery">call celery</button> -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><router-link to='/feed'
              class="text-decoration-none nav-link text-white">Feed</router-link></li>
          <li class="nav-item"><router-link to='/create' class="text-decoration-none nav-link text-white">Write
              Post</router-link></li>
          <li class="nav-item"><router-link to='/selfprofile'
              class="text-decoration-none nav-link text-white">Profile</router-link></li>
          <li class="nav-item"><router-link to='/search'
              class="text-decoration-none nav-link text-white">Search</router-link></li>
          <li class="nav-item"><a class="text-decoration-none nav-link text-danger" @click="logout" href="#"
              style="color:#c9554b;font-weight:bold;">Logout</a></li>
          <!-- <li class="nav-item"><p class="text-decoration-none nav-link" style="color:#c9554b;font-weight:bold;">Sweta</p></li> -->
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import CommonFetch from '../CommonFetch'

export default {
  name: 'Header2',
  data() {
    return {
      'username': null
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push({ name: 'Home' })
    },
    call_celery() {
      CommonFetch(`http://127.0.0.1:5000/send_webhook/This message in from front end`, {
        method: 'GET',
        // headers: {
        //   'authentication_token': cred,
        // },
      })
        .then((data) => {
          console.log(data);
        })
        .catch((err) => {
          this.errorData = err.message;
          alert(err.message)
        })
    }
  },
  beforeMount() {
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) {
      this.$router.push({ name: 'Home' })
    }
    else {
      CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/0`, {
        method: 'GET',
        headers: {
          'authentication_token': cred,
        },
      })
        .then((data) => {
          this.username = data.username;
        })
        .catch((err) => {
          this.errorData = err.message;
          alert(err.message)
        })
  }
}
}
</script>


<style scoped>
nav {
  padding: 5px;
}

.bg-body-tertiary1 {
  --bs-bg-opacity: 1;
  /* background-color: rgba(var(--bs-tertiary-bg-rgb),var(--bs-bg-opacity))!important; */
  background-color: #539d8b;
  position: sticky;
}


nav a {
  padding: 10px;
  font-weight: normal;
  /* color:#f5c5be; */
  color: #f5c5be;
  border-radius: 25px;
  font-family: 'Poppins', sans-serif;
  letter-spacing: 0.3px;
  margin: 3px;
  /* font-size:small; */
}

nav a:hover {
  padding: 10px;
  font-weight: bold;
  /* color:#f5c5be; */
  color: #539d8b !important;
  background-color: #f5c5be;
}

nav a.router-link-exact-active {
  color: black !important;
  font-weight: bold;
  border-radius: 25px;
  background-color: #bfe3c8
    /* display: none; */
}

/* nav a.router-link-exact-active:hover {
    color: #f5c5be;
    display: none;
} */

.blogo {
  width: 60px;
  height: "auto";
  border-radius: 50%
}

.nav-item {
  margin-left: 5px;
}
.welcome-username {
/* background-color: yellow; */
max-width: 400px;
margin-left:10px;
margin-top:10px;
font-family: poppins;
color:white;
text-transform: capitalize;
}
</style>
