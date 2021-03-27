<template>
  <div>
    <el-link @click="goToUser">{{ userDisplay }}</el-link>
  </div>
</template>

<script>
export default {
  name: "userhyperlink",
  props: {
    userID: {
      type: [Number, String],
      default: "",
    },
    username: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      userDisplay: "",
    };
  },
  methods: {
    goToUser: function (index) {
      this.$router.push({
        name: "user",
        params: { userid: this.userID },
      });
    },
  },
  watch: {
    userID(val) {
      // sentinel for not loaded
      if (val != "") {
        if (this.username == "") {
          // no username given, attempt to fetch
          // WARN: better return from serializer, instead of several single requests

          this.$axios
            .get("/users/" + this.userID + "/")
            .then((response) => {
              this.userDisplay = response.data.username;
            })
            .catch((error) => {
              this.$message.error(
                "在获取 UID=" +
                  this.userID +
                  " 的用户信息时出现错误：" +
                  JSON.stringify(error.response.data)
              );
            });
        }
      }
    },
  },
  created() {},
};
</script>

<style scoped></style>
