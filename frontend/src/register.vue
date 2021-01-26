<template>
  <el-dialog title="注册"
             :visible.sync="dialogRegisterVisible">
    <el-form :model="form"
             @keyup.native.enter="registerClick">
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">用户名</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.username"
                    autocomplete="off"
                    placeholder="不少于 3 个字符的用户名"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">密码</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password"
                    v-model="form.password"
                    autocomplete="off"
                    placeholder="不少于 6 个字符的密码"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">确认密码</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password"
                    v-model="form.confirm"
                    autocomplete="off"
                    placeholder="请重复密码"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">姓氏</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.last_name"
                    autocomplete="off"
                    placeholder="姓氏，选填"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">名字</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.first_name"
                    autocomplete="off"
                    placeholder="名字，选填"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">Email</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.email"
                    autocomplete="off"
                    placeholder="用于通知邮件发送"></el-input>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer"
         class="dialog-footer">
      <el-button @click="dialogRegisterVisible = false">取 消</el-button>
      <el-button type="primary"
                 @click="registerClick">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: "register",
  data () {
    return {
      dialogRegisterVisible: false,
      form: {
        username: "",
        password: "",
        confirm: "",
        last_name: "",
        first_name: "",
        email: ""
      }
    };
  },
  methods: {
    open () {
      this.dialogRegisterVisible = true;
    },
    registerClick () {
      if (this.form.password != this.form.confirm) {
        this.$message.error("两次密码不一致！");
        return;
      }
      if (this.form.username.length < 3) {
        this.$message.error("用户名太短！");
        return;
      }
      if (this.form.password.length < 6) {
        this.$message.error("密码太短！");
        return;
      }
      if (
        this.form.username.indexOf("|") >= 0 ||
        this.form.username.indexOf(".") >= 0 ||
        this.form.username.indexOf("#") >= 0
      ) {
        this.$message.error("用户名包含非法字符！");
        return;
      }
      if (
        this.form.username.indexOf("{") >= 0 ||
        this.form.username.indexOf("(") >= 0 ||
        this.form.username.indexOf(")") >= 0
      ) {
        this.$message.error("用户名包含非法字符！");
        return;
      }

      this.$axios
        .post("/user/signup/", this.form)
        .then(response => {
          this.$message({
            message: "注册成功！",
            type: "success"
          });
          this.dialogRegisterVisible = false;
        })
        .catch(error => {
          this.$message.error(
            "注册失败：" + JSON.stringify(error.response.data)
          );
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
