<template>
  <div>
    <el-row>
      <el-col>
        <el-steps align-center>
          <el-step
            title="题目描述"
            description="描述题目的信息、设置截止时间等"
          ></el-step>
          <el-step
            title="端口编辑"
            description="编辑输入与输出的端口"
          ></el-step>
          <el-step title="测试波形" description="编辑测试样例的波形"></el-step>
          <el-step title="参考答案" description="给出问题的参考答案"></el-step>
        </el-steps>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {};
</script>
