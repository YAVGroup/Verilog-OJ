<template>
  <el-tabs type="border-card" v-show="canshow" v-loading="loading">
    <el-tab-pane label="添加题目">
      <adminaddproblem></adminaddproblem>
    </el-tab-pane>
    <!-- <el-tab-pane label="添加比赛"
                 :lazy="true">
      <adminaddcontest></adminaddcontest>
    </el-tab-pane> -->

    <!-- <el-tab-pane label="题目列表"
                 :lazy="true">
      <adminchangepro></adminchangepro>
    </el-tab-pane> -->
    <!-- <el-tab-pane label="比赛列表"
                 :lazy="true">
      <adminchangecontest></adminchangecontest>
    </el-tab-pane> -->
    <!-- <el-tab-pane label="用户列表"
                 :disabled="!isadmin"
                 :lazy="true">
      <adminmanageuser></adminmanageuser>
    </el-tab-pane> -->

    <!-- <el-tab-pane label="Rejudge"
                 :disabled="!isadmin"
                 :lazy="true">
      <adminrejudge></adminrejudge>
    </el-tab-pane> -->

    <!-- <el-tab-pane label="班级管理"
                 :lazy="true">
      <adminclassmanage></adminclassmanage>
    </el-tab-pane> -->
  </el-tabs>
</template>

<script>
import adminaddproblem from "@/components/admin/adminaddproblem";
// import adminaddcontest from "@/components/admin/adminaddcontest";
// import adminchangepro from "@/components/admin/adminchangepro";
// import adminchangecontest from "@/components/admin/adminchangecontest";
// import adminmanageuser from "@/components/admin/adminmanageuser";
// import adminrejudge from "@/components/admin/adminrejudge";
// import adminclassmanage from "@/components/admin/adminclassmanage";

export default {
  name: "admin",
  components: {
    adminaddproblem,
    // adminaddcontest,
    // adminchangepro,
    // adminchangecontest,
    // adminmanageuser,
    // adminrejudge,
    // adminclassmanage,
  },
  data() {
    return {
      type: 1,
      canshow: false,
      loading: true,
    };
  },
  methods: {},
  created() {
    this.canshow = true;
  },
  mounted() {
    this.loading = false;
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  position: relative;
}
</style>
