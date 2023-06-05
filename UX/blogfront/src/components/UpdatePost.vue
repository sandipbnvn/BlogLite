<template>
  <div class="contatiner">
    <div class="updatepost" style="margin-top:40px;">
      <div class="wrapper">
        <div class="logo">
          <img src="../assets/BlogLite_short.png" width="180" height="auto" alt="">
        </div>
        <div class="text-center mt-4 name">
          BlogLite
        </div>
        <small class="text-muted">Update Post</small>

        <form class="p-3 mt-3" enctype="multipart/form-data" @submit.prevent="editPost">
          <div class="form-field d-flex align-items-center">
            <span class="far fa-user"></span>
            <input type="text" name="title" id="title" placeholder="Title" v-model='PostData.title'>
          </div>
          <div class="form-field d-flex align-items-center">
            <span class="far fa-user"></span>
            <textarea name="description" id="description" placeholder="Description" v-model='PostData.description'
              cols="40" rows="5" style="background: transparent;border:none;outline: none;"></textarea>
          </div>

          <div class="d-flex align-items-center">
            <img class="card-img-bottom" v-if="!change_image_pressed && this.PostData.imageURL != null"
              :src="require(`@/assets/uploded_images/${PostData.imageURL}`)" alt="Card image" style="width:100%" />
          </div>
          <div v-if="this.previewImage != null" class="imagePreviewWrapper form-field d-flex align-items-center"
            :style="{ 'background-image': `url(${previewImage})` }" @click="selectImage"> </div>

          <button type="button" class="btn mt-3 mb-3 btn-change-photo" style="background-color:salmon ;"
            @click="changeImage" v-if="PostData.imageURL != null || this.previewImage != null">Change Photo</button>
          <button type="button" class="btn mt-3 mb-3 btn-change-photo" style="background-color:salmon ;"
            @click="changeImage" v-if="this.previewImage === null && PostData.imageURL === null">Add Photo</button>
          <button type="button" class="btn mt-3 mb-3 btn-change-photo" style="background-color:salmon ;"
            @click="removeImage" v-if="PostData.imageURL != null || this.previewImage != null">Remove Photo</button>


          <div class="form-field d-flex align-items-center">
            <input ref="fileInput" accept="image/*" type="file" id="file-input" name="file" class="image-input" @input="pickFile"
              v-on:change="handleFileUpload" v-show="false && PostData.imageURL === null && change_image_pressed">
          </div>
          <button type="submit" class="btn mt-2 btn-change-photo" style="background-color:#539d8b ;">Update
            Post</button>
        </form>
        <span style="padding:3px;color:red;" v-if="errorData != ''">{{ errorData }}</span>
      </div>
    </div>
  </div>
</template>


<script>
import CommonFetch from '../CommonFetch'
// import ImageUpload from './ImageUpload.vue'

export default {
  name: 'UpdatePost',
  // components: { ImageUpload },
  props: ['post_data'],
  data() {
    return {
      "PostData": {
        "title": this.post_data.title,
        "description": this.post_data.description,
        "imageURL": this.post_data.imageURL,
      },
      selectedFile: null,
      previewImage: null,
      change_image_pressed: false,
      "errorData": ""
    }
  },

  // mounted() {
  //   if (this.post_data.imageURL===null) {

  //   }
  // },


  methods: {

    handleFileUpload(event) {
      let files = this.$refs.fileInput.files;
      // console.log(files[0])
      this.PostData.image = files[0]
    },

    changeImage() {
      console.log("change image function called")
      this.PostData.image = null;
      this.change_image_pressed = true;
      let inputField = document.getElementById('file-input')
      if (inputField != null) {
        inputField.click()
      }
    },
    removeImage() {
      this.previewImage = null;
      this.PostData.imageURL = null;
      let cred = localStorage.getItem("Authentication-Token")
      if (!cred) { this.$router.push({ name: 'Home' }) }
      CommonFetch(`http://127.0.0.1:5000/api/extra/remove_post_image/${this.post_data.id}`, {
        headers: {
          'Authentication-Token': cred
        },
      })
        .then((data) => {
          console.log(data)
        })
        .catch((err) => {
          this.errorData = err.message;
        })
    },

    editPost() {
      if (this.PostData.title === "") {
        this.errorData = "Title is Required";
        return
      }
      if (this.PostData.description === "") {
        this.errorData = "Description is Required";
        return
      }

      let cred = localStorage.getItem("Authentication-Token")
      if (!cred) { this.$router.push({ name: 'Home' }) }

      const formData = new FormData();
      formData.append('title', this.PostData.title);
      formData.append('description', this.PostData.description)
      if (this.$refs.fileInput.files[0]) {
        formData.append('image', this.$refs.fileInput.files[0])
      }
      CommonFetch(`http://127.0.0.1:5000/api/posts/${this.post_data.id}`, {
        method: 'PUT',
        body: formData,
        headers: {
          'Authentication-Token': cred
        },
      })
        .then((data) => {
          console.log(data)
          this.errorData = "";
          localStorage.removeItem('user')
          localStorage.removeItem('userPosts')
          this.$router.push('/SelfProfile')
        })
        .catch((err) => {
          this.errorData = err.message;
        })

    },

    onFileSelected(event) {
      this.selectedFile = event.target.files[0];
      // console.log(event)
    },
    selectImage() {
      this.$refs.fileInput.click()
    },
    pickFile() {
      let input = this.$refs.fileInput
      let file = input.files
      if (file && file[0]) {
        let reader = new FileReader
        reader.onload = e => {
          this.previewImage = e.target.result
        }
        reader.readAsDataURL(file[0])
        this.$emit('input', file[0])
      }
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
  max-width: 650px;
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

textarea::placeholder {
  text-align: bottom;
  font-size: large;
}

.wrapper .form-field textarea {
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

.btn {
  max-width: 175px;
}

.imageuploader {
  /* border:1px solid blue; */
  overflow-wrap: break-word;
  width: 100%;
  border-radius: 10px;
}

.imagePreviewWrapper {
  min-width: 250px;
  max-width: 650px;
  min-height: 250px;
  max-height: 650px;
  display: block;
  cursor: pointer;
  margin: 0 auto 30px;
  background-size: cover;
  background-position: center center;
  overflow-wrap: break-word;
  border-radius: 15px;
  font-size: 5px;
}

.image-input {
  font-size: 5px;
}

.btn-change-photo {
  font-size: small;
  width: 28% !important;
  min-width: 120px;
  height: auto !important;
  min-height: 40px;
  margin-right: 10px;
}
</style>
