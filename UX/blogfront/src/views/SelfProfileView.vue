<template>
  <div class="feed">
    <div class="fixed">
      <Header2 />
    </div>
    <div class="welcome-user">
      <div class="container">
        <div class="row d-flex justify-content-center">
          <!-- <div class="col-sm d-flex justify-content-center"> -->
          <h2 v-if="user.username != null" style="font-weight:200;">Welcome to your Profile,
            {{
              user.username
            }}</h2>
          <button class="btn btn-primary downloadButton" @click="downloadFile"
            style="max-width:200px;border-radius: 20px;background-color: #539d8b !important;margin:5px 10px;">Download
            all
            posts</button>

          <button class="btn btn-primary downloadButton"
            style="max-width:200px;border-radius: 20px;background-color: #539d8b !important;margin:5px 10px;"
            @click="sendPosts">Email Me Posts
          </button>
          <div class="form-field d-flex align-items-center excel-input">
            <form class="excel-input-form">
              <label for="fileInput" class="excel-input-label">Upload Posts Through Excel</label>
              <input name="fileInput" type="file"
                title="upload only csv files with two columns with headers 'title' and 'description'" accept=".csv"
                @change="onFileChange" style="max-width:330px;" />
              <button type="button" class="btn btn-primary submit-excel" @click="submitFile">Submit</button>
            </form>
          </div>


          <!-- </div> -->
        </div>
      </div>
    </div>
    <Loading v-if="not_loaded" />
    <UserSummary v-else :user="user" style="padding-top:10px !important;" />
    <div class="cotainer no-posts" v-if="posts && posts.length != 0">
      <!-- <h1 class="post-prompt" >Posts</h1> -->
    </div>
    <div class="cotainer no-posts" v-if="posts && posts.length == 0">
      <h1 class="no-post-prompt">No Posts Yet</h1>
      <button class="btn btn-warning add-post" @click="writeFirst">Write First
        Post</button>
    </div>
    <Post :post_data="posts" @postDeleteReceived="deletePost" />
  </div>
</template>

<script>
// @ is an alias to /src
import Header2 from '@/components/Header2.vue'
import Loading from '@/components/Loading.vue'
import Post from '@/components/Post.vue'
import UserSummary from '@/components/UserSummary.vue'
import CommonFetch from '../CommonFetch'

export default {
  name: 'SelfProfileView',
  components: {
    Header2,
    UserSummary,
    Post,
    Loading,
  },
  data() {
    return {
      "user": {},
      "user_id": null,
      "posts": {},
      "errorData": "",
      "not_loaded": true,
      selectedFile: null

    }
  },
  methods: {
    deletePost(postId) {
      // console.log('ProfileView heard the event and triggered deletePost method')
      this.posts = this.posts.filter(function (item) {
        return item.id != postId
      });
      this.user.posts_size = this.user.posts_size - 1
      // console.log('parent data modified')
    },
    writeFirst() {
      this.$router.push({ name: 'Create' })
    },
    async downloadFile() {
      let cred = localStorage.getItem('Authentication-Token')
      try {
        const response = await fetch('http://127.0.0.1:5000/api/extra/export_posts', {
          method: 'GET',
          headers: {
            'authentication_token': cred,
          },
        });
        const fileBlob = await response.blob();
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(fileBlob);
        // link.download = 'fileName.ext';
        link.click();
        window.URL.revokeObjectURL(link.href);
      } catch (error) {
        console.error(error);
      }
    },
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
    },
    async submitFile() {
      let cred = localStorage.getItem('Authentication-Token')
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      CommonFetch('http://127.0.0.1:5000/uploadPosts', {
        method: 'POST',
        body: formData,
        headers: {
          'authentication_token': cred,
        }
      }).then((data) => {
        alert(data.message);

        setTimeout(() => {
          location.reload();
        }, 500);

      }
      ).catch((err) => console.log(err))
    },
    async sendPosts() {
      let cred = localStorage.getItem('Authentication-Token')
      CommonFetch('http://127.0.0.1:5000/sendPosts', {
        headers: {
          'authentication_token': cred,
        }
      }).then((data) => { alert(data.message) }
      ).catch((err) => console.log(err))
    }
  }
  ,

  beforeCreate() {
    // console.log('SelfProfileView Created')
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) { this.$router.push({ name: 'Home' }) }
    else {
      if (localStorage.getItem('user_id')) {
        this.user_id = JSON.parse(localStorage.getItem('user_id')) //fetching user_id of active user from local storage
      }
      else {
        this.$router.push({ name: 'Home' })
      }

      if (this.user_id) {
        CommonFetch(`http://127.0.0.1:5000/api/extra/all_post_short/${this.user_id}`, {
          method: 'GET',
          headers: {
            'authentication_token': cred,
          },
        })
          .then((data) => {
            this.posts = data; //fetching all posts of the user
          })
          .catch((err) => {
            this.errorData = err.message;
          })
      }

      if (this.user_id) {
        CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/${this.user_id}`, {
          method: 'GET',
          headers: {
            'authentication_token': cred,
          },
        })
          .then((data) => {
            this.user = data; //fetching user info of the user
            this.not_loaded = false;
          })
          .catch((err) => {
            this.errorData = err.message;
          })
      }


    }
  },
  beforeMount() {
    // console.log('SelfProfileView Mounted')
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) { this.$router.push({ name: 'Home' }) }
    else {
      if (localStorage.getItem('user_id')) {
        this.user_id = JSON.parse(localStorage.getItem('user_id')) //fetching user_id of active user from local storage
      }
      else {
        this.$router.push({ name: 'Home' })
      }

      if (this.user_id) {
        CommonFetch(`http://127.0.0.1:5000/api/extra/all_post_short/${this.user_id}`, {
          method: 'GET',
          headers: {
            'authentication_token': cred,
          },
        })
          .then((data) => {
            this.posts = data; //fetching all posts of the user
          })
          .catch((err) => {
            this.errorData = err.message;
            alert(err.message)
          })
      }

      if (this.user_id) {
        CommonFetch(`http://127.0.0.1:5000/api/extra/user_info_short/${this.user_id}`, {
          method: 'GET',
          headers: {
            'authentication_token': cred,
          },
        })
          .then((data) => {
            this.user = data; //fetching user info of the user
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

.excel-input {
  /* background-color: yellow; */
  max-width: 500px;
}

.submit-excel {
  border-radius: 25px;
  background-color: #539d8b;
}


.excel-input-form {
  /* background-color: yellow; */
  margin-left: 30px;
}

.excel-input-label {
  /* background-color:yellow; */
  padding-left: 90px;
}

@media(max-width: 380px) {
  .excel-input-label {
    /* background-color:yellow; */
    padding-left: 10px;
  }

  .submit-excel {
    margin-left: 90px;
    margin-top: 10px;
  }
}
</style>
