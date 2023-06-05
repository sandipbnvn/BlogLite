<template>
  <div class="post">
    <div class="contatiner" style="margin-top:20px;font-family:poppins !important;">
      <div class="createpost">
        <!-- <div class="p-1 mt-0" style="margin-bottom:30px;">
          <h3 class="text-muted summary">User Posts</h3>
        </div> -->
        <div class="p-3 mt-0" v-for="(post, id) in post_data" :key="id">
          <SinglePost :post="post" @postDeleted="postDeleteForwarded" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SinglePost from '@/components/SinglePost.vue'
export default {
  name: 'Post',
  components: { SinglePost },
  props: ["post_data"],
  data() {
    return {
      "deletePressed": false
    }
  },
  methods: {
    postDeleteForwarded(id) {
      // console.log("postDeleteForwarded called")
      this.$emit("postDeleteReceived", id)
      // console.log("postDeleteReceived emitted")

    }
  }

}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

@media(max-width: 380px) {
  .container .post {
    /* margin: 30px 20px; */
    margin: 0px 0px;
    /* padding: 40px 15px 15px 15px; */
    padding: 40px 0px 15px 0px;
  }
}

.summary {
  text-align: center;
  font-weight: 700;
  /* background-color: orange; */
  font-family: poppins !important;
  margin-bottom: 0px !important;
  margin-top:0px !important;
  padding-top: 0px !important;
  padding-bottom: 0px !important;
  /* color: #f5c5be !important; */
  color: black !important;
}
</style>
