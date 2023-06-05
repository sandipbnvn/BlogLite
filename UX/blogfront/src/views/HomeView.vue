<template>
    <div class="home">
      <Header />
      <Loginform class="login-form"/>
  </div>
</template>

<script>
// @ is an alias to /src
import Loginform from '@/components/Loginform.vue'
import Header from '@/components/Header.vue'

export default {
  name: 'HomeView',
  components: {
    Loginform,
    Header,
  },
  beforeCreate() {
    let cred = localStorage.getItem('Authentication-Token')
    if (cred) { this.$router.push({name: 'Feed'})}
  }
}
</script>

<style scoped>
@media (max-width:400px) {
.login-form {
  margin-left:10px;
  min-width:800px !important;
}
}
</style>
