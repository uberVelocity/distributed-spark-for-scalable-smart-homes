<template>
  <div class="container">
    <b-navbar>
        <template slot="brand">
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                <img
                    src="https://raw.githubusercontent.com/buefy/buefy/dev/static/img/buefy-logo.png"
                    alt="Lightweight UI components for Vue.js based on Bulma"
                >
            </b-navbar-item>
        </template>
        <template slot="start">
            <b-navbar-item @click="goHome">
                Home
            </b-navbar-item>
            <b-navbar-item @click="goAbout">
                About
            </b-navbar-item>
        </template>
        <template slot="end">
            <b-navbar-item tag="div">
                <div class="buttons">
                    <a class="button is-primary">
                        <strong>Sign up</strong>
                    </a>
                    <a class="button is-light">
                        Log in
                    </a>
                </div>
            </b-navbar-item>
        </template>
    </b-navbar>
    <h1>Home</h1>
      <button @click="getData()">Heater</button>
      <br>
      <textarea readonly name="timeStampText" id="timeStampText" cols="30" rows="30" v-model="timeStampText"></textarea>
      <br>
      <textarea readonly name="valuesText" id="valuesText" cols="30" rows="30" v-model="valuesText"></textarea>
  </div>
</template>

<script>
import StatusRetriever from '../services/StatusRetriever'
export default {
  data() {
    return {
      timeStampText: '',
      valuesText: ''
    }
  },
  methods: {
    goAbout() {
      this.$router.push('/about');
    },
    goHome() {
      this.$router.push('/');
    },
    async getData() {
      const data = await StatusRetriever.getStatus();
      alert(`received something: ${data}`);
    },
    formatTimeStamps(data) {
      this.timeStampText = '';
      data.forEach(value => {
        this.timeStampText += value + '\n';
      });
    },
    formatValues(data) {
      this.valuesText = '';
      data.forEach(value => {
        this.valuesText += value + '\n';
      });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
