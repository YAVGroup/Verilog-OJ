<template>
  <div>
    <el-option v-for="item in languagelist" :key="item" :label="item" :value="item"></el-option>
  </div>
</template>

<script>
export default {
  name: "languageselect",

  data() {
    return {
      languagelist: ["Verilog"]
    };
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
