<script setup>
  import { store } from '../store.js';
  import { ref, onMounted } from 'vue'

  let username = ref("");
  let password = ref("");
  let confirmPassword = ref("");

  function validateInput(un, pw, cpw) {
    if (!un || !pw || !cpw){
      alert('Please enter all the fields.');
      return false;
    } else if(pw != cpw) {
      alert('Password and Confirm Password fields should match');
      return false;
    } else {
      return true;
    };
  };

  function register() {
    if (validateInput(username.value, password.value, confirmPassword.value)) {
      console.log(username.value);
      console.log(password.value);
      const options = {
        username: username.value,
        password: password.value 
      }

      // send register data to the API 
      fetch("http://127.0.0.1:5000/register", {
        method: 'POST',
        body: JSON.stringify(options),
        headers: { 'Content-Type': 'application/json' } 
      }).then(res => res.json().then(json => ({
        response: res,
        json
      })))
      .then(({ response, json }) => {
          if(!response.ok){
            throw new Error(response.status + " " + json.message);
          }
          store.setUser(json.id, json.username)
      
      })
      .catch(err => {
        alert('Unable to register. ' + err)
      })
    }
  }

</script>

<template>

  <div>
    <h1>Register</h1>
      <form @submit.prevent="register">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" />
      <br />
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" />
      <br />
      <label for="confirmPassword">Confirm Password:</label>
      <input type="password" id="confirmPassword" v-model="confirmPassword" />
      <br />
      <button type="button" @click="register">Register</button>
    </form>
    </div>
    <div class="loginLink">
    Already have an account? 
    <router-link to = "/Login">Login here</router-link><br><br>
    <router-link to = "/" class="home">Home</router-link>
  </div>
</template>

<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f2f2f2;
}
h1 {
  text-align: center;
  margin-top: 25px;
  margin-bottom: 25px;
}
.loginLink{
  margin-top: 30px;
  margin-left: 600px;
}
.home {
  margin-left: 150px;
}
form {
  background-color: #ffffff;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}
input[type="text"],
input[type="email"],
input[type="password"] {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
input[type="submit"] {
  display: block;
  width: 100%;
  background-color: #4CAF50;
  color: #ffffff;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

</style>  
