<template>
  <div>
    <el-row> </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        您所请求的页面不存在，请重新尝试。
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  components: {},
  name: "notfound",
  data() {
    return {};
  },
};
</script>

<style scoped></style>
