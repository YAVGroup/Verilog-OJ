<template>
  <el-dialog title="登录" :visible.sync="dialogLoginVisible">
    <el-form :model="form" @keyup.native.enter="loginClick">
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">User</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.username" autocomplete="off" :autofocus="true"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">Password</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password" v-model="form.password" autocomplete="off"></el-input>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogLoginVisible = false">Cancel</el-button>
      <el-button type="primary" @click="loginClick">OK</el-button>
    </div>
    <a href="/api/user/ustc-login">统一身份认证登陆</a>
  </el-dialog>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      dialogLoginVisible: false,
      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    open() {
      this.dialogLoginVisible = true;
    },
    loginClick() {
      this.$axios
        .post("/user/login/", {
          username: this.form.username,
          password: this.form.password
        })
        .then(response => {
          this.$message({
            message: "登录成功！",
            type: "success"
          });
          sessionStorage.setItem("username", this.form.username);
          if (response.data.last_name == "" && response.data.first_name == "")
            sessionStorage.setItem("name", this.form.username);
          else
            sessionStorage.setItem("name", response.data.last_name+response.data.first_name);
          sessionStorage.setItem("userid", response.data.id);

          sessionStorage.setItem("isadmin", response.data.is_superuser);
          this.$router.go(0);
        })
        .catch(error => {
          if (error.response != undefined)
            this.$message.error("登录失败：" + JSON.stringify(error.response.data));
          else
            this.$message.error("抱歉，似乎出了点问题");
          console.log(error);
        });
    }
  }
};
</script>

<style  scoped>
.el-row {
  margin-bottom: 20px;
}
</style>
