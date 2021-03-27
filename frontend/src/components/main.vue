<template>
  <div>
    <el-row> </el-row>
    <el-row :gutter="12">
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="12" :sm="10" :md="8" :lg="6" :xl="6">
        <el-row>
          <div class="home-frame">
            <newsboard></newsboard>
          </div>
        </el-row>
      </el-col>
      <el-col :xs="12" :sm="10" :md="8" :lg="6" :xl="6">
        <el-row>
          <div class="home-frame">
            <probsearch></probsearch>
          </div>
        </el-row>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <welcomemessage></welcomemessage>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import welcomemessage from "@/components/utils/welcomemessage";
//import topuser from "@/components/utils/topuser";
//import ratingrule from "@/components/utils/ratingrule";
import newsboard from "@/components/utils/newsboard";
import probsearch from "@/components/utils/probsearch";

export default {
  components: {
    welcomemessage,
    //topuser,
    //ratingrule,
    newsboard,
    probsearch,
  },
  name: "homepage",
  data() {
    return {
      tables: [
        { msg: "假装这里是新闻1" },
        { msg: "假装这里是新闻2" },
        { msg: "假装这里是新闻3" },
      ],
    };
  },
  created() {
    //这里后端无接口，可以后期加上（画饼
    /*
    this.$axios.get("/banner/").then(response => {
      this.tables = response.data;
    });
    */
  },
};
</script>

<style scoped>
.home-frame {
  /* box-shadow: 0 1px 2px rgba(0, 0, 0, .12), 0 0 8px rgba(0, 0, 0, .04); */
  padding: 12px 10px 10px 12px;
}
</style>
