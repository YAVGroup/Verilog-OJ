<template>
  <div>
    <el-row> &nbsp; </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <el-row class="main-title">
          <el-col>
            <i class="el-icon-info"></i>
            提交结果
          </el-col>
          <el-button type="primary" plain @click="tryAgain"
            ><i class="el-icon-d-arrow-right"></i> 继续尝试</el-button
          >
        </el-row>
        <el-row>
          <el-card shadow="never">
            <el-row>
              <el-col :span="12">
                <p class="left-aligned">
                  {{ passed_testcase }} / {{ num_testcase }} 个通过测试用例，获
                  {{ score }} / {{ total_score }} 分
                </p>
              </el-col>

              <el-col :span="12">
                <p class="right-aligned">状态：{{ status }}</p>
                <p class="right-aligned">提交时间：{{ submitTimePretty }}</p>
              </el-col>
            </el-row>
          </el-card>
        </el-row>
        <el-row v-if="!loggedIn">
          <el-alert
            type="info"
            show-icon
            title="登录以查看波形和测试结果！"
          ></el-alert>
        </el-row>
        <el-row v-else-if="!hasPermission">
          <el-alert
            type="warning"
            show-icon
            title="您只能查看自己的波形和测试结果！"
          ></el-alert>
        </el-row>
        <el-row v-else>
          <!-- 测试点结果 -->
          <el-collapse>
            <el-collapse-item :key="index" v-for="(result, index) in results">
              <template slot="title">
                <el-col :span="12">
                  <div style="margin-left: 15px">
                    测试用例 {{ index }} （{{
                      prettyType(related_testcases[index].type)
                    }}）： {{ result.result }}
                  </div>
                </el-col>
                <el-col :span="12">
                  <div style="text-align: right">
                    {{ result.grade }} / {{ related_testcases[index].grade }} 分
                  </div>
                </el-col>
              </template>
              <el-card shadow="never">
                <h3>日志</h3>
                <p
                  style="
                    white-space: pre-wrap;
                    margin-left: 15px;
                    word-wrap: break-word;
                    word-break: normal;
                  "
                >{{ result.log }}</p>

                <h3>波形</h3>
                <wavedrom
                  :waveId="String(10 + index)"
                  :parentText="result.app_data"
                  errorMessage="Sorry, no waveform available."
                ></wavedrom>
              </el-card>
            </el-collapse-item>
          </el-collapse>
        </el-row>
        <el-row v-if="!loggedIn">
          <el-alert type="info" show-icon title="登录以查看代码！"></el-alert>
        </el-row>
        <el-row v-else-if="!hasPermission">
          <el-alert
            type="warning"
            show-icon
            title="您只能查看和下载自己的代码！"
          ></el-alert>
        </el-row>
        <el-row v-else>
          <!-- 代码显示 -->
          <el-alert type="info" :closable="false">
            <el-button plain>
              <i class="el-icon-refresh-left"></i>
              <div>撤销</div>
            </el-button>
            <el-button plain>
              <i class="el-icon-refresh-right"></i>
              <div>重做</div>
            </el-button>
            <el-divider direction="vertical"></el-divider>
            <el-button plain>
              <i class="el-icon-scissors"></i>
              <div>剪切</div>
            </el-button>
            <el-button
              plain
              v-clipboard:copy="code"
              v-clipboard:success="onCopy"
              v-clipboard:error="onError"
              ><i class="el-icon-document-copy"></i>
              <div>复制</div>
            </el-button>
            <el-button plain>
              <i class="el-icon-data-board"></i>
              <div>粘贴</div>
            </el-button>
            <el-divider direction="vertical"></el-divider>
            <el-button plain>
              <i class="el-icon-document"></i>
              <div>全选</div>
            </el-button>
            <el-divider direction="vertical"></el-divider>
            <el-button plain @click="downloadFile(submissionid, code)"
              ><i class="el-icon-download"></i>
              <div>下载</div>
            </el-button
            >
          </el-alert>

          <codemirror
            id="mycode"
            v-model="code"
            :options="cmOptions"
          ></codemirror>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<style scope>
.el-tag {
  text-align: center;
  font-weight: bold;
}

.main-title {
  font-size: 20px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  display: flex;
  align-items: center;
}

.main-title .el-button {
  font-size: 16px;
}

.left-aligned {
  text-align: left;
}

.right-aligned {
  text-align: right;
}

.el-alert .el-button {
  padding: 6px 12px;
}

.el-alert .el-button i {
  font-size: 22px;
}

.el-alert .el-button div {
  font-size: 12px;
  margin-top: 4px;
}

.el-alert {
  padding: 6px;
}

.el-alert .el-divider {
  height: 32px;
  vertical-align: baseline;
}
</style>

<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");

require("codemirror/mode/verilog/verilog");
//import languageselect from "@/components/utils/languageselect";
import wavedrom from "@/components/utils/wavedrom";
import { mapState } from "vuex";

export default {
  name: "submission",
  components: {
    codemirror,
    //languageselect,
    wavedrom,
  },
  methods: {
    onCopy(e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError(e) {
      this.$message.error("复制失败：" + e);
    },

    downloadFile(codeid, content) {
      var aLink = document.createElement("a");
      var blob = new Blob([content], { type: "data:text/plain" });
      var downloadElement = document.createElement("a");
      var href = window.URL.createObjectURL(blob); //创建下载的链接
      downloadElement.href = href;
      downloadElement.download = codeid + "." + this.curlang; //下载后文件名
      document.body.appendChild(downloadElement);
      downloadElement.click(); //点击下载
      document.body.removeChild(downloadElement); //下载完成移除元素
      window.URL.revokeObjectURL(href); //释放掉blob对象
    },

    updateStatus() {
      this.$axios
        .get("/submissions/" + this.submissionid + "/")
        .then((response) => {
          // console.log(response.data);
          this.results = response.data.results;
          this.status = response.data.result;
          this.score = response.data.total_grade;
          this.total_score = response.data.problem_belong.total_grade;
          this.num_testcase = this.results.length;
          this.related_testcases = response.data.problem_belong.testcases;
          this.submit_time = new Date(response.data.submit_time);
          console.log(this.submit_time.toISOString());
          this.subm_userid = response.data.user;
          this.problem_id = response.data.problem_belong.id;

          let passed = 0;
          for (let i = 0; i < this.results.length; i++) {
            // console.log(this.results[i]);
            if (this.results[i].result == "Accepted") {
              passed++;
            }
          }
          this.passed_testcase = passed;

          if (this.loggedIn && this.hasPermission) {
            // TODO: support for multiple files
            this.$axios
              .get("/files/" + response.data.submit_files[0] + "/")
              .then((response) => {
                // console.log(response.data);
                this.code = response.data;
              })
              .catch();
          }
        })
        .catch()
        .then(() => {
          if (!this.needRefresh && this.autoRefresh) {
            this.autoRefresh = false;
            clearInterval(this.timer);
          }
          if (this.needRefresh && !this.autoRefresh) {
            this.autoRefresh = true;
            this.timer = setInterval(this.updateStatus, 2000);
          }
        });
    },
    prettyType(type) {
      if (type == "SIM") {
        return "行为级仿真";
      } else if (type == "SYNTHSIM") {
        return "门级仿真";
      } else {
        return type;
      }
    },
    tryAgain() {
      this.$router.push({
        name: "problemdetail",
        params: { problemid: this.problem_id },
      });
    },
  },
  data() {
    return {
      cmOptions: {
        tabSize: 4,
        mode: "verilog",
        theme: "base16-light",
        lineNumbers: true,
        readOnly: true,
        viewportMargin: Infinity,
        lineWrapping: true,
      },
      code: "",

      submissionid: null,
      status: "",
      results: [],
      score: 0,
      total_score: 0,
      num_testcase: 0,
      passed_testcase: 0,
      submit_time: new Date(),
      related_testcases: [],
      subm_userid: "",
      problem_id: 0,

      autoRefresh: false,
    };
  },
  computed: {
    submitTimePretty: function () {
      let tm = this.submit_time;
      let duration = moment(tm).locale("zh-CN").fromNow();
      return duration;
    },
    ...mapState(["loggedIn", "userID", "username", "isSuperUser"]),
    needRefresh: function () {
      return this.results[0].status != "DONE";
    },
    hasPermission: function () {
      return this.subm_userid == this.userID || this.isSuperUser;
    },
  },
  destroyed() {},
  created() {
    // console.log(this.needRefresh);
    this.submissionid = this.$route.params.submissionid;
    this.updateStatus();
  },
  beforeDestroy() {
    if (this.autoRefresh) {
      clearInterval(this.timer);
    }
  },
};
</script>
