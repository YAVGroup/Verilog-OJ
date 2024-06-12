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
          <el-col>
            <i class="el-icon-info"></i>
              用户账户设置
          </el-col>
        </el-row>
        <el-card shadow="none" id="card"
                v-loading="!loggedIn"
                element-loading-text="登陆以修改用户账户信息"
                element-loading-spinner="el-icon-info">
          <el-form :model="form">
            <el-row :gutter="10">
              <el-col :span="3">
                <div style="text-align: center; margin: 5px">用户名</div>
              </el-col>
              <el-col :span="12">
                <el-input v-model="form.username" autocomplete="off"></el-input>
              </el-col>
            </el-row>
            <el-row :gutter="10">
              <p>为了增强用户账户的安全性，请设置安全的密码。</p>
              <p>密码应该满足如下的要求：</p>
              <ul :key="index" v-for="(item, index) in passwordRequirements">
                <li>{{ item }}</li>
              </ul>
            </el-row>
            <el-row :gutter="10">
              <el-col :span="3">
                <div style="text-align: center; margin: 5px">
                  新密码
                </div>
              </el-col>
              <el-col :span="12">
                <el-input
                  type="password"
                  v-model="form.password"
                  placeholder="请输入新密码"
                  autocomplete="off"
                ></el-input>
              </el-col>
            </el-row>
            <el-row :gutter="10">
              <el-col :span="3">
                <div style="text-align: center; margin: 5px">确认密码</div>
              </el-col>
              <el-col :span="12">
                <el-input
                  type="password"
                  v-model="form.confirmPassword"
                  placeholder="请输入确认密码"
                  autocomplete="off"
                ></el-input>
              </el-col>
            </el-row>
          </el-form>

          <el-button type="primary" @click="updateClick">更新</el-button>
        </el-card>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "setting",
  data() {
    return {
      passwordRequirements: [],
      form: {
        username: "",
        password: "",
        confirmPassword: "",
      },
    };
  },
  methods: {
    updateClick() {
      if (!this.form.username) {
        this.$message.error("请输入新的用户名");
        return;
      }
      
      if (this.form.password != this.form.confirmPassword) {
        this.$message.error("您输入的密码和确认密码不一致，请重新输入");
        return;
      }

      this.$axios
        .post("/user/password-strength-validation/", {password: this.form.password})
        .then((response) => {
          // Validation successful
          this.$axios.patch("/users/" + this.$store.state.userID + "/", {
            "username": this.form.username,
            "password": this.form.password
          }).then((response) => {
            this.$message({
              message: "修改成功！",
              type: "success",
            });
            this.$store.dispatch("refreshLogInStatus");
          }).catch((error) => {
            this.$message.error(
              "修改失败：\n" + JSON.stringify(error.response.data)
            );
            this.$store.dispatch("refreshLogInStatus");
          });
        })
        .catch((error) => {
          this.$message.error(
            "密码强度校验失败：\n" + error.response.data.errors.join("\n")
          );
        });
    },
  },
  created() {
    this.form.username = this.$store.state.username;
    this.$axios.get("/user/password-strength-validation/").then((response) => {
      this.passwordRequirements = response.data.password_requirements;
    })
  },
  computed: mapState(
    ["loggedIn"]
  ),
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-row {
  margin-bottom: 20px;
}
</style>
