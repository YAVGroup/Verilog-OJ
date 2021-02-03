<template>
  <el-card shadow="always" id="card">
    <center>
      <h1 :style="color">{{ name }}</h1>
      <!-- <h1 :style="color">{{ username }}</h1> -->
      <!-- <h4 :style="color">{{ email }}</h4> -->
      <h4 :style="color">{{ student_id }}</h4>
    </center>

    <el-row>
      <el-col :span="8">
        <center>
          <h2 :style="color">Submitted</h2>
          <h3 :style="color">{{ submitted }}</h3>
        </center>
      </el-col>
      <el-col :span="8">
        <center>
          <h2 :style="color">AC</h2>
          <h3 :style="color">{{ ac }}</h3>
        </center>
      </el-col>
      <el-col :span="8">
        <center>
          <h2 :style="color">Score</h2>
          <h3 :style="color">{{ score }}</h3>
        </center>
      </el-col>
    </el-row>

    <center>
      <h2 :style="color">AC Problems</h2>
      <br>
    </center>
    <el-button
      id="tag"
      v-for="ac_problem_id in ac_problems"
      :key="ac_problem_id"
      size="small"
      @click="problemclick(ac_problem_id)"
      type="success"
      style="width:70px;"
    >{{ ac_problem_id }}</el-button>
  </el-card>
</template>

<script>
export default {
  name: "user",
  data() {
    return {
      username: "",
      name: "",
      student_id: "",
      ac: "", // AC的题目数
      submitted: "", // 提交的题目数
      score: "", // 提交的题目分数总和
      ac_problems: [], // AC的题目列表
      color: ""
    };
  },
  computed: {
    userid: function() {
      return this.$route.params.userid;
    }
  },
  watch: {
    userid: function() {
      this.updateUserInfo();
    }
  },
  methods: {
    problemclick(id) {
      console.log("problemclick " + id);
      this.$router.push({
        name: "problemdetail",
        params: { problemid: id }
      });
    },
    updateUserInfo: function() {
      // if (this.userid) {
        this.$axios.get("/users/" + this.userid + "/").then(response => {
          this.username = response.data.username;
          if (response.data.last_name == "" && response.data.first_name == "")
            this.name = this.username;
          else
            this.name = response.data.last_name + response.data.first_name;
          this.email = response.data.email;
          if(response.data.student_id == null)
            this.student_id = "";
          else
            this.student_id = response.data.student_id;

          this.ac_problems = response.data.ac_problems;
          this.ac = this.ac_problems.length;
          this.submitted = response.data.submitted_problems.length;
          this.score = response.data.total_score;

          if (response.data.is_superuser)
            this.color = "color: red; font-weight: bold;"
          else
            this.color = "color: black; font-weight: bold";
        }).catch(error => {
          this.$message.error("服务器错误：" + JSON.stringify(error.response.data));
        });
      // }
    }
  },
  created: function () {
    this.updateUserInfo();
  }
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
