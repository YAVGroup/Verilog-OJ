<template>
  <div>
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
    text: function() {
      try {
        if (this.text == "") {
            console.log("asdfasdfasdfasdfasdfasdfasdf")
            throw 'Waveform data empty';
        } 
        WaveDrom.renderWaveForm(this.waveId, JSON.parse(this.text), 'waveform');
        this.isError = false;
      } catch (e) {
        console.warn(e);
        this.isError = true;
      }
    },
    parentText: function() {
      this.text = this.parentText;
    }
  }
}
</script>

<style scoped>
</style>