<template>
  <div>
    <el-row>
      <el-col>
        <basicinfo v-if="true"></basicinfo>
        <portinfo v-if="false"></portinfo>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <comb-steps></comb-steps>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import combSteps from "./combSteps.vue";
import basicinfo from "./basicinfo.vue";
import portinfo from "./portinfo.vue";

export default {
  components: {
    combSteps,
    basicinfo,
    portinfo,
  },
};
</script>
