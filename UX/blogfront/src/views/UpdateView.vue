<template>
    <div class="update">
      <div class="fixed">
        <header2/>
      </div>
      
      <h1>Welcome user to Update page</h1>
      <UpdatePost :post_data="selected_post"/>
  </div>
</template>

<script>
// @ is an alias to /src
// import Loginform from '@/components/Loginform.vue'
// import Header from '@/components/Header.vue'
import Header2 from '@/components/Header2.vue'
import UpdatePost from '@/components/UpdatePost.vue'

export default {
  name: 'UpdateView',
  data() {
    return {
      "selected_post":null
    }
  },
  components: {
    Header2,
    UpdatePost,
  },
  beforeCreate() {
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) { this.$router.push({name: 'Home'})}
    let post = localStorage.getItem('selected_post')
    if (!post) { this.$router.push({name: 'Feed'})}
    this.selected_post=JSON.parse(post)
  },
  beforeMount() {
    let cred = localStorage.getItem('Authentication-Token')
    let post = localStorage.getItem('selected_post')
    if (!cred) { this.$router.push({name: 'Home'})}
    else if(post) {this.selected_post=JSON.parse(post)}
    
  }
}
</script>

<style>

.fixed {
  position: fixed;
  top:0;
  width: 100%;
  
}</style>
