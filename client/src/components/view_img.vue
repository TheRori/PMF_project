<template>
  <div>
    <b-navbar type="dark" variant="dark">
      <b-navbar-nav>
      <b-navbar-brand class="mx-3" href="#">PMF Vision</b-navbar-brand>
      <!-- Navbar dropdowns -->
      <b-nav-item-dropdown text="File" right>
        <b-dropdown-item  v-on:click="showModalSave" >Save</b-dropdown-item>
        <b-modal id="modal-save" @cancel="nameProject = ''"
                 @ok="saveZones(); saved = true" title="Save scenario and zones">
        <b-form-input placeholder='Name of the project' v-model="nameProject">
        </b-form-input>
        </b-modal>
      </b-nav-item-dropdown>
      </b-navbar-nav>
      <b-navbar-nav right class="ml-auto">
                <b-button class="float-right mr-3" ref="back-save"
                  v-on:click="saveZones(); $router.push({ name: 'Create_Scenario',
                  params: { load: nameProject, mode: 'normal' }});">
                  Go to scenario creation</b-button>
        <b-button class="float-right" ref="back-save"
                  v-on:click="reinit = true; showModalSave();">Save and Back home</b-button>
      </b-navbar-nav>
    </b-navbar>
  <b-container class="content_ui">
    <b-row class="mb-3 mt-2 mx-auto">
      <b-col class="mx-auto">
      <h3 class="mx-auto">Do a scenario – Make the zones</h3>
      </b-col>
    </b-row>
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
                  <b-form-input v-model="startPosition.name[index]" v-on:change="selectZone(index)">
                  </b-form-input>
                </b-col>
                <b-col>
                  <b-form-select v-model="startPosition.type[index]" v-on:change="selectZone(index)"
                                 :options="mode_options"></b-form-select>
                </b-col>
                <b-col>
                  <b-form-select v-model="startPosition.z[index]" v-on:change="selectZone(index)"
                                 :options="level_options"></b-form-select>
                </b-col>
              </b-row>
              <b-button v-on:click="removeZone(index)">Remove zone</b-button>
            </b-card-body>
          </b-collapse>
        </b-card>
      </b-row>
        <b-button v-b-modal.modal-zones>
          New zone</b-button>
        <b-modal v-model="doRects" id="modal-zones"
                 title="Using Component Methods" hide-header hide-footer>
          <b-row>
            <b-col>
              <b-form-input v-if="doRects" v-model="zoneName" :class="status($v.zoneName)"
                            placeholder="Zone name"></b-form-input>
              <b-row>
                <div class="error" v-if="!$v.zoneName.required">Field is required</div>
              </b-row>
            </b-col>
            <b-col>
              <b-form-select v-if="doRects" v-model="zoneMode" :class="status($v.zoneMode)"
                             :options="mode_options"></b-form-select>
              <b-row>
                <div class="error" v-if="!$v.zoneMode.required">Field is required</div>
              </b-row>
            </b-col>
            <b-col>
              <b-form-select v-if="doRects" v-model="level" :class="status($v.level)"
                             :options="level_options"></b-form-select>
              <b-row>
                <div class="error" v-if="!$v.level.required">Field is required</div>
              </b-row>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-button variant="outline-danger" block @click="hideModal(true)">
                Cancel</b-button>
            </b-col>
            <b-col>
              <b-button variant="outline-warning"
                        block v-on:click="hideModal(); doRects = true;">OK</b-button>
            </b-col>
          </b-row>
        </b-modal>
      </b-col>
    </b-row>
    <b-row>
      <b-col class="ml-2">
        <b-button v-on:click="saveZones(); $router.push({ name: 'Stream',
        params: { type: 'retake', project: nameProject }});">Take another image</b-button>
      </b-col>
    </b-row>
  </b-container>
 </div>
</template>

<script>
import axios from 'axios';
import { required } from 'vuelidate/lib/validators';
import myImg from '../../../server/screen.jpg';

export default {
  name: 'view_img',
  data() {
    return {
      pos_pic: null,
      zoneMode: null,
      zoneName: null,
      mode_options: [
        { value: null, text: 'Choose a type' },
        { value: 'assembly', text: 'Assembly' },
        { value: 'collect', text: 'Collect' },
        { value: 'display', text: 'Display' },
      ],
      level: null,
      level_options: [
        { value: null, text: 'Choose a level' },
        { value: 0, text: 'First level' },
        { value: 1, text: 'Second level' },
        { value: 2, text: 'Third level' },
      ],
      action_options: [
        { value: null, text: 'Choose an action' },
        { value: 'pick', text: 'pick' },
        { value: 'place', text: 'place' },
        { value: 'control', text: 'control' },
      ],
      ctx: null,
      widthCanvas: process.env.VUE_APP_WIDTH,
      select: false,
      nameProject: '',
      saved: false,
      reinit: false,
      doScenario: false,
      doRects: false,
      selectionMode: false,
      img1: new Image(),
      canvas: document.querySelector('canvas'),
      rect: {
        startX: null,
        startY: null,
        w: null,
        h: null,
      },
      startPosition: {
        id: [],
        name: [],
        x: [],
        y: [],
        z: [],
        w: [],
        h: [],
        type: [],
        selected: [],
      },
      name_steps: '',
      scenario: {
        name: '',
        steps: [{
          name: '',
          operations: [],
        }],
      },
      crop: {
        y: null,
        x: null,
        w: null,
        h: null,
      },
    };
  },
  validations: {
    zoneMode: {
      required,
    },
    zoneName: {
      required,
    },
    level: {
      required,
    },
  },
  created() {
  },
  methods: {
    status(validation) {
      return {
        error: validation.$error,
        dirty: validation.$dirty,
      };
    },
    savePosZone(id, step) {
      this.crop.y = this.startPosition.y[id] * (this.img1.height / (this.widthCanvas * 0.5625));
      this.crop.x = this.startPosition.x[id] * (this.img1.width / this.widthCanvas);
      this.crop.w = this.startPosition.w[id] * (this.img1.width / this.widthCanvas);
      this.crop.h = this.startPosition.h[id] * (this.img1.height / (this.widthCanvas * 0.5625));
      console.log(this.startPosition.x[id]);
      const path1 = 'http://localhost:5000/save_pos_zone';
      axios.post(path1, {
        x: this.crop.x,
        y: this.crop.y,
        w: this.crop.w,
        h: this.crop.h,
        steps: step,
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    returnUrlPosImg(folder, name) {
      // eslint-disable-next-line
      let str = `../../../server/store/${folder}/${name}.jpg`;
      try {
        // eslint-disable-next-line
        return require(`../../../server/store/${folder}/${name}.jpg`);
      } catch (e) {
        const path1 = 'http://localhost:5000/save_crop';
        axios.post(path1, {
          folder: this.nameProject, file: `${name}`,
        })
          .catch((error) => {
            // eslint-disable-next-line
          console.error(error);
          });
        // eslint-disable-next-line
       return 'null';
      }
    },
    showModalSave() {
      if (this.saved === false) {
        this.$root.$emit('bv::show::modal', 'modal-save', '#back-save');
      } else {
        this.saveZones();
      }
    },
    hideModal(cancel = false) {
      this.$v.$touch();
      if (this.$v.$invalid && cancel === false) {
        this.submitStatus = 'ERROR';
      } else if (cancel === true) {
        this.$bvModal.hide('modal-zones');
      } else {
        this.$bvModal.hide('modal-zones');
      }
    },
    convertCoordForJson() {
      for (let j = 0; j < this.startPosition.x.length; j += 1) {
        this.startPosition.y[j] *= (this.img1.height / (this.widthCanvas * 0.5625));
        this.startPosition.x[j] *= (this.img1.width / this.widthCanvas);
        this.startPosition.w[j] = this.startPosition.x[j]
          + this.startPosition.w[j] * (this.img1.width / this.widthCanvas);
        this.startPosition.h[j] = this.startPosition.y[j]
          + this.startPosition.h[j] * (this.img1.height / (this.widthCanvas * 0.5625));
      }
    },
    convertCoordForCanvas() {
      for (let j = 0; j < this.startPosition.x.length; j += 1) {
        this.startPosition.y[j] /= (this.img1.height / (this.widthCanvas * 0.5625));
        this.startPosition.x[j] /= (this.img1.width / this.widthCanvas);
        this.startPosition.w[j] = this.startPosition.w[j]
          / (this.img1.width / this.widthCanvas) - this.startPosition.x[j];
        this.startPosition.h[j] = this.startPosition.h[j]
          / (this.img1.height / (this.widthCanvas * 0.5625)) - this.startPosition.y[j];
      }
    },
    saveZones() {
      const path1 = 'http://localhost:5000/savezones';
      const path2 = 'http://localhost:5000/save_scenario';
      const path3 = 'http://localhost:5000/reinit_img';
      this.convertCoordForJson();
      axios.post(path1, { zones: this.startPosition, folder: this.nameProject })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      axios.post(path2, { scenario: this.scenario, folder: this.nameProject }).then(() => {
        if (this.reinit === true) {
          axios.get(path3)
            .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            });
          this.$router.push('/index');
        }
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.convertCoordForCanvas();
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
    removeZone(i) {
      this.startPosition.id.splice(i, 1);
      this.startPosition.x.splice(i, 1);
      this.startPosition.y.splice(i, 1);
      this.startPosition.w.splice(i, 1);
      this.startPosition.h.splice(i, 1);
      this.startPosition.type.splice(i, 1);
      this.startPosition.z.splice(i, 1);
      this.startPosition.selected.splice(i, 1);
      this.ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      this.ctx.drawImage(this.img1, 0, 0, this.widthCanvas,
        this.widthCanvas * (this.img1.height / this.img1.width));
      this.drawOldRects();
    },
    readZones() {
      const path = 'http://localhost:5000/readzones';
      let d;
      this.startPosition.name = [];
      this.startPosition.x = [];
      this.startPosition.y = [];
      this.startPosition.w = [];
      this.startPosition.h = [];
      this.startPosition.type = [];
      axios.get(path, { params: { folder: this.$route.params.load } })
        .then((res) => {
          d = res.data;
          /* eslint-disable */
          for (const [key,value] of Object.entries(d)) {
            for (const [k,v] of Object.entries(value)) {
              this.startPosition.name.push(v.name);
              this.startPosition.x.push(v.x1);
              this.startPosition.y.push(v.y1);
              this.startPosition.w.push(v.x2);
              this.startPosition.h.push(v.y2);
              this.startPosition.z.push(v.Lvl);
              this.startPosition.type.push((v.type));
            }
          }
          this.convertCoordForCanvas();
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
    readScenario() {
      const path = 'http://localhost:5000/readscenario';
      let d;
      axios.get(path, { params: { folder: this.$route.params.load } })
        .then((res) => {
          d = res.data;
          /* eslint-disable */
          this.scenario = d;
          console.log(d.steps)
          if (this.scenario.name !== '') {
            this.doScenario = true;
          }
        /* eslint-enable */
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
    changeType(value) {
      this.zoneMode = value;
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
        this.startPosition.id.push(this.startPosition.name.length);
        this.startPosition.name.push(this.zoneName);
        this.startPosition.x.push(this.rect.startX);
        this.startPosition.y.push(this.rect.startY);
        this.startPosition.w.push(this.rect.w);
        this.startPosition.h.push(this.rect.h);
        this.startPosition.z.push(this.level);
        this.startPosition.type.push(this.zoneMode);
        this.startPosition.selected.push(false);
      }
      this.zoneName = null;
      this.zoneMode = null;
      this.level = null;
      this.selectionMode = false;
      this.doRects = false;
      console.log(this.startPosition.z);
    },
    checkImg() {
      if (this.$route.params.load !== 'None') {
        console.log(this.$route.params.load);
        const path = 'http://localhost:5000/load_img';
        this.nameProject = this.$route.params.load;
        this.saved = true;
        this.readZones();
        this.doScenario = true;
        this.readScenario();
        if (this.$route.params.mode !== 'retake') {
          axios.get(path, { params: { folder: this.$route.params.load } })
            .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            });
        }
      }
    },
  },
  mounted() {
    this.$refs.select.height = this.widthCanvas * 0.5625;
    this.$refs.select.width = this.widthCanvas;
    this.ctx = this.$refs.select.getContext('2d');
    this.insertImg();
    this.checkImg();
  },
};
</script>

<style>
.do_rects {
  cursor: crosshair;
}

.card {
  min-width: 100%;
}

.content_ui {
  margin-right: 0;
  max-width: 100%;
  margin-left: 0;
}
</style>
