<template>
  <div>
    <el-row :gutter="15">
      <el-col :xs="0" :sm="1" :md="2" :lg="2" :xl="4" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="22" :md="20" :lg="20" :xl="16">
        <el-col :span="16">
          <el-row>
            <el-card shadow="never">
              <!--标题、DDL-->
              <!-- <el-row :gutter="18"> -->
              <div id="title">
                <div
                  style="
                    display: inline-block;
                    margin-top: 6px;
                    margin-left: 10px;
                  "
                >
                  {{ title }}
                </div>
                <div style="float: right; margin-right: 5px">
                  <el-button-group>
                    <el-button
                      plain
                      circle
                      size="medium"
                      icon="el-icon-edit"
                      @click="problemEdit"
                      :disabled="
                        !(loggedIn && (userID == owner || isSuperUser))
                      "
                    ></el-button>
                    <el-button
                      plain
                      circle
                      size="medium"
                      icon="el-icon-delete"
                      @click="problemDelete"
                      :disabled="
                        !(loggedIn && (userID == owner || isSuperUser))
                      "
                    ></el-button>
                  </el-button-group>
                </div>
              </div>
              <el-divider></el-divider>
              <el-row :gutter="18" id="ddl" v-show="have_ddl">截止时间</el-row>
              <el-row
                :gutter="18"
                class="problem-descriptions"
                v-show="have_ddl"
              >
                {{ ddl }}
              </el-row>

              <!--题目描述、输入、输出-->
              <el-row :gutter="18" class="problem-description-title"
                >题目描述</el-row
              >
              <el-row :gutter="18" class="problem-descriptions">
                <div class="problem-descriptions">
                  <markdownIt :mdSource="des"></markdownIt>
                </div>
              </el-row>

              <el-row :gutter="18" class="problem-description-title"
                >输入格式</el-row
              >
              <el-row :gutter="18" class="problem-descriptions">
                <div class="problem-descriptions">{{ input }}</div>
              </el-row>
              <el-row :gutter="18" class="problem-description-title"
                >输出格式</el-row
              >
              <el-row :gutter="18" class="problem-descriptions">
                <div class="problem-descriptions">{{ output }}</div>
              </el-row>

              <!--这里放样例波形图-->
              <el-row :gutter="18" class="problem-description-title"
                >示例波形</el-row
              >
              <el-row
                :gutter="18"
                id="sample_waveform"
                class="problem-descriptions"
              >
                <wavedrom
                  waveId="1"
                  :parentText="waveform"
                  errorMessage="Sorry, no sample waveform available"
                ></wavedrom>
              </el-row>
            </el-card>
          </el-row>

          <el-row>
            <!--提交界面-->
            <submitcard
              title="代码编辑"
              :loggedIn="loggedIn"
              @submit="submit"
              @clear="code = template_code"
            >
              <el-row>
                <el-col class="filelist" :span="6">
                  <div>文件列表</div>
                  <div>
                    <el-button plain type="primary">
                      <i class="el-icon-document-add"></i>
                      <div>新建</div>
                    </el-button>
                    <el-button plain type="primary">
                      <i class="el-icon-document-copy"></i>
                      <div>复制</div>
                    </el-button>
                    <el-button plain type="primary">
                      <i class="el-icon-document-remove"></i>
                      <div>重命名</div>
                    </el-button>
                    <el-button plain type="danger">
                      <i class="el-icon-document-delete"></i>
                      <div>删除</div>
                    </el-button>
                  </div>
                  <div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div class="active">code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                    <div>code.v</div>
                    <div>code2.v</div>
                  </div>
                </el-col>
                <el-col :span="18" class="editor">
                  <div>code.v</div>
                  <codemirror v-model="code" :options="cmOptions"></codemirror>
                </el-col>
              </el-row>
            </submitcard>
          </el-row>
        </el-col>
        <!--侧栏-->
        <el-col :span="8">
          <!--question info-->
          <el-row>
            <el-card shadow="never">
              <el-row>
                <el-col :span="10">创建时间</el-col>
                <el-col :span="14">{{ addtime }}</el-col>
              </el-row>
              <el-row>
                <el-col :span="10">创建者</el-col>
                <el-col :span="14">
                  <userhyperlink :userID="owner"></userhyperlink>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="10">题目难度</el-col>
                <el-col :span="14">{{ level }}</el-col>
              </el-row>
              <el-row>
                <el-col :span="10">题目标签</el-col>
                <el-col :span="14">
                  <taglist :tags="tags" />
                </el-col>
              </el-row>
            </el-card>
          </el-row>
          <!--提交记录-->
          <el-row>
            <el-card shadow="never">
              <div
                style="
                  box-sizing: border-box;
                  padding-bottom: 8px;
                  display: inline-block;
                "
              >
                提交记录
              </div>
              <el-button
                size="mini"
                @click="submissionsRefresh"
                style="float: right"
                :disabled="!loggedIn"
                >刷新</el-button
              >
              <el-table
                :default-sort="{ prop: 'id', order: 'descending' }"
                :data="submissions"
                style="width: 100%"
                :row-class-name="tableRowClassName"
                @row-click="submissionClick"
                v-loading="!loggedIn"
                element-loading-text="登陆以查看本题提交记录"
                element-loading-spinner="el-icon-info"
                size="mini"
              >
                <el-table-column
                  prop="id"
                  label="ID"
                  :width="60"
                ></el-table-column>
                <el-table-column
                  prop="pretty_time"
                  label="日期"
                  :width="90"
                ></el-table-column>

                <el-table-column prop="result" label="状态">
                  <!-- <template slot-scope="scope">
                    <el-tag size="mini" :type="statuetype(scope.row.result)" disable-transitions hit>
                      {{ scope.row.result }}
                      <i class="el-icon-loading" v-show="statuejudge(scope.row.result)"></i>
                    </el-tag>
                  </template> -->
                </el-table-column>
              </el-table>
            </el-card>
          </el-row>
          <!--评论区-->
          <el-row>
            <el-card shadow="never">
              <div
                style="
                  box-sizing: border-box;
                  padding-bottom: 8px;
                  display: inline-block;
                "
              >
                讨论区
              </div>
              <el-button
                size="mini"
                @click="problemDiscuss"
                style="float: right; margin: 0 5px 5px 0"
                type="text"
                :disabled="!loggedIn"
                >进入讨论版</el-button
              >
              <!-- 主题表格 -->
              <el-table
                v-if="topics_display"
                :default-sort="{ prop: 'updatetime', order: 'descending' }"
                :data="topics"
                style="width: 100%"
                :row-class-name="tableRowClassName"
                @row-click="commentClick"
                v-loading="!loggedIn"
                element-loading-text="登陆以查看本题评论"
                element-loading-spinner="el-icon-info"
                size="mini"
              >
                <el-table-column
                  prop="user_belong.username"
                  label="用户"
                  :width="80"
                ></el-table-column>
                <el-table-column prop="title" label="主题"></el-table-column>
                <el-table-column
                  prop="updatetime"
                  label="活跃时间"
                  :width="100"
                  :formatter="time_formatter"
                ></el-table-column>
              </el-table>
              <!-- 默认讨论区隐藏提示 -->
              <el-row type="flex" justify="center" style="margin-bottom: 0">
                <el-button
                  v-if="topics_display"
                  type="text"
                  style="color: #909399"
                  @click="topics_display = false"
                  ><i class="el-icon-arrow-up"></i> 隐藏讨论</el-button
                ><el-button
                  v-else
                  type="text"
                  style="color: #909399"
                  @click="
                    topics_display = true;
                    topicsRefresh();
                  "
                  ><i class="el-icon-arrow-down"></i> 显示讨论</el-button
                ></el-row
              >
            </el-card>
          </el-row>
        </el-col>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
// import statusmini from "@/components/utils/statusmini";
// import prostatistice from "@/components/utils/prostatistice";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/theme/base16-dark.css");

require("codemirror/mode/verilog/verilog");

import submitcard from "@/components/utils/submitcard";
import wavedrom from "@/components/utils/wavedrom";
import markdownIt from "@/components/utils/markdownIt";
import userhyperlink from "@/components/utils/userhyperlink";
import taglist from "@/components/utils/taglist";

import { mapState } from "vuex";
import { prettyDate } from "@/utils/timeUtil";

export default {
  name: "problemdetail",
  components: {
    submitcard,
    codemirror,
    // statusmini,
    // prostatistice,
    wavedrom,
    userhyperlink,
    taglist,
    markdownIt,
  },
  data() {
    return {
      cmOptions: {
        tabSize: 4,
        indentUnit: 4,
        mode: "verilog",
        theme: "base16-light",
        lineNumbers: true,
      },
      title: "",
      des: "",
      input: "",
      output: "",
      owner: "",
      addtime: "",
      ddl: "",
      have_ddl: false,
      tags: "",
      level: "",
      ddl_time: "",
      id: null,

      code: "",
      template_code: "",
      submissions: [],
      topics: [],
      topics_display: false,

      waveform: "",
    };
  },
  watch: {
    code: function (code) {
      localStorage.setItem("code" + this.id, code);
    },
  },
  created() {
    this.id = this.$route.params.problemid;
    if (!this.id) {
      this.$message.error("参数错误" + "(" + this.id + ")");
      return;
    }
    this.$axios
      .get("/problems/" + this.id + "/")
      .then((response) => {
        this.des = response.data.description;
        this.input = response.data.description_input;
        this.output = response.data.description_output;
        this.waveform = response.data.app_data;
        this.owner = response.data.owner;
        this.addtime = response.data.create_time = moment(
          response.data.create_time
        ).format("YYYY-MM-DD HH:mm:ss");

        if (response.data.template_code_files != null) {
          this.$axios
            .get("/files/" + response.data.template_code_files[0] + "/")
            .then((response) => {
              this.template_code = response.data;
            //   this.$message(this.template_code);
              const local_code = localStorage.getItem("code" + this.id);
              if (local_code != null) {
                this.code = local_code;
              } else {
                this.code = this.template_code;
              }
            });
        }

        this.tags = response.data["tags"];

        if (response.data.deadline_time == null) {
          this.ddl = "";
          this.have_ddl = false;
        } else {
          this.ddl_time = response.data.deadline_time;
          let ddlTime = moment(response.data.deadline_time);
          this.ddl =
            ddlTime.format("YYYY-MM-DD hh:mm:ss") +
            " (" +
            ddlTime.endOf("day").fromNow() +
            ")";
          this.have_ddl = true;
        }

        this.title = response.data.name;
        this.level = response.data.level;

        if (this.loggedIn) {
          this.submissionsRefresh();
        }
      })
      .catch((error) => {
        this.$message.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {
    onCopy(e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError(e) {
      this.$message.error("复制失败：" + e);
    },

    problemlevel: function (type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "danger";
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.result == "Pending") return "info-row";
      if (row.result == "Judging") return "judging-row";
      if (row.result == "Wrong Answer") return "danger-row";
      if (row.result == "Compile Error") return "warning-row";
      if (row.result == "Presentation Error") return "warning-row";
      if (row.result == "Waiting") return "info-row";
      if (row.result == "Accepted") return "success-row";
      if (row.result == "Time Limit Exceeded") return "warning-row";
      if (row.result == "Time Limit Exceeded") return "warning-row";
      if (row.result == "Memory Limit Exceeded") return "warning-row";
      if (row.result == "Runtime Error") return "warning-row";
      if (row.result == "System Error") return "warning-row";
      return "";
    },
    statuetype: function (type) {
      if (type == "Pending") return "info";
      if (type == "Judging") return "";
      if (type == "Wrong Answer") return "danger";
      if (type == "Compile Error") return "warning";
      if (type == "Presentation Error") return "warning";
      if (type == "Waiting") return "info";
      if (type == "Accepted") return "success";
      if (type == "Time Limit Exceeded") return "warning";
      if (type == "Memory Limit Exceeded") return "warning";
      if (type == "Runtime Error") return "warning";
      if (type == "System Error") return "danger";
      return "danger";
    },
    statuejudge: function (type) {
      if (type == "Pending") return true;
      if (type == "Judging") return true;
      return false;
    },

    submissionClick(row, col, e) {
      this.$router.push({
        name: "submission",
        params: { submissionid: row.id },
      });
    },

    commentClick(row, col, e) {
      this.$router.push({
        name: "topic",
        params: { topicid: row.id },
      });
    },

    submissionsRefresh() {
      if (!this.loggedIn) {
        this.$message.error("请登陆后查看自己的提交！");
        return;
      }
      this.$axios
        .get("/submissions/?user=" + this.userID + "&problem=" + this.id)
        .then((response) => {
          for (var i = 0; i < response.data.length; i++) {
            response.data[i]["pretty_time"] = prettyDate(
              response.data[i]["submit_time"]
            );
          }
          this.submissions = response.data;
        });
    },

    topicsRefresh() {
      if (!this.loggedIn) {
        this.$message.error("请登陆后查看评论！");
        return;
      }
      this.$axios.get("/topic/?problem=" + this.id).then((response) => {
        for (let i = 0; i < response.data.length; i++) {
          let update_time = moment(response.data[i].update_time).format(
            "YYYY-MM-DD HH:mm:ss"
          );
          for (const comment of response.data[i].comments) {
            const comment_update_time = moment(comment.update_time).format(
              "YYYY-MM-DD HH:mm:ss"
            );

            if (moment(update_time).isBefore(comment_update_time)) {
              update_time = comment_update_time;
            }
          }
          response.data[i].updatetime = update_time;
        }
        this.topics = response.data;
      });
    },

    time_formatter: (row) => prettyDate(row.updatetime),

    problemEdit: function () {
      this.$router.push({
        name: "problemedit",
        params: { problemid: this.id },
      });
    },
    problemDelete: function () {
      if (!this.loggedIn) {
        this.$message.error("请先登录！");
        return;
      }

      if (this.userID != this.owner) {
        this.$message.error("不是题目创建者，没有对应权限");
        return;
      }

      this.$confirm("此操作将永久删除该题目, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$axios
            .delete("/problems/" + this.id + "/")
            .then((response) => {
              this.$message({
                type: "success",
                message: "删除成功!",
              });
              this.$router.push({
                name: "problem",
              });
            })
            .catch((error) => {
              this.$message.error(
                "删除失败：" + JSON.stringify(error.response.data)
              );
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },

    problemDiscuss: function () {
      this.$router.push({
        name: "discussion",
        params: { problemid: this.id },
      });
    },

    submit: function () {
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

          var formData = new FormData();
          var blob = new Blob([this.code], { type: "text/plain" });
          formData.append("file", blob, "code.v");
          return this.$axios.post("/files/", formData);
        })
        .then((response) => {
          const fileid = response.data.id;
          return this.$axios.post("/submit", {
            problem: this.id,
            submit_files: [fileid],
          });
        })
        .then((response) => {
          this.$router.push({
            name: "submission",
            params: { submissionid: response.data.id },
          });
        })
        .catch((error) => {
          this.$message.error(
            "提交失败：" + JSON.stringify(error.response.data)
          );
        });
    },
  },
  computed: {
    ...mapState(["loggedIn", "userID", "username", "isSuperUser"]),
  },
  destroyed() {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#tag {
  text-align: center;
  font-weight: bold;
  margin-right: 13px;
  margin-bottom: 13px;
}
#title {
  color: dimgrey;
  left: 15px;
  font-size: 20px;
  vertical-align: middle;
}
#ddl {
  color: tomato;
  font-weight: bold;
  left: 20px;
  font-size: 20px;
}
#text {
  font-weight: normal;
  font-size: 15px;
  white-space: pre-wrap;
  margin-right: 40px;
}
#data {
  left: 30px;
  padding: 5px 10px;
  color: dimgray;
  background: #f8f8f9;
  border: 1px dashed #e9eaec;
}

.problem-description-title {
  color: deepskyblue;
  font-weight: bold;
  left: 20px;
  font-size: 20px;
}
.problem-descriptions {
  left: 30px;
  font-size: 16px;
  margin-right: 50px;
  /* word-break: break-all; */
  white-space: pre-line;
}
.problem-descriptions >>> * {
  margin-top: 0;
  margin-bottom: 0;
}
.el-row {
  margin-bottom: 20px;
}
.img-responsive {
  display: inline-block;
  height: auto;
  max-width: 75%;
}

.el-card__body > .el-row:nth-child(2) {
  margin: 0;
}

.filelist {
  height: 500px;
  display: flex;
  flex-direction: column;
  border: 1px solid #cbced5;
  box-sizing: border-box;
  border-right: none;
}

.filelist > div:first-child {
  height: 36px;
  box-sizing: border-box;
  text-align: center;
  padding: 6px 0;
  border-bottom: 1px solid #cbced5;
}

.filelist > div:nth-child(2) {
  display: flex;
  justify-content: space-between;
  gap: 4px;
  padding: 4px;
  border-bottom: 1px solid #cbced5;
}

.filelist > div:nth-child(2) > button {
  padding: 4px;
  margin: 0;
  flex-grow: 1;
}

.filelist > div:nth-child(2) > button div {
  margin-top: 4px;
  font-size: 11px;
}

.filelist > div:nth-child(3) {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 4px 10px;
  overflow-y: scroll;
}

.filelist > div:nth-child(3) > div {
  padding: 6px 8px;
  border-radius: 6px;
  border: 2px solid white;
  user-select: none;
}

.filelist > div:nth-child(3) > div:hover {
  background-color: #d9ecff;
}

.filelist > div:nth-child(3) > .active {
  border: 2px solid #8cc5ff;
}

.editor > div:first-child {
  height: 36px;
  line-height: 24px;
  text-align: center;
  padding: 6px 0;
  border: 1px solid #cbced5;
  border-bottom: none;
  box-sizing: border-box;
}
</style>

<style>
.CodeMirror {
  height: 464px;
  border: 1px solid #cbced5;
  box-sizing: border-box;
}
</style>
