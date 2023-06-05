<template>
  <div class="login">
    <div class="wrapper">
      <div class="logo">
        <img src="../assets/BlogLite_short.png" width="200" height="200" alt="">
      </div>
      <div class="text-center mt-4 name">
        BlogLite
      </div>
      <small class="text-muted">Please login</small>

      <form class="p-3 mt-3">
        <div class="form-field d-flex align-items-center">
          <span class="far fa-user"></span>
          <input type="email" name="email" id="email" placeholder="email" v-model='loginData.email'>
        </div>
        <div class="form-field d-flex align-items-center">
          <span class="fas fa-key"></span>
          <input type="password" name="password" id="password" placeholder="password" v-model='loginData.password'>
        </div>
        <button type="button" class="btn mt-3" style="background-color:#539d8b;" @click="login">{{ this.buttonMessage }}</button>
      </form>
      <span style="padding:3px;color:red;">{{ this.errorData }}</span>
    </div>
  </div>
</template>


<script>
import AccessFetch from '../AccessFetch'

export default {
  name: 'Loginform',
  data() {
    return {
      "errorData": '',
      loginData: {
        email: '',
        password: '',

      },
      "buttonMessage":"Login"

    }
  },


  methods: {
    login() {
      
      if (this.loginData.email === "") {
        this.errorData = "Email is Required";
        return
      }
      if (this.loginData.password === "") {
        this.errorData = "Password is Required";
        return
      }
      this.buttonMessage = "Logging in"
      AccessFetch(`http://localhost:5000/login?include_auth_token`, {
        method: 'POST',
        body: JSON.stringify(this.loginData),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((data) => {
          localStorage.setItem('Authentication-Token', data.response.user['authentication_token'])
          // console.log(data.response.user['authentication_token'])
          this.errorData = "";
          this.buttonMessage = "Login";
          this.$router.push({ name: 'Feed' })
        })
        .catch((err) => {
          // console.log(err.message)
          this.buttonMessage = "Login";
          this.errorData = err.message;
        })
    },
  },
  // beforeCreate() {
  //   let cred = localStorage.getItem('Authentication-Token')
  //   if (cred) { this.$router.push({name: 'Feed'})}
  // }
}

</script>


<style scoped>
/* Importing fonts from Google */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* Reseting */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

body {
  background: #ecf0f3;
}

.wrapper {
  max-width: 350px;
  min-height: 500px;
  margin: 80px auto;
  padding: 40px 30px 30px 30px;
  background-color: #ecf0f3;
  border-radius: 15px;
  box-shadow: 13px 13px 20px #cbced1, -13px -13px 20px #fff;
}

.logo {
  width: 80px;
  margin: auto;
}

.logo img {
  width: 100%;
  height: 80px;
  object-fit: cover;
  border-radius: 50%;
  box-shadow: 0px 0px 3px #5f5f5f,
    0px 0px 0px 5px #ecf0f3,
    8px 8px 15px #a7aaa7,
    -8px -8px 15px #fff;
}

.wrapper .name {
  font-weight: 600;
  font-size: 1.4rem;
  letter-spacing: 1.3px;
  padding-left: 10px;
  color: #555;
}

.wrapper .form-field input {
  width: 100%;
  display: block;
  border: none;
  outline: none;
  background: none;
  font-size: 1.2rem;
  color: #666;
  padding: 10px 15px 10px 10px;
  /* border: 1px solid red; */
}

.wrapper .form-field {
  padding-left: 10px;
  margin-bottom: 20px;
  border-radius: 20px;
  box-shadow: inset 8px 8px 8px #cbced1, inset -8px -8px 8px #fff;
}

.wrapper .form-field .fas {
  color: #555;
}

.wrapper .btn {
  box-shadow: none;
  width: 50%;
  height: 40px;
  background-color: #03A9F4;
  color: #fff;
  border-radius: 25px;
  box-shadow: 3px 3px 3px #b1b1b1,
    -3px -3px 3px #fff;
  letter-spacing: 1.3px;
}

.wrapper .btn:hover {
  background-color: #039BE5;
}

.wrapper a {
  text-decoration: none;
  font-size: 0.8rem;
  color: #03A9F4;
}

.wrapper a:hover {
  color: #039BE5;
}

@media(max-width: 380px) {
  .wrapper {
    margin: 30px 20px;
    padding: 40px 15px 15px 15px;
  }
}
</style>
