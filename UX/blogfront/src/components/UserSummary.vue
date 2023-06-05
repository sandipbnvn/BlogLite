<template>
  <div class="contatiner UserSummary" style="margin-top:0px !important;">
    <div class="summary">
      <div class="wrapper" style="margin-top:20px !important;">
        <div class="p-1 mt-0" style="margin-bottom:30px;">
          <h4 class="text-muted summary" style="text-align:center;">User Summary</h4>
        </div>
        <div class="headings">
          <small>Name:</small>
        </div>
        <div class="container-fluid">
          <div class="row">
            <div class="samll-heading col-sm" style="margin-left:0px;">
              <div class="d-flex align-items-left" style="margin-left:0px;padding-left:0px !important;">
                <h2 class="card-title user-name user-info"
                  style=" text-transform: capitalize; margin-left:0px;padding-left:0px;">{{ user.username }}</h2>
                <small v-if="user.following_user" class="follows-user">follows you</small>
              </div>
            </div>
            <div class="samll-heading col-sm">
              <div class="d-flex justify-content-end follow-btn-flex" style="margin-top:0px;">
                <button class="btn btn-info" style="background-color:#539d8b;"
                  v-if="!user.user_following && user.id != this.current_user_id"
                  @click="followUser(user.id)">Follow</button>
                <button class="btn btn-info" style="background-color:#f5c5be;min-width: 110px;border-style: 0px;"
                  v-if="user.user_following" @click="unfollowUser(user.id)">Unfollow</button>
              </div>
            </div>
          </div>

        </div>
        <div class="headings">
          <small>Email ID:</small>
        </div>
        <div class="d-flex align-items-left">
          <h2 class="card-title user-name user-info">{{ user.email }}</h2>
        </div>
        <div class="headings" style="margin-bottom:0px !important;">
          <small>About Me:</small>
        </div>
        <div class="aboutme">
          <small>{{ user.aboutme }}</small>
        </div>
        <div class="container-fluid">
          <div class="row">
            <div class="samll-heading col-sm">
              <div class="headings">
                <small>Follows:</small>
              </div>
              <div class="d-flex align-items-left">
                <h2 class="card-title user-name user-info" @click="goToFollowList" style="cursor:pointer;">{{ user.followed_size }}</h2>
              </div>
            </div>
            <div class="samll-heading col-sm">
              <div class="headings">
                <small>Followed By:</small>
              </div>
              <div class="d-flex align-items-left">
                <h2 class="card-title user-name user-info" @click="goToFollowedList" style="cursor:pointer;">{{ user.followers_size }}</h2>
              </div>
            </div>
            <div class="samll-heading col-sm">
              <div class="headings">
                <small>Total Posts:</small>
              </div>
              <div class="d-flex align-items-left">
                <h2 class="card-title user-name user-info">{{ user.posts_size }}</h2>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import CommonFetch from '../CommonFetch'

export default {
  name: 'UserSummary',
  data() {
    return {
      "errorData": '',
      "current_user_id": '',
    }
  },
  props: ['user'],
  beforeMount() {
    // console.log("uss mounted")
    let user_id = localStorage.getItem("user_id")
    if (user_id) {
      this.current_user_id = user_id;
    }
  },
  methods: {
    followUser(id) {
      let cred = localStorage.getItem('Authentication-Token')
      if (!cred) { this.$router.push({ name: 'Home' }) }
      else {
        CommonFetch(`http://127.0.0.1:5000/api/users/follow/${id}`, {
          method: 'PUT',
          headers: {
            'authentication_token': cred,
          },
        })
          .then((data) => {
            this.user.followers_size = this.user.followers_size + 1
            this.$emit("followed_user", id);
          })
          .catch((err) => {
            // console.log(err.message)
            this.errorData = err.message;
            alert(err.message)
          })
      }
    },
    unfollowUser(id) {
      let cred = localStorage.getItem('Authentication-Token')
      if (!cred) { this.$router.push({ name: 'Home' }) }
      else {
        CommonFetch(`http://127.0.0.1:5000/api/users/unfollow/${id}`, {
          method: 'PUT',
          headers: {
            'authentication_token': cred,
          },
        })
          .then((data) => {
            this.user.followers_size = this.user.followers_size - 1
            this.$emit("unfollowed_user", id);
          })
          .catch((err) => {
            // console.log(err.message)
            this.errorData = err.message;
            alert(err.message)
          })
      }
    },
    goToFollowList() {
      this.$router.push(`/follow/follows/${this.user.id}/${this.user.username}`)
    },
    goToFollowedList() {
      this.$router.push(`/follow/is followed by/${this.user.id}/${this.user.username}`)
    }

  }
}



</script>


<style scoped>
/* Importing fonts from Google */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* Reseting */
* {
  margin: 7px;
  padding: 0px;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

body {
  background: #ecf0f3;
}

.wrapper {
  max-width: 1000px;
  min-height: 450px;
  margin: 80px auto;
  padding: 40px 30px 30px 30px;
  background-color: #ecf0f3;
  border-radius: 15px;
  box-shadow: 13px 13px 20px #cbced1, -13px -13px 20px #fff;
  margin-bottom: 20px !important;
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
    /* margin: 30px 30px !important;
    padding: 40px 15px 15px 15px; */
    margin: 30px 0px !important;
    padding: 40px 5px 15px 5px;
  }

  .container-fluid {
    padding-left: 0px !important;
    margin-left: 0px !important;
  }

  .samll-heading {
    padding-left: 0px !important;
    margin-left: 0px !important;
  }

  .follow-btn-flex {
    margin-right:120px;
}
}

.summary {
  text-align: left;
  font-weight: 700;
  /* background-color: orange; */
  font-family: poppins;
  margin-bottom: 0px;
  /* color: #f5c5be !important; */
  color: black !important;
}

.UserSummary {
  margin-top: 20px;
  /* margin-left:20px !important; */
  /* margin-right:20px !important; */
  min-width: 150px !important;
}

.headings {
  color: grey;
  margin-left: 5 px;
  margin-bottom: 0px !important;
  padding-bottom: 0px !important;
}

.user-info {
  margin-left: 5 px;
  font-weight: 700;
  /* background-color: orange; */
  font-family: poppins;
  margin-bottom: 20px;
  color: #539d8b;
  margin-top: 0px !important;
  padding-top: 0px !important;
}

.aboutme {
  color: #1a1919;
  margin-top: 0px;
  padding-top: 0px;
  margin-bottom: 20px;
}

.small-heading {
  width: 50% !important;

}

.follows-user {
  background-color: #ccc;
  margin-top: 0px;
  color: #606060;
  margin-left: 5px;
  padding: 5px 5px;
  margin-bottom: 20px;
  align-items: top;
  border-radius: 15px;
  padding-bottom: 0px !important;
  padding-top: 7px;
}
</style>
