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
    <a href="/api/user/ustc-login">统一身份认证登录</a>
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
      this.$store.dispatch('logIn', {
        username: this.form.username,
        password: this.form.password,
        // Note on JS newbie:
        // () => {} don't provide their own this binding
        // while function () {} provides
        success_cb: () => {
          this.$message({
            message: "登录成功！",
            type: "success"
          });
          this.dialogLoginVisible = false;
        },
        fail_cb: (error) => {
          if (error.response != undefined)
            this.$message.error("登录失败：" + JSON.stringify(error.response.data));
          else
            this.$message.error("抱歉，似乎出了点问题");
        }
      })
    }
  }
};
</script>

<style  scoped>
.el-row {
  margin-bottom: 20px;
}
</style>
