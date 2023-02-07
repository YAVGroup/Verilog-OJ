<template>
  <el-card shadow="always" id="card">
    <el-form :model="form">
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">昵称</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.username" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">介绍</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.des" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">
            新密码（不更改，请输入上次密码）
          </div>
        </el-col>
        <el-col :span="12">
          <el-input
            type="password"
            v-model="form.password"
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
            v-model="form.confirm"
            autocomplete="off"
          ></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">学校</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.school" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">专业</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.course" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">班级</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.classes" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">学号</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.number" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">真实姓名</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.realname" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">QQ</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.qq" autocomplete="off"></el-input>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="3">
          <div style="text-align: center; margin: 5px">Email</div>
        </el-col>
        <el-col :span="12">
          <el-input v-model="form.email" autocomplete="off"></el-input>
        </el-col>
      </el-row>
    </el-form>

    <el-button type="primary" @click="updateClick">更新</el-button>
  </el-card>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "setting",
  data() {
    return {
      form: {
        password: "",
        confirm: "",
        username: "",
        des: "",
        school: "",
        course: "",
        classes: "",
        number: "",
        realname: "",
        qq: "",
        email: "",
      },
    };
  },
  methods: {
    updateClick() {
      if (!this.userID) {
        this.$message.error("非法访问！");
        return;
      }
      if (
        !this.form.username ||
        !this.form.school ||
        !this.form.course ||
        !this.form.classes ||
        !this.form.number ||
        !this.form.realname ||
        !this.form.qq ||
        !this.form.email
      ) {
        this.$message.error("字段不能为空！");
        return;
      }
      if (this.form.password != this.form.confirm) {
        this.$message.error("两次密码不一致！");
        return;
      }

      if (this.form.username.length < 2) {
        this.$message.error("昵称太短！");
        return;
      }

      if (!this.form.password) {
        this.$message.error("请输入密码");
        return;
      }

      if (this.form.password.length < 6) {
        this.$message.error("密码太短！");
        return;
      }

      if (this.form.des.length <= 0) {
        this.form.des = "这个人很懒，什么都没有没有留下。";
      }

      this.$confirm(
        "确定更新吗?",
        "如果你在参与一场比赛，请勿更新你的【昵称】，会影响排行榜计算，后果自负！",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      ).then(() => {
        // TODO: fix this
        //this.form.password = this.form.password;
        this.$axios.put(`/users/${this.userID}/`, this.form).then(
          (response) => {
            this.$message({
              message: "更新成功！",
              type: "success",
            });
            this.$parent.showHome();
          },
          (response) => {
            this.$message.error("更新失败（" + response + "）");
          }
        );
      });
    },
    async updateUserInfo() {
      if (this.userID) {
        const resp_data = (await this.$axios.get(`/users/${this.userID}`)).data;
        this.form.username = resp_data.username;
        this.form.des = resp_data.des || "这个人很懒，什么都没有没有留下。";
        this.form.school = resp_data.school;
        this.form.course = resp_data.course;
        this.form.classes = resp_data.classes;
        this.form.number = resp_data.number;
        this.form.realname = resp_data.realname;
        this.form.qq = resp_data.qq;
        this.form.email = resp_data.email;
      }
    },
  },
  computed: {
    ...mapState(["loggedIn", "userID", "username", "isSuperUser"]),
  },
  watch: {
    userID: function () {
      this.updateUserInfo();
    },
  },
  created: async function () {
    await this.updateUserInfo();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#card {
  margin: 200px;
  padding: 200px;
}
.el-table .warning-row {
  background: #fff9f9;
}

.el-table .success-row {
  background: #e6ffdf;
}

.el-table .info-row {
  background: #fffff7;
}

.el-table .judging-row {
  background: #f7ffff;
}

.el-table .danger-row {
  background: #fff9f9;
}

.el-tag {
  text-align: center;
  font-weight: bold;
}
</style>
