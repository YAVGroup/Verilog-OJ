<template>
  <div style="overflow: auto;">
    <div v-show="isError" id="wavedrom-error">{{ errorMessage }}</div>
    <div :id="'waveform' +  waveId"></div>
  </div>
</template>

<script>
window.WaveSkin = require('wavedrom/skins/default.js');
var WaveDrom = require('wavedrom');
export default {
  name: 'wavedrom',
  props: {
    waveId: String,
    parentText: String,
    errorMessage: String
  },
  data() {
    return {
      text: this.parentText,
      isError: false
    }
  },
  watch: {
    text: {
      handler: function (newVal, oldVal) {
        // Delay rendering until real DOM created, 
        // or WaveDrom will fail to get the desired element
        this.$nextTick(function () {
          // Code that will run only after the
          // entire view has been re-rendered
          try {
            if (this.text == "") {
                throw 'Waveform data empty';
            }
            // console.log(this.text)
            // console.log(this.waveId)
            WaveDrom.renderWaveForm(this.waveId, JSON.parse(this.text), 'waveform');
            document.getElementById("svgcontent_" + this.waveId).setAttribute("overflow", "auto");
            this.isError = false;
          } catch (e) {
            console.warn(e);
            this.isError = true;
          }
        })
      },
      immediate: true
    },
    parentText: function() {
      this.text = this.parentText;
    }
  },
}
</script>

<style scoped>
</style>