<template>
    <div class="create">
      <div class="fixed">
        <header2/>
      </div>
      
      <h1>Welcome user to create page</h1>
      <CreatePost/>
  </div>
</template>

<script>
// @ is an alias to /src
// import Loginform from '@/components/Loginform.vue'
// import Header from '@/components/Header.vue'
import Header2 from '@/components/Header2.vue'
import CreatePost from '@/components/CreatePost.vue'

export default {
  name: 'CreateView',
  components: {
    Header2,
    CreatePost,
  },
  beforeCreate() {
    let cred = localStorage.getItem('Authentication-Token')
    if (!cred) { this.$router.push({name: 'Home'})}
  }
}
</script>

<style>

.fixed {
  position: fixed;
  top:0;
  width: 100%;
  
}</style>
