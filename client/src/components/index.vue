<template>
<div class="main_menu">
    <b-container>
      <b-row class="mb-5">
        <b-col>
          <img src="../assets/pmf_logo.png">
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <router-link class="main_menu_option" to="/stream">Create a scenario</router-link> <br>
        </b-col>
        <b-col>
          <p class="main_menu_option"
             v-b-modal.modal-load_project v-on:click="getNames">Load a scenario</p>
          <b-modal id="modal-load_project">
            <b-row button v-for='(item, index) in names' v-bind:key="index">
              <router-link :to="{ name: 'View_Img', params: { load: item }}">{{item}}</router-link>
            </b-row>
          </b-modal>
        </b-col>
      </b-row>
    </b-container>
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
<style>
.main_menu {
  background-color: black;
  height: 100vh;
  max-width: 100vw;
  margin: 0;
  display: flex;
  align-items: center;
}

.main_menu_option {
  color: cornflowerblue;
  font-size: 1.8rem;
  margin: auto !important;
}

.main_menu_option:hover {
  color: azure !important;
  text-decoration: none !important;
}
</style>
