<template>
  <el-card shadow="always" id="card">
    <center>
      <h1>欢迎来到USTC Verilog-OJ Wiki</h1>
      <h2>在这里你可以学习Vrilog的基础知识，vivado的实用教程</h2>
      <h2>现在让我们开始吧！</h2>
    </center>
    <el-row :gutter="10">
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <b>verilog基础语法</b>
          </div>
          <div style=" margin-bottom: 18px;">这里有基础的Verilog语法，可以帮助你完成实验</div>
          <div style=" margin-bottom: 18px;">
            <el-button @click="glClick" type="primary">点击学习</el-button>
          <!--  <el-button @click="jiubanClick" type="text">进入旧版</el-button> -->
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <b>vivado基本操作</b>
          </div>
          <div style=" margin-bottom: 18px;">这里有一些vivado的基本操作，可以帮助你入门</div>
          <div style=" margin-bottom: 18px;">
            <el-button @click="mbClick" type="primary">点击学习</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <b>优秀作品</b>
          </div>
          <div style=" margin-bottom: 18px;">这里有优秀的大作业模板，仅供展示</div>
          <div style=" margin-bottom: 18px;">
            <el-button @click="trainningClick" type="primary">点击查看</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
export default {
  name: "wiki",
  data() {
    return {};
  },
  methods: {
    glClick(){
      this.$router.push({
          name: "newalgorithm"
      });
    },
    jiubanClick(){
      this.$router.push({
          name: "algorithm"
      });
    },
    mbClick(){
      this.$router.push({
          name: "mbcode"
      });
    },
    trainningClick(){
      this.$router.push({
          name: "trainning"
      });
    }
  },
  created() {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
