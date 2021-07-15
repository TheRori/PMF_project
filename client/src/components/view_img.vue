<template>
  <b-container>
    <b-row>
      <b-col>
        <canvas id='canvas' ref='select' @mousedown='startSelect' @mousemove='drawRect'
           @mouseup='stopSelect'>
        </canvas>
      </b-col>
      <b-col>
        <b-list-group>
          <b-list-group-item button v-for='(item, index) in startPosition.x' v-bind:key="item.id"
              v-on:click='selectZone(index)'><p>Test{{index}}</p>
            <p v-on:click='removeZone(index)'>{{zoneSelectedText[index]}}</p></b-list-group-item>
        </b-list-group>
      </b-col>
    </b-row>
    <b-button v-on:click='saveZones'>Save</b-button>
    <b-button v-on:click='readZones'>Read</b-button>
  </b-container>
</template>

<script>
import axios from 'axios';
import myImg from '../../../server/salut.jpg';

export default {
  name: 'view_img',
  data() {
    return {
      ctx: null,
      widthCanvas: 800,
      selectionMode: false,
      zoneSelectedText: [],
      zoneMode: 'action',
      img1: new Image(),
      canvas: document.querySelector('canvas'),
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
        selected: [],
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
    selectZone(i) {
      this.zoneSelectedText = [];
      for (let j = 0; j < this.startPosition.x.length; j += 1) {
        this.zoneSelectedText.push('');
        this.startPosition.selected[j] = false;
      }
      this.startPosition.selected[i] = true;
      this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
        this.widthCanvas * (this.img1.height / this.img1.width));
      this.drawOldRects();
      this.zoneSelectedText[i] = 'Remove zone';
    },
    removeZone(i) {
      this.startPosition.x.splice(i, i + 1);
      this.startPosition.y.splice(i, i + 1);
      this.startPosition.w.splice(i, i + 1);
      this.startPosition.h.splice(i, i + 1);
      this.startPosition.type.splice(i, i + 1);
      this.startPosition.selected.splice(i, i + 1);
      const path = 'http://localhost:5000/savezones';
      axios.post(path, this.startPosition)
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
        this.widthCanvas * (this.img1.height / this.img1.width));
      this.drawOldRects();
    },
    readZones() {
      const path = 'http://localhost:5000/readzones';
      let z;
      this.startPosition.x = [];
      this.startPosition.y = [];
      this.startPosition.w = [];
      this.startPosition.h = [];
      this.startPosition.type = [];
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
              this.startPosition.type.push((v.Zone));
            }
          }
        /* eslint-enable */
          this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
          this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
            this.widthCanvas * (this.img1.height / this.img1.width));
          this.drawOldRects();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    startSelect(e) {
      const rOffset = this.canvas.getBoundingClientRect();
      this.selectionMode = true;
      this.rect.startX = e.clientX - rOffset.left;
      this.rect.startY = e.clientY - rOffset.top;
    },
    insertImg() {
      this.img1 = new window.Image();
      this.img1.src = myImg;
      this.img1.onload = () => {
        this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
          this.widthCanvas * (this.img1.height / this.img1.width));
      };
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
    },
    drawOldRects() {
      for (let i = 0; i < this.startPosition.x.length; i += 1) {
        this.ctx.beginPath();
        this.ctx.rect(this.startPosition.x[i], this.startPosition.y[i],
          this.startPosition.w[i], this.startPosition.h[i]);
        if (this.startPosition.type[i] === 'action') {
          this.ctx.strokeStyle = 'red';
        } else if (this.startPosition.type[i] === 'check') {
          this.ctx.strokeStyle = 'blue';
        }
        if (this.startPosition.selected[i] === true) {
          this.ctx.strokeStyle = 'green';
        }
        this.ctx.closePath();
        this.ctx.stroke();
      }
    },
    stopSelect() {
      this.startPosition.x.push(this.rect.startX);
      this.startPosition.y.push(this.rect.startY);
      this.startPosition.w.push(this.rect.w);
      this.startPosition.h.push(this.rect.h);
      this.startPosition.type.push(this.zoneMode);
      this.startPosition.selected.push(false);
      this.selectionMode = false;
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
