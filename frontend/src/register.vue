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
                    placeholder="不少于3个字符的用户名，必填"></el-input>
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
                    placeholder="不少于6个字符的密码，必填"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">确认密码</div>
        </el-col>
        <el-col :span="12">
          <el-input type="password"
                    v-model="form.comfirm"
                    autocomplete="off"
                    placeholder="请重复密码，必填"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">姓氏</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.last_name"
                    autocomplete="off"
                    placeholder="请填写真实姓名，必填"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">名字</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.first_name"
                    autocomplete="off"
                    placeholder="请填写真实姓名，必填"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align:center;margin:5px;">Email</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.email"
                    autocomplete="off"
                    placeholder="请填写真实邮箱"></el-input>
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
        comfirm: "",
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
      if (
        !this.form.last_name ||
        !this.form.first_name
      ) {
        this.$message.error("字段不能为空！");
        return;
      }
      if (this.form.password != this.form.comfirm) {
        this.$message.error("两次密码不一致！");
        return;
      }
      if (this.form.username.length < 3) {
        this.$message.error("用户名太短！");
        return;
      }
      /*if (this.form.name.length < 2) {
        this.$message.error("昵称太短！");
        return;
      }*/
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

      this.form.password = this.$md5(this.form.password);
      // this.$axios
      //   .post("/userdata/", this.form)
      //   .then(response => {
      this.$axios
        .post("/user/signup", this.form)
        .then(response => {
          if (response.data == "usererror") {
            this.$message.error("用户名已存在！");
            return;
          }
          this.$message({
            message: "注册成功！",
            type: "success"
          });
          this.dialogRegisterVisible = false;
          this.form.password = "";
        })
        .catch(error => {
          this.$message.error(
            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
          );
        });
      //})
      // .catch(error => {
      //   if (JSON.stringify(error.response.data).indexOf("user") >= 0)
      //     this.$message.error("用户名已存在！");
      //   else
      //     this.$message.error(
      //       "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
      //     );
      // });
    }
  }
};
</script>

<style  scoped>
.el-row {
  margin-bottom: 20px;
}
</style>
