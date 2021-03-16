<template>
  <el-row :gutter="15">
    <el-col :xs="0" :sm="1" :md="2" :lg="2" :xl="4" class="placeholder">
      <!-- placeholder only -->
      &nbsp;
    </el-col>
    <el-col :xs="24" :sm="22" :md="20" :lg="20" :xl="16">
      <!-- Welcome message -->
      <el-row>
        <el-card shadow="never">
          <el-row>
            <h3 style="display: inline-block; margin: 3px 0px;">欢迎您向 Verilog OJ 贡献题目！</h3>
          </el-row>
          <el-row>
            <div>
              Verilog OJ 测试期间需要大家的反馈和配合。我们为新手上路的各位准备了常用的模板，帮助大家完成简单题目的创建。
            </div>
            <div>
              更多信息您可以查看
              <a href="https://github.com/YAVGroup/Verilog-OJ/blob/master/doc/operation/Problem_add_HOWTO.md">Verilog OJ 出题指南</a>。
            </div>
          </el-row>
        </el-card>
      </el-row>

      <el-row>
        <el-card shadow="never">
          <el-tabs tab-position="top"
                   v-model="currentTabPageName"
                   @tab-click="handleTabPageClick">
            <el-tab-pane label="基本信息" name="BasicInfoTab">

              <el-form ref="basicInfoForm" :model="basicInfoForm" label-width="160px">
                <el-form-item label="题目名称">
                  <el-input v-model="basicInfoForm.name" maxlength="20" show-word-limit></el-input>
                </el-form-item>
                <el-form-item label="启用截止时间">
                  <el-switch v-model="basicInfoForm.deadlineEnabled"></el-switch>
                </el-form-item>
                <el-form-item label="截止时间" v-if="basicInfoForm.deadlineEnabled">
                  <el-col :span="11">
                    <el-date-picker type="datetime"
                                    placeholder="选择日期"
                                    v-model="basicInfoForm.deadline_time"
                                    style="width: 100%;"></el-date-picker>
                  </el-col>
                </el-form-item>
                <el-form-item label="难度">
                  <el-select v-model="basicInfoForm.level" placeholder="请选择难度">
                    <el-option key="1" label="简单" :value="1"></el-option>
                    <el-option key="2" label="普通" :value="2"></el-option>
                    <el-option key="3" label="中等" :value="3"></el-option>
                    <el-option key="4" label="困难" :value="4"></el-option>
                    <el-option key="5" label="极其困难" :value="5"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="题目标签">
                  <el-col :span="11">
                    <el-select
                      v-model="basicInfoForm.tags"
                      multiple
                      filterable
                      allow-create
                      default-first-option
                      style="width: 100%;"
                      placeholder="请选择或新增题目标签">
                      <el-option
                        v-for="item in basicInfoForm.tagOptions"
                        :key="item"
                        :label="item"
                        :value="item">
                      </el-option>
                    </el-select>
                  </el-col>
                </el-form-item>
                <el-form-item label="题目描述">
                  <el-input type="textarea" v-model="basicInfoForm.description"></el-input>
                </el-form-item>
                <el-form-item label="输入格式描述">
                  <el-input type="textarea" v-model="basicInfoForm.description_input"
                            :autosize="{ minRows: 5, maxRows: 15}"></el-input>
                </el-form-item>
                <el-form-item label="输出格式描述">
                  <el-input type="textarea" v-model="basicInfoForm.description_output"
                            :autosize="{ minRows: 5, maxRows: 15}"></el-input>
                </el-form-item>
                <el-form-item label="示例波形 (WaveJSON)">
                  <el-input type="textarea" v-model="basicInfoForm.waveform"
                            :autosize="{ minRows: 5, maxRows: 15}"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary">预览</el-button>
                  <el-button>从其他题目导入</el-button>
                </el-form-item>
              </el-form>


            </el-tab-pane>
            <el-tab-pane label="评测信息" name="JudgeInfoTab">
              <el-dialog
                title="选择模板"
                :visible.sync="templateSelectionDialogVisible"
                :before-close="judgeWorkspaceAbortTemplateSelection"
                :show-close="false"
                width="30%">
                <div v-for="(value, key) in judgeWorkspaceTemplates" v-bind:key="key">
                  <el-radio :label="key" v-model="templateSelectionChosen">{{ value.name }}</el-radio>
                  <el-row style="margin-top: 6px;">描述：{{ value.description }}</el-row>
                </div>

                <span slot="footer" class="dialog-footer">
                  <el-button type="primary" plain 
                             @click="() => {this.judgeWorkspaceImport(this.templateSelectionChosen, false); templateSelectionDialogVisible = false;}"
                             >导入全部</el-button>
                  <el-button type="primary" plain 
                             @click="() => {this.judgeWorkspaceImport(this.templateSelectionChosen, true); templateSelectionDialogVisible = false;}"
                             >仅导入测试用例</el-button>
                  <el-button plain @click="templateSelectionDialogVisible = false">取消</el-button>
                </span>
              </el-dialog>

              <el-row>
                <el-container>
                  <el-aside>
                    <el-row style="margin: 20px;">
                      <el-button-group>
                        <!-- Add {file, testcase} -->
                        <el-button plain size="small" @click="judgeWorkspaceShowTemplateSelection">导入模板</el-button>
                      </el-button-group>
                      
                    </el-row>
                    <el-row>
                      <el-tree  :data="judgeInfoHierarchy"
                                :props="{
                                          children: 'children',
                                          label: 'name'
                                        }"
                                :expand-on-click-node="false"
                                default-expand-all
                                highlight-current
                                >
                        <span class="judge-workspace-treenode" slot-scope="{ node, data }"
                              @click="handleTreeHierarchyClick(node, data)">
                          <span>{{ node.label }}</span>
                          <span>
                            <el-button
                              type="text"
                              size="mini"
                              @click.stop="() => judgeWorkspaceAddFile(data)"
                              v-if="typeof data.fileAppendable !== 'undefined' && data.fileAppendable"
                              >
                              添加
                            </el-button>
                            <el-button
                              type="text"
                              size="mini"
                              @click.stop="() => judgeWorkspaceDeleteFile(node, data)"
                              v-if="typeof data.isFile !== 'undefined' && data.isFile"
                              >
                              删除
                            </el-button>
                            <el-button
                              type="text"
                              size="mini"
                              @click.stop="() => judgeWorkspaceAddTestcase(data)"
                              v-if="typeof data.testcaseAppendable !== 'undefined' && data.testcaseAppendable"
                              >
                              添加
                            </el-button>
                            <el-button
                              type="text"
                              size="mini"
                              @click.stop="() => judgeWorkspaceDeleteTestcase(node, data)"
                              v-if="typeof data.isTestCase !== 'undefined' && data.isTestCase"
                              >
                              删除
                            </el-button>
                          </span>
                        </span>
                      </el-tree>
                    </el-row>

                    
                  </el-aside>
                  <el-main>
                    <el-row>
                        <el-input placeholder="example.py" v-model="currentWorkspace.fileNode.fileName">
                          <template slot="prepend">文件名</template>
                          <template slot="append">{{ prettyModeName }}</template>
                        </el-input>

                      
                    </el-row>
                    <el-row>
                      <codemirror ref="masterCm" v-model="currentWorkspace.fileNode.content"
                                  :options="cmOptionsByFileName"></codemirror>
                    </el-row>

                  </el-main>
                </el-container>

              </el-row>


            </el-tab-pane>
          </el-tabs>
          <!-- 这里的操作比较 dirty，是直接用 absolute 定位扔到那个位置，这里要注意叠放次序保证按钮在上（就是先写 el-tabs 后写 el-button），否则会按不到 -->
          <!-- Ref: https://segmentfault.com/q/1010000020057405 -->
          <el-button type="success"
                    size="medium"
                    @click="submitAll"
                    :loading="submitButtonBusy"
                    style="font-weight: bold; position: absolute; right: 25px; top: 17px;">提交</el-button>
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
import wavedrom from "@/components/utils/wavedrom";
import 'vue-datetime/dist/vue-datetime.css'

import { mapState } from 'vuex';
import Userhyperlink from '../utils/userhyperlink.vue';

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
    // wavedrom
  },
  data () {
    return {
      basicInfoForm: {
        name: '',
        description: '',
        description_input: '',
        description_output: '',
        deadlineEnabled: false,
        deadline_time: '',
        waveform: '',
        level: 1,
        tags: [],
        tagOptions: ['组合逻辑', '时序逻辑']
      },
      /**
       * Used to illustrate {problem, testcase} related files and grades
       */
      judgeInfoHierarchy: [
        {
          name: '题目',
          type: 'Problem',
          children: [
            {
              name: '模板代码文件',
              type: 'ProblemMeta',
              patchUrl: '/problems/{problemid}/',
              patchKey: 'template_code_file',
              fileAppendable: true,
              isMultiple: false,
              children: []
            },
            {
              name: '评测所用文件',
              type: 'ProblemMeta',
              patchUrl: '/problems/{problemid}/',
              patchKey: 'template_code_file',
              fileAppendable: true,
              isMultiple: false,
              children: []
            }
          ]
        },
        {
          name: '测试用例',
          type: 'TestCases',
          testcaseAppendable: true,
          // Used purely for local identification, remote have no such mechanics
          testcaseNextID: 0,
          children: []
        }
      ],
      judgeWorkspaceTemplates: {},
      templateSelectionDialogVisible: false,
      templateSelectionChosen: "",
      currentWorkspace: {
        fileNode: {       // one-off default for now
          fileName: "",
          content: "在左侧创建文件以开始编辑。"
        }
      },
      // BasicInfoTab, JudgeInfoTab
      currentTabPageName: "BasicInfoTab",
      submitButtonBusy: false,

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
      retrieve_title: "",
      retrieve_code: "",
      waveedit: true,

      tagnames: [],
      activeNames: ["1", "2", "3", "4", "5", "6"],
      level: 1,
      ddl_time: null,
      lastindex: 0,
      lastchange: 0,
      retrievefile: 0,
      dialogVisible: false,

      content: "",
      code_items : [
        { code: "" }
      ],
      code_templates : [
        { code: "" }
      ],

      //对应顺序为wavedump.py,vcd_main.py,testbench.v,vcd_visualize.v,main.sh
      testcases: [
        { code:["","","","",""] }
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
  computed: {
    prettyModeName () {
      let currentCmOptions = this.cmOptionsByFileName;
      if (currentCmOptions.mode == "null") {
        return "无高亮";
      } else {
        let mode = currentCmOptions.mode;
        return mode.substring(0, 1).toUpperCase() + mode.substring(1);
      }
    },
    cmOptionsByFileName () {
      let segments = this.currentWorkspace.fileNode.fileName.split(".");
      let mode = "";
      if (segments.length < 2) {
        mode = "null";
      } else {
        let extension = segments[segments.length - 1];
        mode = this.getModeByExtension(extension);
      }

      return {
        tabSize: 4,
        mode: mode,
        theme: "base16-light",
        lineNumbers: true,
        readOnly: false,
      };
    },
    inProblemEditMode () {
      return this.$route.params.problemid != null;
    },
    ...mapState([
      'loggedIn',
      'userID',
      'username',
      'isSuperUser'
    ])
  },
  created () {
      if (this.$route.params.problemid!=null) {
        this.is_change = true;
        this.fillBasicInfoByProblem(this.$route.params.problemid);
      }

      if(this.is_change) { //edit模式
        this.$axios.get("/problems/"+ this.$route.params.problemid +"/?id="+ this.$route.params.problemid + 
          "&owner=" + this.userID).then(response => {
          var problem = response.data;
          // console.log(problem);
          this.title = problem["name"];
          if(problem["deadline_time"]==null) {
            this.have_ddl = false;
            this.ddl_time = null;
          } else {
            this.have_ddl = true;
            this.ddl_time = problem["deadline_time"];
          }
          this.level = problem["level"];
          this.des = problem["description"];
          this.input = problem["description_input"];
          this.output = problem["description_output"];
          this.waveform = problem["app_data"];
          //对应需要单独获取对应的testfile文件
          var testcases = problem["testcases"][0]["testcase_files"];

          //对应顺序为wavedump.py,vcd_main.py,testbench.v,vcd_visualize.v,main.sh
          if (testcases !=null ) {
            //循环会导致奇怪的错误
            for(var i=0;i<testcases.length;i++) {
              this.$axios.get("/files/" + testcases[i] + "/")
                .then(response => {
                  // console.log(response.data);
                  var temp = response.headers["content-disposition"];
                  // response['Content-Disposition'] = 'attachment; filename="%s"'
              
                  var filename = temp.slice(22,temp.length-1);
                  // console.log(filename)
                  switch(filename) {//对应顺序为wavedump.py,vcd_main.py,testbench.v,vcd_visualize.py,main.sh
                    case "wavedump.py": 
                      this.testcases[0].code[0] = response.data;
                      break;
                    case "vcd_main.py":
                      this.testcases[0].code[1] = response.data;
                      break;
                    case "testbench.v":
                      this.testcases[0].code[2] = response.data;
                      break;
                    case "vcd_visualize.py":
                      this.testcases[0].code[3] = response.data;
                      break;
                    case "main.sh":
                      this.testcases[0].code[4] = response.data;
                      break;
                  }
              })
            }
          }

          var  template = problem["template_code_file"];

          if (template != null) {
            this.$axios.get("/files/" + template + "/")
            .then(response => {
              this.code_templates[0].code = response.data;
            })
          }

          var judge = problem["judge_files"][0];

          if (judge!=null) {
            this.$axios.get("/files/" + judge + "/")
                .then(response => {
              this.code_items[0].code = response.data;
            })
          }

        }).catch(error => {
              this.$message.error("发生错误！" + "(" + JSON.stringify(error.response.data) + ")");
            }); 
        this.content =  this.code_items[0].code;
      } else {
        console.log("add problem");
      }

  },
  methods: {
    getModeByExtension (extName) {
      const mmap = {
        py: "python",
        v: "verilog",
        sh: "shell"
      };
      if (typeof mmap[extName] != 'undefined') {
        return mmap[extName];
      } else {
        return "null";
      }
    },
    // Ref: https://stackoverflow.com/questions/8349571/codemirror-editor-is-not-loading-content-until-clicked
    handleTabPageClick (tabInst, event) {
      // console.log(tabInst, event);
      if (tabInst.name == 'JudgeInfoTab') {
        this.$refs.masterCm.refresh();
      }
    },
    handleTreeHierarchyClick (node, data) {
      if (typeof data.isFile != 'undefined' && data.isFile) {
        this.$set(this.currentWorkspace, "fileNode", data);
     }
    },
    // Judge File Related
    judgeWorkspaceAddFile (data) {
      const newFile = {
        isFile: true,
        fileName: "newFile.txt",
        isBinary: false, // TODO: support for binary files
        inSyncWithServer: false, // use el-icon-cloudy to represent server sync
        serverFileID: null,
        content: "",
        // https://stackoverflow.com/questions/51059477/defining-user-defined-getters-in-a-vue-component
        // ^ So no problem defining user getters
        get name() {
          return this.fileName 
                 + (this.inSyncWithServer ? 
                    " (" + this.serverFileID + ")" : " (Not Sync)");
        }
      };
      data.children.push(newFile);
      if (!data.isMultiple) {
        data.fileAppendable = false;
      }
      return newFile;
    },
    judgeWorkspaceDeleteFile (node, data) {
      const parent = node.parent;
      const children = parent.data.children;
      // Compare Object means compare reference
      const index = children.findIndex(d => d === data);
      children.splice(index, 1);

      if (!parent.data.isMultiple) {
        parent.data.fileAppendable = true;
      }
    },
    judgeWorkspaceAddTestcase (data) {
      const newTestcase = {
        isTestCase: true,
        inSyncWithServer: false,
        serverTestCaseID: null,
        isMultiple: true,
        fileAppendable: true,
        localTestcaseID: data.testcaseNextID++,
        children: [],
        get name() {
          return "Testcase #" + this.localTestcaseID +
                (this.inSyncWithServer ? 
                    " (" + this.serverTestCaseID + ")"
                  : " (Not Sync)" );
        }
      };
      data.children.push(newTestcase);
    },
    judgeWorkspaceDeleteTestcase (node, data) {
      const parent = node.parent;
      const children = parent.data.children;
      // Compare Object means compare reference
      const index = children.findIndex(d => d === data);
      children.splice(index, 1);

      if (!parent.data.isMultiple) {
        parent.data.fileAppendable = true;
      }
    },
    judgeWorkspaceShowTemplateSelection () {
      this.judgeWorkspaceGetTemplatesBrief().then(() => {
        this.templateSelectionDialogVisible = true;
      });
    },
    judgeWorkspaceAbortTemplateSelection (done) {
      // no-op to force click "Cancel"
      return;
    },
    judgeWorkspaceGetTemplatesBrief () {
      return this.$axios({
        url: 'testcase-templates/index.json',
        baseURL: process.env.BASE_URL
      }).then(response => {
        this.judgeWorkspaceTemplates = response.data;
      }).catch(error => {
        this.$message.error(
          "获取模板时出现错误：" + JSON.stringify(error.response.data)
        );
      });
    },
    judgeWorkspaceGetTemplate (templateName) {
      return this.$axios({
        url: 'testcase-templates/' + this.judgeWorkspaceTemplates[templateName].url + "/index.json",
        baseURL: process.env.BASE_URL
      }).then(response => {
        this.judgeWorkspaceTemplates[templateName]["content"] = response.data;
      }).catch(error => {
        this.$message.error(
          "获取模板 " + templateName + " 时出现错误：" + JSON.stringify(error.response.data)
        );
      });
    },
    /**
     * judgeWorkspaceImport
     * testcaseOnly - add a new testcase, ignore others
     * TODO: use relative position
     */
    judgeWorkspaceImport (templateName, testcaseOnly) {
      return this.judgeWorkspaceGetTemplate(templateName).then(() => {
        let problemPromises = [];
        if (!testcaseOnly) {
          problemPromises = [
            // template_code_file
            this.$axios({
              url: 'testcase-templates/' 
                    + this.judgeWorkspaceTemplates[templateName].url + "/"
                    + this.judgeWorkspaceTemplates[templateName].content.template_code_file,
              baseURL: process.env.BASE_URL
            }).then(response => {
              let fileInst = this.judgeWorkspaceAddFile(this.judgeInfoHierarchy[0].children[0]);
              fileInst.fileName = this.judgeWorkspaceTemplates[templateName].content.template_code_file;
              fileInst.content = response.data;
            }),
            // judge_files
            ...this.judgeWorkspaceTemplates[templateName].content.judge_files.map(
              (filename) => {
                return this.$axios({
                  url: 'testcase-templates/' 
                        + this.judgeWorkspaceTemplates[templateName].url + "/"
                        + filename,
                  baseURL: process.env.BASE_URL
                }).then(response => {
                  let fileInst = this.judgeWorkspaceAddFile(this.judgeInfoHierarchy[0].children[1]);
                  fileInst.fileName = filename;
                  fileInst.content = response.data;
                })
              }
            )
          ];
        }
        
        // erase existing testcases
        this.$set(this.judgeInfoHierarchy[1], "children", []);
        this.judgeWorkspaceAddTestcase(this.judgeInfoHierarchy[1]);

        const testcasePromises = [
          // testcase_files
          ...this.judgeWorkspaceTemplates[templateName].content.testcase_files.map(
            (filename) => {
              return this.$axios({
                url: 'testcase-templates/' 
                      + this.judgeWorkspaceTemplates[templateName].url + "/"
                      + filename,
                baseURL: process.env.BASE_URL
              }).then(response => {
                let fileInst = this.judgeWorkspaceAddFile(this.judgeInfoHierarchy[1].children[0]);
                fileInst.fileName = filename;
                fileInst.content = response.data;
              })
            }
          )
        ];
        
        Promise.all([...problemPromises, ...testcasePromises]).then(() => {
          this.$message.success("模板导入成功！");
        }).catch((error) => {
          this.$message.error("模板导入失败! " + error.response.data);
        });
      })
    },

    // Returns a Promise with problemID on fulfilled
    submitBasicInfo () {
      let basicInfo = {
        name: this.basicInfoForm.name,
        deadline_time: this.basicInfoForm.deadlineEnabled ? 
                        this.basicInfoForm.deadline_time :
                        null,
        level: this.basicInfoForm.level,
        tags: this.basicInfoForm.tags.join("|"),
        description: this.basicInfoForm.description,
        description_input: this.basicInfoForm.description_input,
        description_output: this.basicInfoForm.description_output,
        app_data: this.basicInfoForm.waveform
      };

      if (this.inProblemEditMode) {
        // should override existing ones
        let problemID = this.$route.params.problemid;

        return this.$axios.patch(
          "/problems/" + problemID + "/", {
            id: problemID,
            ...basicInfo
          }
        ).then((response) => {
          return response.data.id;   // return problemID on resolved
        });
      } else {
        return this.$axios.post(
          "/problems/", {
            ...basicInfo
          }
        ).then((response) => {
          return response.data.id;   // return problemID on resolved
        });
      }
    },
    // returns Promise with fileID on fulfilled
    submitFile (fileID, fileContent) {
      
    },

    // returns Promise
    submitJudgeWorkspace () {

    },
    submitAll () {
      console.log("submitAll() called.");
      this.submitButtonBusy = true;
      this.submitBasicInfo().then(
        (problemID) => {
          // submit everything else

        },
        (error) => {
          this.$message.error("提交基本信息失败：" + error.response.data);
        }
      ).finally(() => {
        this.$message.success("提交成功!");
        this.submitButtonBusy = false;
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

    async deltestcase(problemid) {
      return this.$axios.get("/problem-testcases/?problem=" + problemid + "/" ).then(response => {
        var res = response.data;
        for (var i=0;i < res.length;i=i+1) {
            console.log(res[i]);
            this.$axios.delete("problem-testcases/"+
              res[i].id+"/"
            );
        }
            }).catch(error => {
            this.$message.error("提交错误！" + "(" + JSON.stringify(error.response.data) + ")");
          });  
    },

    async problemedit() {
      if(this.is_edit==false) {
        this.is_edit = true;
        return;
      }
      else if(!this.loggedIn){
        this.$message.error("请先登录！");
        return;
      }
      else{
        switch(this.lastchange) {
          case 0:
            this.code_items[this.lastindex].code = this.content;
            break;
          case 1:
            this.code_templates[this.lastindex].code = this.content;
            break;
          case 2:
            this.testcases[this.lastindex].code[0] = this.content;
            break;
          case 3:
            this.testcases[this.lastindex].code[1] = this.content;
            break;
          case 4:
            this.testcases[this.lastindex].code[2] = this.content;
            break;
          case 5:
            this.testcases[this.lastindex].code[3] = this.content;
            break;
          case 6:
            this.testcases[this.lastindex].code[4] = this.content;
            break;
      }
        this.is_edit = false;

        const code_id = await this.upload(this.code_items[0].code,'code_ref.v');
        const template_id = await this.upload(this.code_templates[0].code,'template_code.v');
        const wavedump_id = await this.upload(this.testcases[0].code[0],'wavedump.py');
        const vcd_main_id = await this.upload(this.testcases[0].code[1],'vcd_main.py');
        const testbench_id = await this.upload(this.testcases[0].code[2],'testbench.v');
        const vcd_visualize_id = await this.upload(this.testcases[0].code[3],'vcd_visualize.py');
        const main_id = await this.upload(this.testcases[0].code[4],'main.sh');
        var body = {}
        body['name'] = this.title;
        body['description'] = this.des;
        body['description_input'] = this.input;
        body['description_output'] = this.output;
        body['app_data'] = this.waveform;
        body['level'] = this.level;
        body['owner'] = this.userID;
        body['template_code_file'] = template_id;
        body['judge_files'] = [code_id];
        if(this.have_ddl)
          body['deadline_time'] = this.ddl_time;
        // console.log(template_id);
        if (this.is_change) {

          await this.deltestcase(this.$route.params.problemid);
          this.$axios.patch(
            "/problems/" + this.$route.params.problemid + "/", body
          )

          // for(var j=0;j<testcase_list.length;j=j+1) {
          //   this.$axios.delete("/problem-testcases/"+testcase_list[j].id+"/").catch(error=>{
          //     this.$message.error("提交错误！" + "(" + JSON.stringify(error.response.data) + ")");
          //   });
          // }
          // var testcase_body = {};
          // testcase_body['type'] = 'SIM';
          // testcase_body['testcase_files'] = [wavedump_id,vcd_main_id,vcd_visualize_id,main_id,testbench_id];
          // testcase_body['problem'] = this.$route.params.problemid;
          // this.$axios.patch("/problem-testcases/"+ this.$route.params.problemid + "/", testcase_body).catch(error => {
          //     this.$message.error("提交错误！" + "(" + JSON.stringify(error.response.data) + ")");
          //   });
          this.upload_testcase([wavedump_id,vcd_main_id,vcd_visualize_id,main_id,testbench_id],
              this.$route.params.problemid
            );
            return   this.$router.push({
              name: 'problemdetail',
              params: {problemid: this.$route.params.problemid}
              }).catch(error => {
              this.$message.error("服务器错误！" + "(" + JSON.stringify(error.response.data) + ")");
          });  

        }
        else return this.$axios.post(
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
    fillBasicInfoByProblem (problemID) {
      this.$axios.get("/problems/" + problemID).then(response => {
        let problem = response.data;
        
        let formNewVal = {
          name: problem.name,
          description: problem.description,
          description_input: problem.description_input,
          description_output: problem.description_output,
          deadlineEnabled: (problem.deadline_time != null),
          deadline_time: problem.deadline_time,
          waveform: problem.app_data,
          level: problem.level,
          tags: problem.tags.split("|").length == 1 ? [] : problem.tags.split("|")
        };

        this.basicInfoForm = formNewVal;
      }).catch(error => {
        this.$message.error(
          "题目信息获取失败：" + JSON.stringify(error.response.data)
        );
      });
    },
    /*
     * This only works with problem owned by the current logged user
     */
    fillJudgeInfoByProblem (problemID) {
      this.$axios.get("/problems/" + problemID).then(response => {
        let problem = response.data;
        
        const downloadFile = (fileID) => {
          return this.$axios.get("/files/" + fileID).then(response => {
            return {
              fileName: null,
              content: response.data
            };
          });
        };

        // [ { id: 5, files: [1,2,3] } , ...]
        let testcaseFiles = problem.testcases.map((testcase) => {
          return {
            id: testcase.id,
            files: testcase.testcase_files
          };
        });

        let judgeFiles = problem.judge_files;
        let templateCodeFile = problem.template_code_file;

      }).catch(error => {
        this.$message.error(
          "题目信息获取失败：" + JSON.stringify(error.response.data)
        );
      });
    }
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
.el-row {
  margin-bottom: 20px;
}
.img-responsive {
  display: inline-block;
  height: auto;
  max-width: 75%;
}

.collapsible {
  background-color: #777;
  color: white;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.active, .collapsible:hover {
  background-color: #555;
}

.content {
  padding: 0 18px;
  display: none;
  overflow: hidden;
  background-color: #f1f1f1;
}

.judge-workspace-treenode {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

</style>
