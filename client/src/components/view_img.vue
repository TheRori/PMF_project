<template>
  <div>
    <canvas id='canvas' ref='select' @mousedown='startSelect' @mousemove='drawRect'
         @mouseup='stopSelect'>
    </canvas>
    <button v-on:click='saveZones'>Save</button>
    <button v-on:click='readZones'>Read</button>
  </div>
</template>

<script>
import axios from 'axios';
import myImg from '../assets/salut.jpg';

export default {
  name: 'view_img',
  data() {
    return {
      ctx: null,
      selectionMode: false,
      zoneMode: 'action',
      img1: new Image(),
      rect: {
        startX: null,
        startY: null,
        w: null,
        h: null,
      },
      startPosition: {
        x: [],
        y: [],
        w: [],
        h: [],
        type: [],
      },
    };
  },
  created() {
    window.addEventListener('keydown', (e) => {
      if (e.key === 'c') {
        this.changeType('check');
      }
      if (e.key === 'a') {
        this.changeType('action');
      }
    });
  },
  methods: {
    saveZones() {
      const path = 'http://localhost:5000/savezones';
      axios.post(path, this.startPosition)
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.$router.push('/index');
    },
    readZones() {
      const path = 'http://localhost:5000/readzones';
      let z;
      this.startPosition.x = [];
      this.startPosition.y = [];
      this.startPosition.w = [];
      this.startPosition.h = [];
      axios.get(path)
        .then((res) => {
          z = res.data;
          /* eslint-disable */
          for (const [key,value] of Object.entries(z)) {
            for (const [k,v] of Object.entries(value)) {
              this.startPosition.x.push(v.X);
              this.startPosition.y.push(v.Y);
              this.startPosition.w.push(v.W);
              this.startPosition.h.push(v.H);
            }
          }
        /* eslint-enable */
          this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
          this.ctx.drawImage(this.img1, 0, 0);
          this.drawOldRects();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    startSelect(e) {
      this.selectionMode = true;
      this.rect.startX = e.pageX;
      this.rect.startY = e.pageY;
    },
    insertImg() {
      this.img1 = new window.Image();
      this.img1.src = myImg;
      this.img1.onload = () => {
        this.ctx.drawImage(this.img1, 0, 0);
      };
    },
    drawRect(e) {
      if (this.selectionMode) {
        this.rect.w = (e.pageX) - this.rect.startX;
        this.rect.h = (e.pageY) - this.rect.startY;
        this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
        this.ctx.drawImage(this.img1, 0, 0);
        this.ctx.beginPath();
        this.ctx.rect(this.rect.startX, this.rect.startY, this.rect.w, this.rect.h);
        if (this.zoneMode === 'action') {
          this.ctx.strokeStyle = 'red';
        }
        if (this.zoneMode === 'check') {
          this.ctx.strokeStyle = 'blue';
        }
        this.ctx.closePath();
        this.ctx.stroke();
        this.drawOldRects();
      }
    },
    changeType(value) {
      this.zoneMode = value;
      console.log('sdfsafsa');
    },
    drawOldRects() {
      for (let i = 0; i < this.startPosition.x.length; i += 1) {
        console.log('hello');
        this.ctx.beginPath();
        this.ctx.rect(this.startPosition.x[i], this.startPosition.y[i],
          this.startPosition.w[i], this.startPosition.h[i]);
        if (this.startPosition.type[i] === 'action') {
          this.ctx.strokeStyle = 'red';
        }
        if (this.startPosition.type[i] === 'check') {
          this.ctx.strokeStyle = 'blue';
        }
        this.ctx.closePath();
        this.ctx.stroke();
      }
    },
    stopSelect() {
      this.startPosition.x[this.startPosition.x.length] = this.rect.startX;
      this.startPosition.y[this.startPosition.y.length] = this.rect.startY;
      this.startPosition.w[this.startPosition.w.length] = this.rect.w;
      this.startPosition.h[this.startPosition.h.length] = this.rect.h;
      this.startPosition.type[this.startPosition.type.length] = this.zoneMode;
      this.selectionMode = false;
      console.log(this.startPosition);
    },
  },
  mounted() {
    this.$refs.select.height = window.innerHeight;
    this.$refs.select.width = window.innerWidth;
    this.ctx = this.$refs.select.getContext('2d');
    this.insertImg();
  },
};

</script>
