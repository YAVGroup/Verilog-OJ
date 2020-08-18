<template>
  <div>
    <el-row class="home-title">
      <i class="el-icon-thumb"></i>
      快速搜索
    </el-row>

    <el-row>
      <el-col offset="1" span="22">
        <el-input v-model="input" placeholder="输入题号，快速跳转" prefix-icon="el-icon-search"></el-input>
        
      </el-col>
    </el-row>

  </div>
</template>

<script>
export default {
  name: "probsearch",
  data() {
    return {
      input: ''
    };
  },
  methods:{
    
  }
};
</script>

<style scoped>

.news-item {
  /* background-color: #fafafb; */
  list-style: none;
  padding-left: 5px;
}

.news-item a:link, .news-item a:visited {
  color: #333;
  text-decoration: none;
}

.news-item a:hover {
  color: #333;
  text-decoration: underline;
}

.home-title {
  font-size: 20px;
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}

</style>