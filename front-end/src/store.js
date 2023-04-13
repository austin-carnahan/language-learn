import { reactive } from 'vue'

export let store = reactive({
  userId: null,
  username: null,
  setUser(userId, username) {
    this.userId = userId,
    this.username = username

    console.log("successfully set user in store")
  },
  getUsername(){
    return this.username;
  },
  getUserId() {
    return this.userId;
  }

})