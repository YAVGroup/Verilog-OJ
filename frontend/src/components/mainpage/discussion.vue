<template>
  <div>
    <el-row type="flex" justify="center">
      <el-col :xs="24" :sm="24" :md="24" :lg="18" :xl="12">
        <el-row style="margin-top: 15px">
          <b @click="toProblemdetail" style="cursor: pointer; color: #409eff">{{
            problem
          }}</b>
          <el-button plain @click="resetStatus" style="float: right" size="mini"
            >刷新</el-button
          ></el-row
        >

        <el-table
          :default-sort="{ prop: 'updatetime', order: 'descending' }"
          :data="tableData"
          @row-click="rowClick"
          v-loading="loading"
        >
          <el-table-column
            prop="user_belong.username"
            label="用户"
            :min-width="120"
          ></el-table-column>

          <el-table-column prop="title" label="主题" :min-width="150">
          </el-table-column>

          <el-table-column prop="comments.length" label="回复" :min-width="60">
          </el-table-column>

          <el-table-column
            prop="updatetime"
            label="最后活跃时间"
            :min-width="120"
          ></el-table-column>
        </el-table>

        <!-- 发布帖子 -->
        <submitcard
          style="margin-top: 20px"
          title="发帖 (支持 markdown)"
          :loggedIn="loggedIn"
          @submit="submitTopic"
          @clear="(topicDescription = ''), (topicTitle = '')"
        >
          <!-- 标题编辑 -->
          <el-row>
            <el-col :span="2" type="flex" align="middle">主题：</el-col>
            <el-col :span="22"
              ><el-input
                v-model="topicTitle"
                placeholder="请输入标题"
                maxlength="50"
                show-word-limit
              ></el-input
            ></el-col>
          </el-row>
          <!-- 帖子内容编辑 -->
          <markdowneditor v-model="topicDescription"></markdowneditor
        ></submitcard>
      </el-col>
    </el-row>

    <el-row> &nbsp; </el-row>
    <el-row>
      <el-col>
        <center>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentpage"
            :page-sizes="[10, 20, 30, 50]"
            :page-size="pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalstatus"
          ></el-pagination>
        </center>
      </el-col>
    </el-row>
  </div>
</template>

<style scope>
.el-tag {
  text-align: center;
  font-weight: bold;
}
</style>

<script>
import moment from "moment";
import { mapState } from "vuex";

import markdowneditor from "@/components/utils/markdowneditor";
import submitcard from "@/components/utils/submitcard";

export default {
  name: "discussion",
  components: {
    markdowneditor,
    submitcard,
  },
  methods: {
    toProblemdetail() {
      this.$router.push({
        name: "problemdetail",
        params: { problemid: this.problemid },
      });
    },

    rowClick(row, col, e) {
      if (col.label == "用户") {
        this.$router.push({
          name: "user",
          params: { userid: row.user_belong.id },
        });
        return;
      }
      this.$router.push({
        name: "topic",
        params: { topicid: row.id },
      });
    },

    resetStatus() {
      this.currentpage = 1;
      this.getstatusdata();
    },

    handleSizeChange(val) {
      this.pagesize = val;
      this.getstatusdata();
    },

    handleCurrentChange(val) {
      this.currentpage = val;
      this.getstatusdata();
    },

    getstatusdata() {
      this.loading = true;

      this.$axios.get("/problems/" + this.problemid).then((response) => {
        this.problem = response.data.name;
      });

      let url =
        "/topic/?problem=" +
        this.problemid +
        "&limit=" +
        this.pagesize +
        "&offset=" +
        (this.currentpage - 1) * this.pagesize;

      this.$axios.get(url).then((response) => {
        for (let i = 0; i < response.data.results.length; i++) {
          let update_time = moment(response.data.results[i].update_time).format(
            "YYYY-MM-DD HH:mm:ss"
          );
          for (const comment of response.data.results[i].comments) {
            const comment_update_time = moment(comment.update_time).format(
              "YYYY-MM-DD HH:mm:ss"
            );
            if (moment(update_time).isBefore(comment_update_time)) {
              update_time = comment_update_time;
            }
          }
          response.data.results[i].updatetime = update_time;
        }

        this.tableData = response.data.results;
        this.totalstatus = response.data.count;
        this.loading = false;
      });
    },

    submitTopic: function () {
      if (!this.loggedIn) {
        this.$message.error("请先登录！");
        return;
      }

      if (!this.topicTitle) {
        this.$message.error("请输入主题！");
        return;
      }

      if (!this.topicDescription) {
        this.$message.error("请输入正文！");
        return;
      }

      this.$confirm("确定提交吗？", "提交", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$message({
            type: "success",
            message: "提交中...",
          });

          return this.$axios.post("/addtopic", {
            problem: this.problemid,
            title: this.topicTitle,
            description: this.topicDescription,
          });
        })
        .then((response) => {
          this.resetStatus();
          this.topicDescription = "";
          this.topicTitle = "";
          this.$router.push({
            name: "topic",
            params: { topicid: response.data.id },
          });
        })
        .catch((error) => {
          this.$message.error(
            "提交失败：" + JSON.stringify(error.response.data)
          );
        });
    },
  },

  data() {
    return {
      problem: "",
      problemid: "",
      tableData: [],
      currentpage: 1,
      pagesize: 30,
      totalstatus: 10,
      loading: false,

      topicTitle: "",
      topicDescription: "",
    };
  },
  computed: {
    ...mapState(["loggedIn", "userID", "username", "isSuperUser"]),
  },
  created() {
    this.problemid = this.$route.params.problemid;
    this.getstatusdata();
  },
};
</script>
