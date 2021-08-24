<template>
<div>
  <b-container>
    <row>
      <b-col>
        <canvas v-bind:class="{ do_rects: doRects }" id='canvas' ref='select'
        v-on="{ mousedown: startSelect, mousemove: drawRect, mouseup: stopSelect }">
        </canvas>
      </b-col>
    </row>
    <b-modal id="cropped" @ok="saveCrop(); saved = true">
      <img src='../../../server/cropped.jpg'></b-modal>
  </b-container>
</div>
</template>

<script>
import axios from 'axios';
import myImg from '../../../server/pos.jpg';

export default {
  name: 'pos_img',
  data() {
    return {
      cropped: false,
      ctx: null,
      widthCanvas: process.env.VUE_APP_WIDTH,
      img1: new Image(),
      rect: {
        startX: null,
        startY: null,
        x: null,
        y: null,
        ww: null,
        hh: null,
        w: null,
        h: null,
      },
      crop: {
        y: null,
        x: null,
        w: null,
        h: null,
      },
      selectionMode: false,
    };
  },
  methods: {
    startSelect(e) {
      const rOffset = this.canvas.getBoundingClientRect();
      this.rect.startX = e.clientX - rOffset.left;
      this.rect.startY = e.clientY - rOffset.top;
      this.selectionMode = true;
      this.rect.x = e.offsetX;
      this.rect.y = e.offsetY;
    },
    drawRect(e) {
      this.canvas = document.querySelector('canvas');
      const rOffset = this.canvas.getBoundingClientRect();
      if (this.selectionMode) {
        this.rect.w = (e.clientX - rOffset.left) - this.rect.startX;
        this.rect.h = (e.clientY - rOffset.top) - this.rect.startY;
        this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
        this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
          this.widthCanvas * (this.img1.height / this.img1.width));
        this.ctx.beginPath();
        this.ctx.rect(this.rect.startX, this.rect.startY, this.rect.w, this.rect.h);
        this.ctx.closePath();
        if (Math.abs(this.rect.h * this.rect.w) > 40) {
          this.ctx.stroke();
        }
      }
    },
    stopSelect(e) {
      this.rect.ww = e.offsetX - this.rect.x;
      this.rect.hh = e.offsetY - this.rect.y;
      this.selectionMode = false;
      this.crop.y = this.rect.y * (this.img1.height / this.$refs.select.height);
      this.crop.x = this.rect.x * (this.img1.width / this.$refs.select.width);
      this.crop.w = this.rect.ww * (this.img1.width / this.$refs.select.width);
      // eslint-disable-next-line
      this.crop.h = this.rect.hh * (this.img1.height / this.$refs.select.height);
      console.log(this.crop.w);
      console.log(this.rect.ww);
      const path1 = 'http://localhost:5000/crop';
      axios.post(path1, {
        y: this.crop.y, x: this.crop.x, w: this.crop.w, h: this.crop.h,
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.$root.$emit('bv::show::modal', 'cropped', '#back-save');
    },
    saveCrop() {
      const path1 = 'http://localhost:5000/save_crop';
      axios.post(path1, {
        folder: this.$route.params.project, file: this.$route.params.pos,
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.$router.push(`/view_img/${this.$route.params.project}`);
    },
    insertImg() {
      this.img1 = new window.Image();
      this.img1.src = myImg;
      this.img1.onload = () => {
        this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
          this.widthCanvas * (this.img1.height / this.img1.width));
      };
    },
  },
  mounted() {
    this.$refs.select.height = this.widthCanvas * 0.5625;
    this.$refs.select.width = this.widthCanvas;
    this.ctx = this.$refs.select.getContext('2d');
    this.insertImg();
  },
};
</script>
