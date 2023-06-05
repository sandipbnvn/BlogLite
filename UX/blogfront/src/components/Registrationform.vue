<template>
  <div class="register" style="margin-top:90px;">
    <div class="wrapper">
        <div class="logo">
            <img src="../assets/BlogLite_short.png" width="180" height="auto" alt="">
        </div>
        <div class="text-center mt-4 name">
            BlogLite
        </div>
        <small class="text-muted">Please Register Yourself</small>
        
        <form class="p-3 mt-3">
            <div class="form-field d-flex align-items-center">
                <span class="far fa-user"></span>
                <input type="email" name="email" id="email" placeholder="email" v-model='RegisterData.email'>
            </div>
            <div class="form-field d-flex align-items-center">
                <span class="far fa-user"></span>
                <input type="text" name="username" id="username" placeholder="username" v-model='RegisterData.username'>
            </div>
            <div class="form-field d-flex align-items-center">
                <span class="far fa-user"></span>
                <!-- <input type="text" name="aboutme" id="aboutme" placeholder="about me" v-model='loginData.email' cols="40" rows="5" word-break: break-word;> -->
                <textarea name="aboutme" id="aboutme" placeholder="about me" v-model='RegisterData.aboutme' cols="40" rows="5" style="background: transparent;border:none;outline: none;"></textarea>
            </div>                
            <div class="form-field d-flex align-items-center">
                <span class="fas fa-key"></span>
                <input type="password" name="password" id="password" placeholder="password" v-model='RegisterData.password'>
            </div>
            <div class="form-field d-flex align-items-center">
                <span class="fas fa-key"></span>
                <input type="password" name="retypepassword" id="retypepassword" placeholder="retype password" v-model='retypepassword'>
            </div>
            <button type="button" class="btn mt-3" style="background-color:#539d8b ;" @click="register">{{ registerButton }}</button>
        </form>
        <span style="padding:3px;color:red;">{{ errorData }}</span>
        <span style="padding:3px;color:#539d8b;">{{ infoData }}</span>
        <span v-if="passwords && notsubmitted" style="padding:3px;color:#539d8b;">{{ passwordsMatch }}</span>
        <span v-else style="padding:3px;color:red;">{{ passwordsMatch }}</span>
        </div>
  </div>
</template>


<script>
import RegisterFetch from '../RegisterFetch'

export default {
  name: 'Registrationform',
  data() {
    return {
      "passwords":true,
      notsubmitted:true,
      "errorData":'',
      retypepassword: '',
      "infoData":'',
      registerButton:"Register",
      RegisterData: {
        email: '',
        username: '',
        aboutme: '',
        password: '',
        
      },
    }
  },


  methods: {
    register() {
      this.notsubmitted=false;
      if (this.RegisterData.email==="") {
        this.errorData="Email is Required";
        return
      }
      if (!this.RegisterData.email.includes("@")) {
        this.errorData="Please enter a valid email id";
        return
      }
      if (this.RegisterData.username==="") {
        this.errorData="Username is Required";
        return
      }
      if (this.RegisterData.password==="") {
        this.errorData="Password is Required";
        return
      }
      if (this.retypepassword==="") {
        this.errorData="Please retype Password";
        return
      }
      if (this.RegisterData.password!="" && this.retypepassword!="" && this.RegisterData.password != this.retypepassword) {
        this.errorData="Passwords don't match";
        return
      }
      this.registerButton = "Registering"
      RegisterFetch(`http://127.0.0.1:5000/api/users`, {
        method: 'POST',
        body: JSON.stringify(this.RegisterData),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((data) => {
          console.log(data)
          this.infoData=data;
          this.errorData="";
          this.registerButton="Register";
        })
        .catch((err) => {
          this.registerButton="Register";
          console.log(err.message)
          this.errorData=err.message;
        })
    },
  },

  computed: {
    passwordsMatch: function() {
      if (this.RegisterData.password != "" && this.retypepassword !="" && this.RegisterData.password===this.retypepassword && this.notsubmitted) {
        this.passwords=true;return "passwords match!!"
      } 
      else if(this.RegisterData.password != "" && this.retypepassword !="" && this.RegisterData.password!=this.retypepassword && this.notsubmitted) { this.passwords=false;return "passwords don't match"}
      else {return ""}
    }
  }
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
    min-height: 00px;
    margin: 80px auto;
    /* margin-top: 10px; */
    padding: 60px 30px 30px 30px;
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

.wrapper .form-field input{
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

textarea::placeholder {
  text-align:bottom;
  font-size:large;
}

.wrapper .form-field textarea{
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

</style>
