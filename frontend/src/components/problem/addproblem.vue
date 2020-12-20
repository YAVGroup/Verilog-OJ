<template>
  <el-row :gutter="15">
    <el-col :span="18">
      <el-row>
        <el-card shadow="always">
          <!--标题、DDL-->
          <el-row :gutter="18" id="ddl" >Title</el-row>
          <el-row :gutter="18" id="title">
            <el-col :span="20">
              <el-input v-model="title"></el-input>
              
            </el-col>
            <el-col :span="2">
              <el-button type="success"
                         @click="problemedit"
                         style="font-weight:bold;margin-left:10px;">Submit</el-button>
            </el-col>
          </el-row>
          <el-row :gutter="18" id="ddl" >Deadline</el-row>
          <el-row :gutter="18" class="problem-descriptions" >
              <el-radio v-model="have_ddl" label=true>have ddl</el-radio>
              <el-radio v-model="have_ddl" label=false>no ddl</el-radio>
              <datetime type="datetime" v-model="ddl_time"></datetime>
          </el-row>
          

          <!--题目描述、输入、输出-->
          <el-row :gutter="18"
                  class="problem-description-title">Description</el-row>
          <el-row :gutter="18" class="problem-descriptions">
            <el-input  type="textarea" v-model="des"></el-input>
          </el-row>

          <el-row :gutter="18"
                  class="problem-description-title">Input</el-row>
          <el-row :gutter="18" class="problem-descriptions">
            <el-input  type="textarea" v-model="input"></el-input>
          </el-row>
          <el-row :gutter="18"
                  class="problem-description-title">Output</el-row>
          <el-row :gutter="18" class="problem-descriptions">
            <el-input  type="textarea" v-model="output"></el-input>
          </el-row>

          <!--这里放样例波形图-->
          <el-row :gutter="18"
                  class="problem-description-title">Sample waveform</el-row>
          <el-row :gutter="18"
                  id="sample_waveform" class="problem-descriptions">
            <el-input  v-model="waveform" type="textarea"></el-input>
          </el-row>
        </el-card>
      </el-row>

      <el-row>
        <el-card shadow="always">
          <!--提交界面-->
          <el-row :gutter="15">


            <!-- <el-col :span="2">
              <el-button type="info"
                         style="font-weight:bold;margin-left:30px;">Submit Files</el-button>
            </el-col> -->
          </el-row>

          <!--代码编辑-->
          <el-row>
            <el-container style="height: 500px; border: 1px solid #eee">
              <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
                <el-menu :default-openeds="['1', '3']">
                  <el-submenu index="1">
                    <template slot="title"><i class="el-icon-message"></i>代码文件</template>
                    <el-menu-item-group>
                      <template slot="title">模板文件</template>
                      <li v-for="(code_item, index) in code_items" :key="code_item.code">
                        <el-menu-item @click="code_select(code_item.code,'verilog',0,index)">code.v </el-menu-item>
                      </li>
                      <li v-for="(code_template, index) in code_templates" :key="code_template.code">
                        <el-menu-item @click="code_select(code_template.code,'verilog',1,index)">code_template.v</el-menu-item>
                      </li>
                    </el-menu-item-group>
                    <el-menu-item-group title="仿真文件">
                      <li v-for="(testbench,index) in testbenches" :key="testbench.code">
                        <el-menu-item @click="code_select(testbench.code,'verilog',2,index)" >testbench.v</el-menu-item>
                      </li>
                    </el-menu-item-group>
                  </el-submenu>
                  <el-submenu index="2">
                    <template slot="title"><i class="el-icon-menu"></i>判题文件</template>
                    <li v-for="(testcase,index) in testcases" :key="testcase.code">
                    <el-menu-item-group>
                      <template slot="title">判题脚本{{index}}</template>
                      <el-menu-item @click="code_select(testcase.code[0],'python',3,index)" >wavedump.py</el-menu-item>
                      <el-menu-item @click="code_select(testcase.code[1],'python',4,index)" >vcd_main.py</el-menu-item>
                      <el-menu-item @click="code_select(testcase.code[2],'python',5,index)" >vcd_visualize.py</el-menu-item>
                      <el-menu-item @click="code_select(testcase.code[3],'shell',6,index)"  >main.sh</el-menu-item>
                    </el-menu-item-group>
                    </li>

                  </el-submenu>

                </el-menu>
              </el-aside>
              
              <el-container>             
                <el-main id="container_main">
                  <!-- <el-input v-model="code" size=big tpye="textarea"></el-input> -->
                  <codemirror v-model="content"
                        :options="cmOptions"></codemirror>
                </el-main>
              </el-container>
            </el-container>

          </el-row>
        </el-card>
      </el-row>
    </el-col>


  </el-row>
</template>
<style scope>
.CodeMirror {
  height: 500px;
}
</style>
<script>
import moment from "moment";
import qs from "qs";
import { codemirror } from "vue-codemirror";
// import statusmini from "@/components/utils/statusmini";
import languageselect from "@/components/utils/languageselect";
// import prostatistice from "@/components/utils/prostatistice";
import { Datetime } from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'
require("codemirror/lib/codemirror.css");
require("codemirror/theme/base16-light.css");
require("codemirror/theme/base16-dark.css");

require("codemirror/mode/verilog/verilog");
require("codemirror/mode/python/python");
require("codemirror/mode/shell/shell");

export default {
  name: "addproblem",
  components: {
    codemirror,
    // statusmini,
    // prostatistice,
    datetime: Datetime
  },
  data () {
    return {
      title: "",
      des: "",
      input: "",
      output: "",
      datetimeFormat: "YYYY-MM-DD HH:mm:ss",
      endDatetime: null,
      // author: "",
      addtime: "",
      ddl: "",
      have_ddl: false,
    
      tagnames: [],
      activeNames: ["1", "2", "3", "4", "5", "6"],
      level: "Easy",
      ddl_time: null,
      lastindex: 0,
      lastchange: 0,

      content: "",
      code_items : [
        { code: "" }
      ],
      code_templates : [
        { code: "" }
      ],
      testbenches:  [
        { code: "" }
      ],
      testcases: [
        { code:["","","",""] }
      ],

      // language: "Verilog",
      cmOptions: {
        tabSize: 4,
        mode: "Verilog",
        theme: "base16-light",
        lineNumbers: true,
        readOnly: false,
      },
      // template_code: "",
      submissions: [],

      waveform: "",

      // codetemplate: {},

      // ac: 100,
      // mle: 100,
      // tle: 100,
      // rte: 100,
      // pe: 100,
      // ce: 100,
      // wa: 100,
      // se: 100,
      judgetype: "primary",
      loadingshow: false,
      // submitid: -1
    };
  },
  created () {
      this.content =  this.code_items[0].code;

  //   this.$axios
  //     .get("/problems/" + this.id + "/")
  //     .then(response => {
  //       this.des = response.data.description;
  //       this.input = response.data.description_input;
  //       this.output = response.data.description_output;
  //       this.waveform = response.data.app_data;
  //       // this.author = response.data.author;
  //       this.addtime = response.data.create_time =
  //         moment(response.data.create_time).format("YYYY-MM-DD HH:mm:ss");

  //       this.code = "";
  //       if (response.data.template_code_file != null) {
  //         this.$axios.get("/files/" + response.data.template_code_file + "/")
  //         .then(response => {
  //           this.code = response.data;
  //         })
  //       }

  //       // var li = response.data.template.split("*****")
  //       // for (var i = 1; i < li.length; i += 2) {
  //       //   this.codetemplate[li[i]] = li[i + 1]
  //       // }
  //       // this.code = this.codetemplate[this.language]

  //       // this.$axios
  //       //   .get("/problemdata/" + this.ID + "/")
  //       //   .then(response => {
  //       if (response.data["level"] == "1") response.data["level"] = "Easy";
  //       if (response.data["level"] == "2")
  //         response.data["level"] = "Medium";
  //       if (response.data["level"] == "3") response.data["level"] = "Hard";
  //       if (response.data["level"] == "4")
  //         response.data["level"] = "VeryHard";
  //       if (response.data["level"] == "5")
  //         response.data["level"] = "ExtremelyHard";
  //       // response.data.level = "Easy";

  //       if (response.data["tags"] == null) response.data["tags"] = ["无"];
  //       else response.data["tags"] = response.data["tags"].split("|");
  //       // response.data.tag = ["无"];

  //       // if (response.data.submission == 0) {
  //       //   this.ac = 0;
  //       //   this.mle = 0;
  //       //   this.tle = 0;
  //       //   this.rte = 0;
  //       //   this.pe = 0;
  //       //   this.ce = 0;
  //       //   this.wa = 0;
  //       //   this.se = 0;
  //       // } else {
  //       //   this.ac = parseFloat(
  //       //     ((response.data.ac * 100) / response.data.submission).toFixed(2)
  //       //   );
  //       //   this.mle = parseFloat(
  //       //     ((response.data.mle * 100) / response.data.submission).toFixed(
  //       //       2
  //       //     )
  //       //   );
  //       //   this.tle = parseFloat(
  //       //     ((response.data.tle * 100) / response.data.submission).toFixed(
  //       //       2
  //       //     )
  //       //   );
  //       //   this.rte = parseFloat(
  //       //     ((response.data.rte * 100) / response.data.submission).toFixed(
  //       //       2
  //       //     )
  //       //   );
  //       //   this.pe = parseFloat(
  //       //     ((response.data.pe * 100) / response.data.submission).toFixed(2)
  //       //   );
  //       //   this.ce = parseFloat(
  //       //     ((response.data.ce * 100) / response.data.submission).toFixed(2)
  //       //   );
  //       //   this.wa = parseFloat(
  //       //     ((response.data.wa * 100) / response.data.submission).toFixed(2)
  //       //   );
  //       //   this.se = parseFloat(
  //       //     ((response.data.se * 100) / response.data.submission).toFixed(2)
  //       //   );
  //       // }

  //       if (response.data.deadline_time == null) {
  //         this.ddl = "";
  //         this.have_ddl = false;
  //       } else {
  //         this.ddl_time = response.data.deadline_time;
  //         let ddlTime = moment(response.data.deadline_time);
  //         this.ddl = ddlTime.format("YYYY-MM-DD hh:mm:ss") + " (" + ddlTime.endOf('day').fromNow() + ")";
  //         //this.ddl = response.data.deadline_time;
  //         this.have_ddl = true;
  //       }

  //       this.title = response.data.name;
  //       this.level = response.data.level;
  //       this.tagnames = response.data.tags;
  //       this.submissions = response.data.submissions;
  //       this.submissions_refresh();

  //       this.$refs.prosta.setdata(this.$data);

  //     })
  //     .catch(error => {
  //       this.$message.error("服务器错误！" + "(" + JSON.stringify(error.response.data) + ")");
  //     });
  },
  methods: {
    /*
    changetemplate (lang) {
      var t = this.codetemplate[lang]
      if (t) {
        this.$confirm("确定切换语言吗？", "切换后当前代码不会保存！", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(() => {

          this.code = this.codetemplate[lang]
        })
      }
    },
  */
    onCopy (e) {
      this.$message.success("复制成功！");
    },
    // 复制失败
    onError (e) {
      this.$message.error("复制失败：" + e);
    },

    code_select: function( message, language, change, index ) {
      switch(this.lastchange) {
        case 0:
          this.code_items[this.lastindex].code = this.content;
          break;
        case 1:
          this.code_templates[this.lastindex].code = this.content;
          break;
        case 2:
          this.testbenches[this.lastindex].code = this.content;
          break;
        case 3:
          this.testcases[this.lastindex].code[0] = this.content;
          break;
        case 4:
          this.testcases[this.lastindex].code[1] = this.content;
          break;
        case 5:
          this.testcases[this.lastindex].code[2] = this.content;
          break;
        case 6:
          this.testcases[this.lastindex].code[3] = this.content;
          break;
      }

      this.lastchange = change;
      this.lastindex = index;
      this.content = message;
      this.cmOptions["mode"] = language;
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
    statuetype: function(type) {
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
    statuejudge: function(type) {
      if (type == "Pending") return true;
      if (type == "Judging") return true;
      return false;
    },

    rowClick(row, col, e) {
      this.$router.push({
        name: 'submission',
        params: {submissionid: row.id}
      })
    },

    submissions_refresh(){
      this.$axios
        .get(
          "/submissions/?user=" +
            this.username +
            "&problem=" +
            this.problem
        )
        .then(response => {
          for (var i = 0; i < response.data.length; i++) {
            response.data[i]["submittime"] = moment(
              response.data[i]["submit_time"]
            ).format("YYYY-MM-DD");
          }
          this.submissions = response.data;
        });
    },

    problemedit: function(){
      if(this.is_edit==false) {
        this.is_edit = true;
        return;
      }
      else if(!sessionStorage.userid){
        this.$message.error("请先登录！");
        return;
      }
      else{
        this.is_edit = false;
        return this.$axios.put(
          "/problem/"+this.id+"/",{
            name: this.title,
            deadline_time: this.ddl_time,
            description: this.dec,
            description_input: this.input,
            description_output: this.output,
            app_data: this.wavefrom
            }
        ).catch(error => {
          this.$message.error("服务器错误！" + "(" + JSON.stringify(error.response.data) + ")");
        });
      }
    },

    submit: function () {
      if (this.addtime == "") {
        this.$message.error("非法操作！");
        return;
      }
      if (!sessionStorage.userid) {
        this.$message.error("请先登录！");
        return;
      }

      if (!this.code) {
        this.$message.error("请输入代码！");
        return;
      }
      if (!this.language) {
        this.$message.error("请选择语言！");
        return;
      }

      this.$confirm("确定提交吗？", "提交", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.$message({
          type: "success",
          message: "提交中..."
        });

        var formData = new FormData();
        var blob = new Blob([this.code], {type: "text/plain"});
        formData.append('file', blob, 'code.v');
        return this.$axios.post("/files/", formData);
      }).then(response => {
        const fileid = response.data.id;
        return this.$axios.post("/submit", {
          'problem': this.id,
          'submit_files': [fileid],
        });
      }).then(response => {
        this.$router.push({
          name: 'submission',
          params: {submissionid: response.data.id}
        });
      }).catch(error => {
        this.$message.error("提交失败：" + JSON.stringify(error.response.data));
      });
    },
  },
  destroyed () {
  }
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
  left: 10px;
  font-size: 20px;
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
#contain_main {
  padding: 5px 10px;
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
  word-break: break-all;
  white-space: pre-line;
}
.el-row {
  margin-bottom: 20px;
}
.img-responsive {
  display: inline-block;
  height: auto;
  max-width: 75%;
}
</style>
