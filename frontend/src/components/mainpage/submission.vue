<template>
  <div>
    <el-row>
      &nbsp;
    </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <el-row class="main-title">
          <i class="el-icon-info"></i>
          提交结果
        </el-row>
        <el-row>
          <el-card shadow="never">
            <el-row>
              <el-col :span="12">
                <p class="left-aligned">{{ passed_testcase }} / {{ num_testcase }} 个通过测试用例，获 {{ score }} / {{ total_score }} 分</p>

              </el-col>

              <el-col :span="12">
                <p class="right-aligned">状态：{{ status }}</p>
                <p class="right-aligned">提交时间：{{ submitTimePretty }}</p>
              </el-col>
            </el-row>
          </el-card>
        </el-row>
        <el-row>
          <!-- 测试点结果 -->
          <el-collapse>
            <el-collapse-item :key="index" v-for="(result, index) in results">

              <template slot="title">
                <el-col :span="12">
                  <div style="margin-left: 15px;">测试用例 {{ index }} （{{ prettyType(related_testcases[index].type) }}）： {{ result.result }} </div>
                </el-col>
                <el-col :span=12>
                  <div style="text-align: right;">{{ result.grade }} / {{ related_testcases[index].grade }} 分</div>
                </el-col>
              </template>
              <el-card shadow="never">
                <h3>日志</h3>
                <p style="white-space: pre-wrap; margin-left: 15px; word-wrap: break-word; word-break: normal;">{{result.log}}</p>

                <h3>波形</h3>
                <wavedrom :waveId="String(10 + index)"
                          :parentText="result.app_data"
                          errorMessage="Sorry, no waveform available."></wavedrom>

              </el-card>
            </el-collapse-item>
          </el-collapse>
        </el-row>
      <el-row>
        <!-- 代码显示 -->
        <el-alert title="Code："
                  type="info"
                  :closable="false">
          <el-button size="mini"
                      v-clipboard:copy="code"
                      v-clipboard:success="onCopy"
                      v-clipboard:error="onError">Copy</el-button>
          <el-button size="mini"
                      @click="downloadFile(submissionid,code)">Download</el-button>
        </el-alert>

        <codemirror id="mycode"
                    v-model="code"
                    :options="cmOptions"></codemirror>
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
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}

.left-aligned {
  text-align: left;
}

.right-aligned {
  text-align: right;
}
</style>

<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");

require("codemirror/mode/verilog/verilog");
import languageselect from "@/components/utils/languageselect";
import wavedrom from "@/components/utils/wavedrom";

export default {
  name: "submission",
  components: {
    codemirror,
    languageselect,
    wavedrom
  },
  methods: {
    onCopy (e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError (e) {
      this.$message.error("复制失败：" + e);
    },

    downloadFile (codeid, content) {
      var aLink = document.createElement("a");
      var blob = new Blob([content], { type: "data:text/plain" });
      var downloadElement = document.createElement("a");
      var href = window.URL.createObjectURL(blob); //创建下载的链接
      downloadElement.href = href;
      downloadElement.download = codeid + '.' + this.curlang; //下载后文件名
      document.body.appendChild(downloadElement);
      downloadElement.click(); //点击下载
      document.body.removeChild(downloadElement); //下载完成移除元素
      window.URL.revokeObjectURL(href); //释放掉blob对象
    },
    prettyDate (time) {
      let date = new Date((time || "").replace(/-/g,"/").replace(/[TZ]/g," ")),
        diff = (((new Date()).getTime() - date.getTime()) / 1000),
        day_diff = Math.floor(diff / 86400);

      // return date for anything greater than a day
      if ( isNaN(day_diff) || day_diff < 0 || day_diff > 0 )
        return date.getDate() + " " + date.toDateString().split(" ")[1];

      return day_diff == 0 && (
          diff < 60 && "刚刚" ||
          diff < 120 && "1 分钟前" ||
          diff < 3600 && Math.floor( diff / 60 ) + " 分钟前" ||
          diff < 7200 && "1 小时前" ||
          diff < 86400 && Math.floor( diff / 3600 ) + " 小时前") ||
        day_diff == 1 && "昨天" ||
        day_diff < 7 && day_diff + " 天前" ||
        day_diff < 31 && Math.ceil( day_diff / 7 ) + " 周前";
    },

    updateStatus () {
      this.$axios.get('/submissions/' + this.submissionid + '/').then(response => {
        // console.log(response.data);
        this.results = response.data.results;
        this.status = response.data.result;
        this.score = response.data.total_grade;
        this.total_score = response.data.problem_belong.total_grade;
        this.num_testcase = this.results.length;
        this.submit_time = new Date(response.data.submit_time);

        let passed = 0;
        for (let i = 0; i < this.results.length; i++) {
          // console.log(this.results[i]);
          if (this.results[i].result == "Accepted") {
            passed++;
          }
        }
        this.passed_testcase = passed;

        // TODO: support for multiple files
        return this.$axios.get('/files/' + response.data.submit_files[0] + '/');
      }).then(response => {
        // console.log(response.data);
        this.code = response.data;
      })
    },
    prettyType (type) {
      if (type == 'SIM') {
        return "行为级仿真";
      } else if (type == 'SYNTHSIM') {
        return "门级仿真";
      } else {
        return type;
      }
    }
  },
  data () {
    return {
      cmOptions: {
        tabSize: 4,
        mode: "verilog",
        theme: "base16-light",
        lineNumbers: true,
        readOnly: true,
        viewportMargin: Infinity,
        lineWrapping: true
      },
      isadmin: false,
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
    }
  },
  computed: {
    submitTimePretty : function () {
      let tm = this.submit_time;
      return this.prettyDate(tm.toISOString());
    }
  },
  destroyed () {
  },
  created () {
    this.isadmin = sessionStorage.isadmin;
    this.submissionid = this.$route.params.submissionid;
    this.updateStatus();
    this.timer = setInterval(this.updateStatus, 500);
  },
  beforeDestroy () {
    clearInterval(this.timer);
  }
};
</script>
