<template>
  <el-row :gutter="15">
    <el-col :span="18">
      <el-row>
        <el-card shadow="always">
          <!--标题、DDL-->
          <el-row gutter="18">
            <el-col :span="2">
              <el-button type="success"
                         @click="problemedit"
                         style="font-weight:bold;margin-left:10px;">Submit</el-button>
            </el-col>
            <el-col :span="2">
              <el-button type="danger"
                         @click="is_change=false"
                         style="font-weight:bold;margin-left:30px;" v-if="is_change">Cancel</el-button>
              <el-button v-else type="danger"
                         @click="is_change=true"
                         style="font-weight:bold;margin-left:30px;">Edit</el-button>
            </el-col>
          </el-row>
          <el-row :gutter="18" 
            class="problem-description-title" v-if="is_change">select problem</el-row>
          <el-row :gutter="18" 
            class="problem-description-title" v-if="is_change">
              <el-select v-model="problem_id" placeholder="题目：">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-row>
          <el-row :gutter="18" id="ddl" >Title</el-row>
          <el-row :gutter="18" id="title">
            <el-col :span="20">
              <el-input v-model="title"></el-input>
            </el-col>
          </el-row>
          <el-row :gutter="18" id="ddl" >Deadline</el-row>
          <el-row :gutter="18" class="problem-descriptions" >
              <el-radio v-model="have_ddl" :label="true">have ddl</el-radio>
              <el-radio v-model="have_ddl" :label="false">no ddl</el-radio>
              <datetime type="datetime" icon="el-icon-date" v-model="ddl_time" v-show="have_ddl" ></datetime>
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

          <el-row :gutter="18"
                  class="problem-description-title">Level </el-row>
          <el-row :gutter="18" class="problem-descriptions">        
              <el-select v-model="level" placeholder="难度：">
                <el-option key="1" label="简单" :value="1"></el-option>
                <el-option key="2" label="普通" :value="2"></el-option>
                <el-option key="3" label="中等" :value="3"></el-option>
                <el-option key="4" label="困难" :value="4"></el-option>
                <el-option key="5" label="极其困难" :value="5"></el-option>
              </el-select>
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

          <el-row>
            <el-button @click="retrieveTemplate">
              Test frontend retrieve
            </el-button>
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
      is_change: false,
      options:[],
      problem_id:0,

      tagnames: [],
      activeNames: ["1", "2", "3", "4", "5", "6"],
      level: 1,
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

      this.$axios.get("/problems/?owner=" + sessionStorage.userid)
      .then(response => {
          var problems = response.data;
          for (var i=0;i<problems.length;i=i+1) {
            this.options.push({
              "value": problems[i]["id"],
              "label": problems[i]["id"]+" "+problems[i]["name"],
            })
          }
        });

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

    async upload(code, filename) {
        var formData = new FormData();
        var blob = new Blob([code], {type: "text/plain"});
        formData.append('file', blob, filename);
        return this.$axios.post("/files/", formData).then(response => {
          return response.data.id;
        }).catch(error => {
            this.$message.error("提交错误！" + filename + "(" + JSON.stringify(error.response.data) + ")");
          });  
    },

    async upload_testcase(code_ids,problemid) {
        var body = {};
        body['type'] = 'SIM';
        body['testcase_files'] = code_ids ;
        body['problem'] = problemid;
        return this.$axios.post("/problem-testcases/", body).catch(error => {
            this.$message.error("提交错误！" + "(" + JSON.stringify(error.response.data) + ")");
          });  
    },

    async problemedit() {
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

        const code_id = await this.upload(this.code_items[0].code,'code_ref.v');
        const template_id = await this.upload(this.code_templates[0].code,'template_code.v');
        const testbench_id = await this.upload(this.testbenches[0].code,'testbench.v');
        const wavedump_id = await this.upload(this.testcases[0].code[0],'wavedump.py');
        const vcd_main_id = await this.upload(this.testcases[0].code[1],'vcd_main.py');
        const vcd_visualize_id = await this.upload(this.testcases[0].code[2],'vcd_visualize.py');
        const main_id = await this.upload(this.testcases[0].code[3],'main.sh');
        var body = {}
        body['name'] = this.title;
        body['description'] = this.des;
        body['description_input'] = this.input;
        body['description_output'] = this.output;
        body['app_data'] = this.waveform;
        body['level'] = this.level;
        body['owner'] = this.username;
        body['template_code_file'] = template_id;
        body['judge_files'] = [code_id];
        if(this.have_ddl)
          body['deadline_time'] = this.ddl_time;
        console.log(template_id);
        return this.$axios.post(
            "/problems/",body
          ).then(response => {
            this.upload_testcase([wavedump_id,vcd_main_id,vcd_visualize_id,main_id,testbench_id],
              response.data.id
            );
            this.$router.push({
            name: 'problemdetail',
            params: {problemid: response.data.id}
        })}).catch(error => {
            this.$message.error("服务器错误！" + "(" + JSON.stringify(error.response.data) + ")");
          });  
      }
    },
    retrieveTemplate: function () {
      alert(process.env.BASE_URL);
      this.$axios({
        url: 'testcase-templates/index.json',
        baseURL: process.env.BASE_URL
      }).then(response => {
        alert(response.data);
      })
    },
    problemchange() {
      this.is_change = true;
      this.$axios
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
