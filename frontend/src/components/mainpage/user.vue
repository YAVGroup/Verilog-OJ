<template>
  <div>
    <el-row> &nbsp; </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <el-card shadow="never">
          <el-row class="main-title">
            <i class="el-icon-user"></i>
            {{ name }} 的主页
          </el-row>
          <el-divider></el-divider>
          <el-descriptions>
            <el-descriptions-item label="UID">{{ userid }}</el-descriptions-item>
            <el-descriptions-item label="用户名">{{ username }}</el-descriptions-item>
            <el-descriptions-item label="姓名">{{ name }}</el-descriptions-item>
            <el-descriptions-item label="学号">{{student_id}}</el-descriptions-item>
            <el-descriptions-item label="管理员">{{is_superuser ? "是" : "否"}}</el-descriptions-item>
            <el-descriptions-item label="总分">{{score}}</el-descriptions-item>
          </el-descriptions>
          <el-divider></el-divider>
          <el-row>
            {{ name }} 在本站通过了 {{ numACProblems }} 道题目。
          </el-row>
          <el-button
            id="tag"
            v-for="ac_problem in ac_problems"
            :key="ac_problem.id"
            size="small"
            @click="problemclick(ac_problem.id)"
            type="success"
            style="width: 50px"
            >{{ ac_problem.logic_id }}</el-button
          >
          <el-divider></el-divider>
          <el-row>
            截至目前，{{ name }} 还有 {{ numUndoneProblems }} 道题目没有做完。
          </el-row>
          <el-button
            id="tag"
            v-for="undone_problem in undone_problems"
            :key="undone_problem.id"
            size="small"
            @click="problemclick(undone_problem.id)"
            :type="checkSubmitted(undone_problem.id) ? 'info' : ''"
            style="width: 50px"
            >{{ undone_problem.logic_id }}</el-button
          >
        </el-card>
        


      </el-col>
    </el-row>
  </div>

</template>

<script>
export default {
  name: "user",
  data() {
    return {
      username: "",
      name: "",
      student_id: "",
      submitted: "", // 提交的题目数
      score: "", // 提交的题目分数总和
      ac_problems: [], // AC的题目列表
      submitted_problems: [],
      undone_problems: [],
      is_superuser: false,
    };
  },
  computed: {
    userid: function () {
      return this.$route.params.userid;
    },
    numACProblems: function () {
      return this.ac_problems.length;
    },
    numUndoneProblems: function () {
      return this.undone_problems.length;
    },
    allSubmittedProblemId: function () {
      let submittedId = [];
      for (let i = 0; i < this.submitted_problems.length; i++) {
        submittedId.push(this.submitted_problems[i].id);
      }

      return submittedId;
    }
  },
  watch: {
    userid: function () {
      this.updateUserInfo();
    },
  },
  methods: {
    checkSubmitted(id) {
      return this.allSubmittedProblemId.includes(id);
    },
    problemclick(id) {
      this.$router.push({
        name: "problemdetail",
        params: { problemid: id },
      });
    },
    updateUserInfo: function () {
      // if (this.userid) {
      this.$axios
        .get("/users/" + this.userid + "/")
        .then((response) => {
          this.username = response.data.username;
          if (response.data.last_name == "" && response.data.first_name == "")
            this.name = this.username;
          else this.name = response.data.last_name + " " + response.data.first_name;
          this.email = response.data.email;
          if (response.data.student_id == null) this.student_id = "";
          else this.student_id = response.data.student_id;

          this.ac_problems = response.data.ac_problems;
          this.undone_problems = response.data.undone_problems;
          this.submitted_problems = response.data.submitted_problems;
          this.score = response.data.total_score;

          this.is_superuser = response.data.is_superuser;
        })
        .catch((error) => {
          this.$message.error(
            "服务器错误：" + JSON.stringify(error.response.data)
          );
        });
      // }
    },
  },
  created: function () {
    this.updateUserInfo();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#card {
  margin: 200px;
  padding: 200px;
}
#tag {
  text-align: center;
  font-weight: bold;
  margin-left: 7px;
  margin-bottom: 7px;
}
</style>
