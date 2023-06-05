<template>
  <div class="singlepost">
    <div class="wrapper">
      <div class="d-flex align-items-left">
        <h2 class="card-title user-name" style="cursor:pointer;" @click="gotoprofile">{{ post.username }}</h2>
      </div>
      <div class="d-flex align-items-left user-email">
        <p style="margin-bottom:0px !important;">{{ post.email }}</p>
      </div>

      <div class="d-flex align-items-left">
        <h4 class="post-title">{{ post.title }}</h4>
      </div>
      <div class="d-flex align-items-left post_date">
        <Dateformatting :create_date="post.creation_date" class="post_date" />
      </div>
      <div class="d-flex align-items-left" style="text-align:left">
        <p class="post-description">{{ post.description }}</p>
      </div>
      <div class="d-flex align-items-center">
        <img class="card-img-bottom" v-if="post.imageURL != null"
          :src="require(`@/assets/uploded_images/${post.imageURL}`)" alt="Card image"
          style="width:100%;border-radius: 10px;" />
      </div>
      <div class="d-flex align-items-left" style="text-align:left" v-if="active_user_post">
        <button class="btn btn-warning post-edit" style="background-color:#e1b382"
          @click="updatePost(post)">Edit</button>
        <button class="btn btn-warning post-delete-prompt" style="background-color:#ff5e6c"
          @click="deletePressed = true;" v-if="!deletePressed">Delete</button>
        <button class="btn btn-warning post-delete" style="background-color:#ff5e6c !important"
          @click="deletePost(post.id)" v-if="deletePressed">Sure?</button>
        <button class="btn btn-warning post-delete" style="background-color:#ff5e6c !important"
          @click="deletePressed = false;" v-if="deletePressed">No</button>
        <p>{{ this.errorData }}</p>

      </div>
      <div class="d-flex align-items-left" style="text-align:left">
      </div>
    </div>
  </div>

</template>

<script>
import CommonFetch from '../CommonFetch'
import Dateformatting from '@/components/Dateformatting.vue'
export default {
  name: 'SinglePost',
  components: { Dateformatting },
  props: ["post"],
  data() {
    return {
      "deletePressed": false,
      errorData: "",
    }
},
  computed: {
    active_user_post() {
      if (localStorage.getItem("user_id")) {
        let user_id = JSON.parse(localStorage.getItem("user_id"))
        return (this.post.user_id === user_id)
      }
    },
  },

  methods: {
    gotoprofile() {
      this.$router.push(`/profile/${this.post.user_id}`)
      // console.log("username clicked")
    },

    deletePost(id) {
      this.deletePressed = false
      // console.log(`delete post at SinglePost comp called with post id: ${id}`)
      let cred = localStorage.getItem("Authentication-Token")
      if (!cred) {
        this.$router.push({ name: 'Home' })
      }
      else {
        // console.log('starting to remove data from database')
        CommonFetch(`http://127.0.0.1:5000/api/posts/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': cred
          },
        })
          .then((data) => {
            // console.log(`deleted from database ${data}`)
            this.errorData = "";
            this.$emit('postDeleted', id)
            // console.log("postDeleted event emitted from SinglePost Comp")
          })
          .catch((err) => {
            this.errorData = err.message;
          })
      }
    },
    updatePost(post) {
      let cred = localStorage.getItem("Authentication-Token")
      if (cred) {
        localStorage.setItem('selected_post', JSON.stringify(post))
        this.$router.push({ name: 'Update' })
      }
    }
  }
}
</script>


<style scoped>
.wrapper {
  max-width: 1000px;
  margin-top: 0px !important;
  margin-bottom: 0px !important;
  padding-top: 40px;
}

@media(max-width: 380px) {
  .wrapper {
    /* margin: 30px 20px; */
    margin: 0px 0px;
    /* padding: 40px 15px 15px 15px; */
    padding: 40px 10px 15px 10px;
  }
}

.user-name {
  font-weight: 700;
  /* background-color: orange; */
  font-family: poppins;
  text-transform: capitalize;
  margin-bottom: 0px;
  color: #539d8b;
}

.user-email {
  font-weight: 100;
  color: #494848;
  padding-bottom: 10px !important;
  /* padding-top:7px;
  padding-left:5px; */
  margin-bottom: 20px !important;
  font-family: poppins !important;
  font-size: small !important;
}

.post_date {
  font-weight: 200 !important;
  color: #494848 !important;
  padding-bottom: 0px !important;
  margin-bottom: 0px !important;
  margin-top: 0px !important;
  font-size: small !important;
  font-family: poppins !important;
  /* font-style:italic; */
}

.btn-follow {
  width: 100px !important;
  font-size: small;
}

.post-title {
  font-weight: 500;
  font-family: poppins;
  margin-bottom: 0px;
  color: black;
  text-align: left;
}

.post-description {
  font-weight: 300;
  font-family: poppins;
  font-size: 20px !important;
  letter-spacing: 0px;
  line-height: 1.2;
  color: black;
}

.post-edit,
.post-delete-prompt {
  margin-top: 20px;
  width: 28% !important;
  max-width: 120px !important;
  min-width: 80px !important;
  font-family: poppins !important;
  font-size: small;
  text-align: center !important;
}

.post-delete-prompt {
  margin-left: 10px;
}

.post-delete {
  margin-top: 20px;
  width: 28% !important;
  max-width: 120px !important;
  min-width: 80px !important;
  font-family: poppins !important;
  font-size: small;
  text-align: center !important;
  background-color: lightcoral !important;
  margin-left: 10px;
}
</style>
