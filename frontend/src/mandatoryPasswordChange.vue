<template>
  <el-dialog title="账户密码更新" :visible.sync="dialogVisible" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false">
    <el-form :model="form" @keyup.native.enter="changeClick">
      <el-row :gutter="10">
        <p>为了增强用户账户的安全性，请设置更安全的密码。</p>
        <p>密码应该满足如下的要求：</p>
        <ul :key="index" v-for="(item, index) in passwordRequirements">
          <li>{{ item }}</li>
        </ul>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">新密码</div>
        </el-col>
        <el-col :span="12">
          <el-input
            type="password"
            v-model="form.password"
            autocomplete="off"
            placeholder="账户的新密码"
          ></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">确认新密码</div>
        </el-col>
        <el-col :span="12">
          <el-input
            type="password"
            v-model="form.confirmPassword"
            autocomplete="off"
            placeholder="重复输入账户的新密码"
          ></el-input>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="doLogout">退出登录</el-button>
      <el-button type="primary" @click="changeClick">确定</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: "mandatoryPasswordChange",
  props: {
    dialogVisible: Boolean,
  },
  data() {
    return {
      passwordRequirements: [],
      form: {
        password: "",
        confirmPassword: "",
      },
    };
  },
  created() {
    this.fetchRequirements();
  },
  methods: {
    fetchRequirements() {
      this.$axios.get("/user/password-strength-validation/").then((response) => {
        this.passwordRequirements = response.data.password_requirements;
      })
    },
    changeClick() {
      if (this.form.password != this.form.confirmPassword) {
        this.$message.error("您输入的密码和确认密码不一致，请重新输入");
        return;
      }

      this.$axios
        .post("/user/password-strength-validation/", {password: this.form.password})
        .then((response) => {
          // Validation successful
          this.$axios.patch("/users/" + this.$store.state.userID + "/", {
            "password": this.form.password
          }).then((response) => {
            this.$message({
              message: "密码修改成功！",
              type: "success",
            });
            this.$store.dispatch("refreshLogInStatus");
          }).catch((error) => {
            this.$message.error(
              "密码修改失败：\n" + error.response.data
            );
          });
        })
        .catch((error) => {
          this.$message.error(
            "密码强度校验失败：\n" + error.response.data.errors.join("\n")
          );
        });
    },
    doLogout() {
      this.$store.dispatch("logOut", {
          // Note on JS newbie:
          // () => {} don't provide their own this binding
          // while function () {} provides
          success_cb: () => {
            this.$message({
              message: "登出成功！",
              type: "success",
            });
          },
          fail_cb: (error) => {
            this.$message.error(
              "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
            );
          },
        });
    },
  },
};
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}
</style>
