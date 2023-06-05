<template>
   <!-- <nav class="navbar bg-body-tertiary"> -->
    <nav class="navbar bg-body-tertiary1">
    <!-- <nav class="navbar" style="background-color: #e3f2fd;"> -->
      <div class="container-fluid">
        <img alt="Vue logo" src="../assets/BlogLite_short.png" width="60" height="auto" style="border-radius:50%" class="blogo">
        <div class="d-flex">
          <router-link to='/' class = "text-decoration-none">Login</router-link>
          <router-link to='/register' class = "text-decoration-none">Register</router-link>
          <!-- <router-link to="/about">Login</router-link> -->
        </div>
      </div>
    </nav>
</template>

<script>
export default {
  name: 'Header',
  }
</script>


<style scoped>
  nav {
    padding: 5px;
  }

  .bg-body-tertiary1 {
    --bs-bg-opacity: 1;
    /* background-color: rgba(var(--bs-tertiary-bg-rgb),var(--bs-bg-opacity))!important; */
    background-color: #539d8b;
  }


  nav a {
    padding: 10px;
    font-weight: bold;
    /* color:#f5c5be; */
    color:white;
    border-radius: 25px;
    font-family: 'Poppins', sans-serif;
    letter-spacing: 1.3px;
  }

  nav a:hover {
    padding: 10px;
    font-weight: bold;
    /* color:#f5c5be; */
    color:#539d8b;
    background-color:#f5c5be;
  }
  nav a.router-link-exact-active {
    color: #f5c5be;
    display: none;
}

.blogo {
  width:60px;
  height:"auto";
  border-radius:50%
}


</style>
