<template>
  <el-card shadow="always" id="card">

    <!-- 整体结果 -->
    <el-alert title="Status:"
              :type="alerttype(status)"
              :description="status + ', ' + score + '/' + total_score"
              :closable="false"
              show-icon
              :show-close="false"></el-alert>

    <!-- 测试点结果 -->
    <el-collapse>
      <el-collapse-item :key="index" v-for="(result, index) in results">

        <template slot="title">
          <el-alert :title="'test case ' + index + ':' + result.result"
                    :show-icon="true"
                    :type="alerttype(result.result)"
                    :closable="false">
            <!-- <template slot="title">
              <b>{{result.result}}</b>
              {{' '+data.caseresult + ' on test ' + data.casetitle}}</b>
            </template> -->
          </el-alert>
        </template>
        <el-alert :type="alerttype(result.result)"
                  :closable="false">
          <h5 style="white-space:pre;margin-left:15px;">
            {{result.log}}
          </h5>
          <!-- <h5 style="white-space:pre;margin-left:15px;"
              v-if="data.casedata!=''">{{'Time: '+ data.casetime + 'MS'+' Memory: '+data.casememory+'MB'}}</h5>
          <h5 style="white-space:pre;margin-left:15px;"
              v-if="data.casedata!=''">Test Input:</h5>
          <div style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
                v-if="data.casedata!=''">{{data.casedata+'\n'}}</div>

          <h5 style="white-space:pre;margin-left:15px;"
              v-if="data.casedata!=''">Your Output:</h5>
          <div style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
                v-if="data.casedata!=''">{{data.caseuseroutput+'\n'}}</div>

          <h5 style="white-space:pre;margin-left:15px;"
              v-if="data.casedata!=''">Expected Output:</h5>
          <div style="white-space:pre;margin-left:15px;word-wrap:break-word;word-break: normal;"
                v-if="data.casedata!=''">{{data.caseoutputdata+'\n'}}</div> -->
        </el-alert>
      </el-collapse-item>
    </el-collapse>

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
      <el-button v-if="isadmin"
                  type="danger"
                  size="mini"
                  @click="deletestatus(submissionid)">Delete</el-button>
    </el-alert>

    <codemirror id="mycode"
                v-model="code"
                :options="cmOptions"></codemirror>

  </el-card>
</template>


<style scope>
.el-tag {
  text-align: center;
  font-weight: bold;
}
</style>

<script>
import moment from "moment";
import { codemirror } from "vue-codemirror";
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");

require("codemirror/mode/verilog/verilog");
import languageselect from "@/components/utils/languageselect";
export default {
  name: "submission",
  components: {
    codemirror,
    languageselect
  },
  methods: {
    alerttype (status) {
      if(status == 'Accepted')
        return 'success';
      else if(status == 'Pending' || status == 'Judging')
        return 'warning';
      else
        return 'error';
    },
    deletestatus (id) {
      this.$axios
        .delete("/submissions/" + id + "/").then(response => {
          this.$message.success("成功！")
        })
        .catch(error => {
          this.$message.error("失败！" + error)
        });
    },
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
    };
  },
  destroyed () {
  },
  created () {
    this.isadmin = sessionStorage.isadmin;
    this.submissionid = this.$route.params.submissionid;
    this.$axios.get('/submissions/' + this.submissionid + '/').then(response => {
      this.results = response.data.results;
      this.status = response.data.result;
      this.score = response.data.total_grade;
      this.total_score = response.data.problem_belong.total_grade;
    })
  }
};
</script>
