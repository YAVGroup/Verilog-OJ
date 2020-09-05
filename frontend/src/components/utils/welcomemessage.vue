<template>
  <div>
      <el-col :offset="1" :span="22">
        <h2>欢迎您使用 Verilog 在线评测服务</h2>

        <p>本评测服务由 Yet Another Verilog Group 小组开发，提供 Verilog 题目在线评测和可视化功能。</p>
        <p>本服务综合了不同难度的数字电路设计问题，适合各种水平的数字电路学习者。您输入的 Verilog 模块将会通过一系列向量，并与标准模块对应的输出来评价您实现的正确性。</p>
        <p>除了正确性评测之外，部分设计问题还要求您的实现满足给定的时序约束，同时用实现的 LUT 和触发器数目判断您的电路的质量。</p>
      </el-col>

  </div>

  <!-- <div class="sub-header">
    <b>Welcome to USTC Verilog OJ</b>
  </div>
  <b>Version：developing</b>
  <br>
  <h3><a href="https://github.com/lluckydog/Verilog-OJ" target="_blank" style="text-decoration: none;color:#409EFF;">Github </a></h3>
  <h3><a href="https://github.com/lluckydog/Verilog-OJ" target="_blank" style="text-decoration: none;color:#67C23A;">Documentation</a></h3> -->

</template>

<script>
export default {
  name: "welcomemessage",
};
</script>

<style  scoped>
</style>
