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
      <label>Heater: {{heater}} hours</label>
      <br>
      <label>Lamp: {{lamp}} hours</label>
      <br>
      <label>Vacuum: {{vacuum}} hours</label>
      <br>
      <label>Wattage: {{wattage}}</label>
  </div>
</template>

<script>
import StatusRetriever from '../services/StatusRetriever'
export default {
  data() {
    return {
      heater: 0,
      vacuum: 0,
      lamp: 0,
      wattage: 0
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
      const req = await StatusRetriever.getStatus();
      console.log(`predictions = ${req.data.predictions}`);
      const data = req.data.predictions;
      for (let i = 0; i < 6; i++) {
        console.log(`data[${i}] = ${data[i]}`);
      }
      this.wattage = data[4];
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
