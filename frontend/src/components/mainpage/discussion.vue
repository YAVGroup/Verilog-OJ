<template>
  <div>
    <el-row>
      <el-col
        :xs="{ span: 12, push: 0 }"
        :sm="{ span: 7, push: 0 }"
        :md="{ span: 6, push: 0 }"
        :lg="{ span: 5, push: 3 }"
        :xl="{ span: 3, push: 6 }"
        style="cursor: pointer; color: #409eff"
      >
        <b @click="toProblemdetail">{{ problem }}</b>
      </el-col>
      <el-col
        :xs="{ span: 12, pull: 0 }"
        :sm="{ span: 17, pull: 0 }"
        :md="{ span: 18, pull: 0 }"
        :lg="{ span: 19, pull: 3 }"
        :xl="{ span: 21, pull: 6 }"
        style="text-align: right"
      >
        <el-button plain @click="resetStatus" size="mini">刷新</el-button>
      </el-col>
    </el-row>
    <el-row type="flex" justify="center">
      <el-col :xs="24" :sm="24" :md="24" :lg="18" :xl="12">
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
        <el-card shadow="never" style="margin-top: 20px">
          <!--提交界面-->
          <el-row :gutter="15">
            <i style="padding: 5px 10px" class="el-icon-edit"></i>
            <div style="display: inline-block; font-size: 20px">
              发帖 (支持 markdown)
            </div>

            <div v-if="!loggedIn" style="display: inline-block; float: right">
              <el-tooltip
                class="item"
                effect="dark"
                content="登陆以进行提交"
                placement="top"
              >
              </el-tooltip>
            </div>
            <div style="display: inline-block; float: right" v-else>
              <el-button
                type="success"
                size="medium"
                @click="submitTopic"
                style="font-weight: bold; margin-right: 10px; float: right"
                >提交</el-button
              >
              <el-button
                type="danger"
                size="medium"
                @click="code = ''"
                style="font-weight: bold; margin-right: 10px; float: right"
                >清空</el-button
              >
            </div>
          </el-row>

          <!-- 标题编辑 -->
          <el-row>
            <el-col :span="2" type="flex" align="middle">主题：</el-col>
            <el-col :span="22"
              ><el-input
                v-model="topictitle"
                placeholder="请输入标题"
                maxlength="50"
              ></el-input
            ></el-col>
          </el-row>

          <!--内容编辑-->
          <el-row>
            <codemirror v-model="code" :options="cmOptions"></codemirror>
          </el-row>
        </el-card>
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

import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/mode/markdown/markdown");

export default {
  name: "discussion",
  components: {
    codemirror,
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

      if (!this.code) {
        this.$message.error("请输入代码！");
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
            title: this.topictitle,
            description: this.code,
          });
        })
        .then((response) => {
          this.resetStatus();
          this.code = "";
          this.topictitle = "";
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

      topictitle: "",
      cmOptions: {
        tabSize: 4,
        mode: "markdown",
        theme: "base16-light",
        lineNumbers: true,
        viewportMargin: Infinity,
        lineWrapping: true,
      },
      code: "",
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
