<template>
<div>
<router-link to="/stream">Take a pic</router-link> <br>
<p v-b-modal.modal-load_project v-on:click="getNames">Load a scenario</p>
  <b-modal id="modal-load_project">
    <b-row button v-for='(item, index) in names' v-bind:key="index">
      <router-link :to="{ name: 'View_Img', params: { load: item }}">{{item}}</router-link>
    </b-row>
  </b-modal>
</div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'index',
  data() {
    return {
      names: [],
    };
  },
  methods: {
    getNames() {
      const path = 'http://localhost:5000/get_project_names';
      let d;
      axios.get(path)
        .then((res) => {
          d = res.data;
          /* eslint-disable */
          for (const [key,value] of Object.entries(d)) {
            this.names.push(value)
          }
        /* eslint-enable */
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
