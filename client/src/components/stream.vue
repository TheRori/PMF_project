<template>
<b-container>
  <b-row>
    <b-col><img v-if="$route.params.type !== 'pos'" src="http://localhost:5000/video_feed"
                width="600px">
    ><img v-if="$route.params.type === 'pos'" src="http://localhost:5000/video_feed?crop=True"
                width="600px"></b-col>
  </b-row>
  <b-row>
    <b-col><router-link v-if="$route.params.type === 'normal'"
                        :to="{ name: 'View_Img', params: { load: 'None'}, mode:'normal'}">
      <span v-on:click="takeimage('')">
      Take a picture</span></router-link>
    <router-link v-if="$route.params.type === 'retake'"
                        :to="{ name: 'View_Img',
                        params: { load: $route.params.project, mode:'retake'}}">
      <span v-on:click="takeimage('')">
      Take a picture</span></router-link></b-col>
    <router-link v-if="$route.params.type === 'pos'"
                        :to="{ name: 'Position image', params:
                        { project: $route.params.project, pos: $route.params.pos,
                        step: $route.params.step}}">
      <span v-on:click="takeimage('2')">
      Take a position picture</span></router-link>
    <b-col><router-link to="/">
      Back to home</router-link></b-col>
  </b-row>
</b-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'stream',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    takeimage(id) {
      const path = `http://localhost:5000/takeimage${id}`;
      axios.get(path)
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.$forceUpdate();
    },
  },
};
</script>
