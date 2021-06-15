<template>
<div>
  <img src="http://localhost:5000/video_feed" width="600px">
  <router-link to="/view_img"><span v-on:click="takeimage">Take a picture</span></router-link>
  <br>
  <router-link to="/">Back to home</router-link>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    takeimage() {
      const path = 'http://localhost:5000/takeimage';
      axios.get(path)
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getMessage() {
      const path = 'http://localhost:5000/video_feed';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
