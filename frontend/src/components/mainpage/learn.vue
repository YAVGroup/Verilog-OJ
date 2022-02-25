<template>
  <div>
    <el-row> &nbsp; </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <el-row>
            <el-card shadow="never">
            <el-row>
                <h3 style="display: inline-block; margin: 3px 0px">
                欢迎您向 Verilog OJ 贡献题目！
                </h3>
            </el-row>
            <el-row>
                <div>
                Verilog OJ
                测试期间需要大家的反馈和配合。我们为新手上路的各位准备了常用的模板，帮助大家完成简单题目的创建。
                </div>
                <div>
                更多信息您可以查看
                <a
                    href="https://github.com/YAVGroup/Verilog-OJ/blob/master/doc/operation/Problem_add_HOWTO.md"
                    >Verilog OJ 出题指南</a
                >。
                </div>
            </el-row>
            </el-card>
        </el-row>

        <el-row>
          <div style="white-space: pre-wrap">
            111
          </div>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "learn",
  data() {
    return {
      news: [],
    };
  },
  methods: {
    
  },
  created() {
    // this.$axios.get("/news/").then((response) => {
    //   this.news = response.data;
    // });
  },
};
</script>

<style scoped>

</style>
