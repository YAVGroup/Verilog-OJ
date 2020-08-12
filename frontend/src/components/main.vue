<template>
  <el-row :gutter="12">
    <el-col :span="6">
      <el-row :gutter="10"><welcomemessage></welcomemessage></el-row>

      <el-row :gutter="10">
      <!-- <el-card style="height:150px;" :body-style="{ padding: '0px' }"> -->
        <el-carousel height="150px" direction="horizontal" arrow="never" :interval="6000">
          <el-carousel-item v-for="item in tables" :key="item.msg">
              <div style="margin:20px;" v-html="item.msg"></div>
          </el-carousel-item>
        </el-carousel>
      <!-- </el-card> -->

      <!-- <el-row :gutter="10"><topuser></topuser></el-row> -->
      </el-row>
    </el-col>

    <el-col :span="18">
      <el-row>
        <el-tabs type="border-card">
          <el-tab-pane :label="'Description'"><description></description></el-tab-pane>
          <el-tab-pane :label="'Rule'" :lazy="true"><ratingrule></ratingrule></el-tab-pane>
        </el-tabs>
      </el-row>
      <el-row>
        <!--<contestmini></contestmini>-->
      </el-row>
    </el-col>
  </el-row>
</template>

<script>

import welcomemessage from "@/components/utils/welcomemessage";
//import topuser from "@/components/utils/topuser";
import ratingrule from "@/components/utils/ratingrule";
//import contestmini from "@/components/utils/contestmini";
import description from "@/components/utils/description";
export default {
  components: {
    welcomemessage,
    //topuser,
    ratingrule,
    //contestmini,
    description,
  },
  name: "homepage",
  data() {
    return {
      tables: [{'msg':'假装这里是新闻1'}, {'msg':'假装这里是新闻2'}, {'msg':'假装这里是新闻3'}]
    };
  },
  created() {
    //这里后端无接口，可以后期加上（画饼
    /*
    this.$axios.get("/banner/").then(response => {
      this.tables = response.data;
    });
    */
  }
};
</script>

<style scoped>
.el-row {
  margin-bottom: 12px;
}

.el-carousel__item:nth-child(2n) {
  background-color: #ffffff;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #ffffff;
}
</style>
