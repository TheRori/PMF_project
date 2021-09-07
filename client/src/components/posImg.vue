<template>
<div>
  <b-navbar type="dark" variant="dark">
      <b-navbar-nav>
      <b-navbar-brand class="mx-3" href="#">PMF Vision</b-navbar-brand>
      <!-- Navbar dropdowns -->
      </b-navbar-nav>
    </b-navbar>
  <b-container>
    <b-row>
      <b-col>
        <canvas v-bind:class="{ do_rects: doRects }" id='canvas' ref='select' v-on="doRects ?
        { mousedown: startSelect, mousemove: drawRect, mouseup: stopSelect } :
        {mousedown: selectZoneMouse}">
        </canvas>
      </b-col>
      <b-col class="my-accordion" role="tablist">
      <b-row button v-for='(item, index) in startPosition.x' v-bind:key="item.id"
          v-on:click='selectZone(index)'>
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle="'accordion-' + index" variant="info">
              Zone {{startPosition.id[index]}}</b-button>
          </b-card-header>
          <b-collapse :id="'accordion-' + index" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-row>
                <b-col>
                  <b-form-select v-model="startPosition.type[index]" v-on:change="selectZone(index)"
                                 :options="mode_options"></b-form-select>
                </b-col>
              </b-row>
              <b-button v-on:click="removeZone(index)">Remove zone</b-button>
            </b-card-body>
          </b-collapse>
        </b-card>
      </b-row>
        <b-button v-b-modal.modal-zones>
          New zone</b-button>
        <b-modal v-model="doRects" id="modal-zones" :class="status($v.zoneMode)"
                 title="Using Component Methods" hide-header hide-footer>
          <b-row>
            <b-col>
              <b-form-select v-if="doRects" v-model="zoneMode"
                             :options="mode_options"></b-form-select>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-button variant="outline-danger" block @click="hideModal">
                Cancel</b-button>
            </b-col>
            <b-col>
              <b-button variant="outline-warning"
                        block v-on:click="hideModal(); doRects = true;">OK</b-button>
            </b-col>
          </b-row>
          <b-row>
            <div class="error" v-if="!$v.zoneMode.required">Field is required</div>
          </b-row>
        </b-modal>
      </b-col>
    </b-row>
    <b-row>
        <b-button class="float-right" ref="back-save"
    v-on:click="saveZone();saveCrop();">
    Accept this zone of control</b-button>
    </b-row>
  </b-container>
</div>
</template>

<script>
import axios from 'axios';
import { required } from 'vuelidate/lib/validators';
import myImg from '../../../server/pos.jpg';

export default {
  name: 'pos_img',

  data() {
    return {
      zoneMode: null,
      submitStatus: null,
      zoneName: null,
      doRects: false,
      startPosition: {
        id: [],
        x: [],
        y: [],
        w: [],
        h: [],
        type: [],
        selected: [],
      },
      mode_options: [
        { value: '', text: 'Default' },
        { value: 'assembly', text: 'Assembly' },
        { value: 'collect', text: 'Collect' },
        { value: 'display', text: 'Display' },
      ],
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
        x1: null,
        x2: null,
        y1: null,
        y2: null,
      },
      selectionMode: false,
    };
  },
  validations: {
    zoneMode: {
      required,
    },
  },
  methods: {
    validateState(name) {
      const { $dirty, $error } = this.$v.form[name];
      return $dirty ? !$error : null;
    },
    status(validation) {
      return {
        error: validation.$error,
        dirty: validation.$dirty,
      };
    },
    saveZone() {
      const path1 = 'http://localhost:5000/save_zone_control';
      this.crop.y1 = this.startPosition.y[0] * (this.img1.height / (this.widthCanvas * 0.5625));
      this.crop.x1 = this.startPosition.x[0] * (this.img1.width / this.widthCanvas);
      this.crop.x2 = this.startPosition.w[0] * (this.img1.width / this.widthCanvas);
      this.crop.y2 = this.startPosition.h[0] * (this.img1.height / (this.widthCanvas * 0.5625));
      axios.post(path1,
        {
          zone: this.crop,
          folder: this.$route.params.project,
          step: this.$route.params.step,
          file: this.$route.params.pos,
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    hideModal() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.submitStatus = 'ERROR';
      } else {
        this.$bvModal.hide('modal-zones');
      }
    },
    removeZone(i) {
      this.startPosition.id.splice(i, 1);
      this.startPosition.x.splice(i, 1);
      this.startPosition.y.splice(i, 1);
      this.startPosition.w.splice(i, 1);
      this.startPosition.h.splice(i, 1);
      this.startPosition.type.splice(i, 1);
      this.startPosition.selected.splice(i, 1);
      this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
        this.widthCanvas * (this.img1.height / this.img1.width));
      this.drawOldRects();
    },
    selectZone(i) {
      for (let j = 0; j < this.startPosition.x.length; j += 1) {
        this.startPosition.selected[j] = false;
      }
      this.startPosition.selected[i] = true;
      this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
        this.widthCanvas * (this.img1.height / this.img1.width));
      this.drawOldRects();
    },
    selectZoneMouse(e) {
      this.canvas = document.querySelector('canvas');
      const rOffset = this.canvas.getBoundingClientRect();
      const posX = e.clientX - rOffset.left;
      const posY = e.clientY - rOffset.top;
      console.log(this.startPosition);
      for (let j = 0; j < this.startPosition.x.length; j += 1) {
        if (posX >= this.startPosition.x[j] && posY >= this.startPosition.y[j]
        && posX <= this.startPosition.x[j] + this.startPosition.w[j]
        && posY <= this.startPosition.y[j] + this.startPosition.h[j]) {
          this.$root.$emit('bv::toggle::collapse', `accordion-${j}`);
        }
      }
    },
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
        if (this.zoneMode === null) {
          this.ctx.strokeStyle = 'black';
        } else if (this.zoneMode === 'assembly') {
          this.ctx.strokeStyle = 'red';
        } else if (this.zoneMode === 'collect') {
          this.ctx.strokeStyle = 'yellow';
        } else if (this.zoneMode === 'display') {
          this.ctx.strokeStyle = 'green';
        }
        this.ctx.closePath();
        if (Math.abs(this.rect.h * this.rect.w) > 40) {
          this.ctx.stroke();
        }
        this.drawOldRects();
      }
    },
    drawOldRects() {
      for (let i = 0; i < this.startPosition.x.length; i += 1) {
        this.ctx.beginPath();
        this.ctx.rect(this.startPosition.x[i], this.startPosition.y[i],
          this.startPosition.w[i], this.startPosition.h[i]);
        if (this.startPosition.type[i] === null) {
          this.ctx.strokeStyle = 'black';
        } else if (this.startPosition.type[i] === 'assembly') {
          this.ctx.strokeStyle = 'red';
        } else if (this.startPosition.type[i] === 'collect') {
          this.ctx.strokeStyle = 'yellow';
        } else if (this.startPosition.type[i] === 'display') {
          this.ctx.strokeStyle = 'green';
        }
        this.ctx.closePath();
        this.ctx.stroke();
      }
    },
    stopSelect() {
      if (this.rect.w < 0 && this.rect.h > 0) {
        this.rect.startX += this.rect.w;
        this.rect.w = Math.abs(this.rect.w);
      } else if (this.rect.h < 0 && this.rect.w > 0) {
        this.rect.startY += this.rect.h;
        this.rect.h = Math.abs(this.rect.h);
      } else if (this.rect.w < 0 && this.rect.h < 0) {
        this.rect.startX += this.rect.w;
        this.rect.startY += this.rect.h;
        this.rect.h = Math.abs(this.rect.h);
        this.rect.w = Math.abs(this.rect.w);
      }
      if ((Math.abs(this.rect.w * this.rect.h > 40)) && (this.selectionMode)) {
        this.startPosition.id.push(this.startPosition.x.length);
        this.startPosition.x.push(this.rect.startX);
        this.startPosition.y.push(this.rect.startY);
        this.startPosition.w.push(this.rect.w);
        this.startPosition.h.push(this.rect.h);
        this.startPosition.type.push(this.zoneMode);
        this.startPosition.selected.push(false);
      }
      this.selectionMode = false;
      this.doRects = false;
    },
    saveCrop() {
      const canvas = document.getElementById('canvas');
      // eslint-disable-next-line
      const image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
      window.location.href = image;
      const path1 = 'http://localhost:5000/save_crop';

      axios.post(path1, {
        folder: this.$route.params.project, file: this.$route.params.pos,
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.$router.push(`/scenario/${this.$route.params.project}`);
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
