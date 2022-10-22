<template>
    <div>
      <el-row> &nbsp; </el-row>
      <el-row>
        <el-col :xs="0" :sm="2" :md="4" :lg="5" :xl="6" class="placeholder">
          <!-- placeholder only -->
          &nbsp;
        </el-col>
        <el-col :xs="24" :sm="20" :md="16" :lg="14" :xl="12">
          <el-row class="main-title">
            <i class="el-icon-document"></i>
            专题练习：{{ this.name }}
          </el-row>
          <el-divider></el-divider>
          <el-row>
            <markdownIt :mdSource="this.content"></markdownIt>
          </el-row>
        </el-col>
      </el-row>
    </div>
</template>

<script>

  import markdownIt from "@/components/utils/markdownIt";

  export default {
    name: "learndetail",
    components: {
      markdownIt
    },
    data() {
      return {
        bookID: 0,
        name: "",
        description_short: "",
        content: ""
      }
    },
    methods: {
      
    },
    created() {
      this.bookID = this.$route.params.bookid;
      this.$axios.get("/problem-books/" + this.bookID + "/").then((response) => {
        this.name = response.data.name;
        this.description_short = response.data.description_short;
        this.content = response.data.content;
      });
    },
  };
</script>
  
<style scoped>
.main-title {
  font-size: 20px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}
</style>
  