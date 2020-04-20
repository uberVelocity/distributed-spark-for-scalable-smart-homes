<template>
  <div class="container">
    <div class="devices-container">
      <div
        class="device"
        v-for="(device, index) in devices"
        v-bind:item="device"
        v-bind:index="index"
        v-bind:key="device.id"
      >
        {{ `${device.id}: ${device.number}` }}
      </div>
    </div>
    <button @click="getData">Get predictions</button>
  </div>
</template>

<script>
import StatusRetriever from '../services/StatusRetriever'
export default {
  data() {
    return {
      devices: []
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
      console.log(`predictions = ${req.data}`);
      const data = req.data;
      console.log(`id 1: ${data[0].id}, model 2: ${data[1].model}, number 3: ${data[2].number}`);
      this.devices = data;
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
