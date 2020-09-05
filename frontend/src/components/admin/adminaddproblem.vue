<template>
  <el-form ref="addproblemform" :model="addproblemform" label-position="right">
    <!-- <h3><a style="text-decoration: none;color:#67C23A;" target="_blank" href="https://docs.lpoj.cn/doc/oj.html#%E7%AE%A1%E7%90%86%E5%91%98%E9%A1%B5%E9%9D%A2%E8%AF%B4%E6%98%8E">具体使用，点我看管理员文档</a></h3>
    <el-form-item label="题目编号：">
      <el-input v-model="addproblemform.problem" style="width:400px;" readonly></el-input>
    </el-form-item>
    <el-form-item label="特殊选项：添加其他OJ题目用！不知道的话请忽略">
      <el-input v-model="addproblemform.oj" placeholder="OJ" style="width:100px;"></el-input>
      <el-input
        v-model="addproblemform.source"
        placeholder="Pro ID"
        style="width:100px;margin-left:40px;"
      ></el-input>
    </el-form-item>
    <el-form-item label="作者：">
      <el-input v-model="addproblemform.author" style="width:400px;"></el-input>
    </el-form-item> -->
    <el-form-item label="标题：">
      <el-input v-model="addproblemform.name" style="width:400px;"></el-input>
    </el-form-item>
    <el-form-item label="题目描述：">
      <el-input type="textarea" v-model="addproblemform.description" autosize style="width:800px;"></el-input>
    </el-form-item>
    <el-form-item label="输入描述：">
      <el-input type="textarea" v-model="addproblemform.description_input" autosize style="width:800px;"></el-input>
    </el-form-item>
    <el-form-item label="输出描述：">
      <el-input type="textarea" v-model="addproblemform.description_output" autosize style="width:800px;"></el-input>
    </el-form-item>

    <el-form-item>
      <el-upload style="width:400px;" ref="upload_description" action=""
        :http-request="upload" :on-success="onSuccessForDescription" :on-error="onError" :before-remove="beforeRemove"
        multiple :file-list="descriptionFileList">
        <el-button slot="trigger" size="small" type="primary">上传额外的描述文件</el-button>
      </el-upload>
    </el-form-item>

    <el-form-item label="是否设置DDL">
      <el-switch v-model="haveddl" active-text="是" inactive-text="否"></el-switch>
    </el-form-item>

    <el-form-item label="DDL（暂时请输入文本）" v-show="haveddl">
      <el-input v-model="ddl" autosize style="width:800px;"></el-input>
    </el-form-item>

    <el-form-item label="难度：">
      <el-select v-model="addproblemform.level" placeholder="请选择" style="width:200px;">
        <el-option key="1" label="简单" :value="1"></el-option>
        <el-option key="2" label="普通" :value="2"></el-option>
        <el-option key="3" label="中等" :value="3"></el-option>
        <el-option key="4" label="困难" :value="4"></el-option>
        <el-option key="5" label="极其困难" :value="5"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="标签（用|分割）：">
      <el-input v-model="addproblemform.tags" style="width:400px;"></el-input>
    </el-form-item>
    <!-- <el-form-item label="分数（建议100~10000）：">
      <el-input-number
        style="width:200px;"
        v-model="addproblemform.score"
        :step="100"
        :min="100"
        :max="10000"
      ></el-input-number>
    </el-form-item> -->

    <el-form-item>
      <el-upload style="width:400px;" ref="upload_template" action=""
        :http-request="upload" :on-success="onSuccessForTemplateCode" :on-error="onError" :before-remove="beforeRemove"
        :limit="1" :file-list="templateCodeFileList">
        <el-button slot="trigger" size="small" type="primary">上传模板代码文件</el-button>
      </el-upload>
    </el-form-item>

    <el-form-item>
      <el-upload style="width:400px;" ref="upload_judge" action=""
        :http-request="upload" :on-success="onSuccessForJudge" :on-error="onError" :before-remove="beforeRemove"
        multiple :file-list="judgeFileList">
        <el-button slot="trigger" size="small" type="primary">上传测试用的文件</el-button>
        <div slot="tip" class="el-upload__tip">包括评测脚本、标准解答、testbench等，具体格式还有待讨论</div>
      </el-upload>
    </el-form-item>

    <el-button type="success" @click="addProblem" style="float:right;">添加题目</el-button>
  </el-form>
</template>

<script>
export default {
  name: "admin",
  data() {
    return {
      problemcount: 0,

      descriptionFileList: [],
      templateCodeFileList: [],
      judgeFileList: [],

      haveddl: false,
      ddl: "",

      addproblemform: {
        name: "题目标题",
        description: "题目说明",
        description_input: "输入说明",
        description_output: "输出说明",

        // deadline_time: null,
        description_files: [],
        template_code_file: null,
        judge_files: [],

        tags: "简单题|模拟",
        // template:
        //   "*****Verilog*****\n\n",
        level: 1,
      },
    };
  },
  methods: {
    upload (content) {
      var formData = new FormData();
      formData.append('file', content.file);
      this.$axios.post("/files/", formData).then(response => {
        content.onSuccess(response);
      }).catch(error => {
        this.$message.error("上传失败：" + error.response.data);
        content.onError();
      })
    },

    onSuccessForDescription (response, file, fileList) {
      this.descriptionFileList = fileList;
      this.$message.success("上传成功");
    },
    onSuccessForTemplateCode (response, file, fileList) {
      this.templateCodeFileList = fileList;
      this.$message.success("上传成功");
    },
    onSuccessForJudge (response, file, fileList) {
      this.judgeFileList = fileList;
      this.$message.success("上传成功");
    },

    onError (error, file, fileList) {
      this.$message.error("上传失败：" + JSON.stringify(error.response.data));
    },

    beforeRemove (file, fileList) {
      this.$axios.delete("/api/files/" + file.response.id + "/").then(response => {
        this.$message.success("删除成功");
        return true;
      }).catch(error => {
        this.$message.error("删除失败！");
        return false;
      })
    },

    addProblem() {
      if (this.templateCodeFileList.length > 1){
        this.$message.error("模板代码文件至多一个");
        return;
      }

      this.$confirm("确定添加吗？", "添加题目", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(resonse => {
        if(this.haveddl)
          this.addproblemform.deadline_time = this.ddl;

        for (const file of this.descriptionFileList)
          this.addproblemform.description_files.push(file.response.data.id);
        if(this.templateCodeFileList.length == 1)
          this.addproblemform.template_code_file = this.templateCodeFileList[0].response.data.id;
        for (const file of this.judgeFileList)
          this.addproblemform.judge_files.push(file.response.data.id);

        this.$axios.post("/problems/", this.addproblemform).then(response => {
          this.$message.success("题目添加成功！");
        }).catch(error => {
          this.$message.error("题目添加失败：" + JSON.stringify(error.response.data));
        })
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
