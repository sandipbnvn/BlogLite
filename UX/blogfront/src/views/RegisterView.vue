<template>
  <div class="register">
    <div class="fixed">
      <Header />
    </div>
    <Registrationform />

  </div>
</template>

<script>
import Registrationform from '@/components/Registrationform.vue'
import Header from '@/components/Header.vue'


export default {
  name: 'RegisterView',
  components: {
    Header,
    Registrationform
  }
}
</script>

<style>
.fixed {
  position: fixed;
  top:0;
  width: 100%;
}
</style>
