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
            <h3 style="display: inline-block; margin: 3px 0px">
              欢迎您向 Verilog OJ 贡献题目！
            </h3>
          </el-row>
          <el-row>
            <div>
              Verilog OJ
              测试期间需要大家的反馈和配合。我们为新手上路的各位准备了常用的模板，帮助大家完成简单题目的创建。
            </div>
            <div>
              更多信息您可以查看
              <a
                href="https://github.com/YAVGroup/Verilog-OJ/blob/master/doc/operation/Problem_add_HOWTO.md"
                >Verilog OJ 出题指南</a
              >。
            </div>
          </el-row>
        </el-card>
      </el-row>

      <el-row>
        <el-card shadow="never">
          <el-tabs
            tab-position="top"
            v-model="currentTabPageName"
            @tab-click="handleTabPageClick"
          >
            <el-tab-pane label="基本信息" name="BasicInfoTab">
              <el-form
                ref="basicInfoForm"
                :model="basicInfoForm"
                label-width="160px"
                :rules="basisInfoRules"
              >
                <el-form-item label="题目名称" prop="name">
                  <el-input
                    v-model="basicInfoForm.name"
                    maxlength="20"
                    show-word-limit
                  ></el-input>
                </el-form-item>
                <el-form-item label="启用截止时间">
                  <el-switch
                    v-model="basicInfoForm.deadlineEnabled"
                  ></el-switch>
                </el-form-item>
                <el-form-item
                  label="截止时间"
                  v-if="basicInfoForm.deadlineEnabled"
                >
                  <el-col :span="11">
                    <el-date-picker
                      type="datetime"
                      placeholder="选择日期"
                      v-model="basicInfoForm.deadline_time"
                      style="width: 100%"
                    ></el-date-picker>
                  </el-col>
                </el-form-item>
                <el-form-item label="难度">
                  <el-select
                    v-model="basicInfoForm.level"
                    placeholder="请选择难度"
                  >
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
                      style="width: 100%"
                      placeholder="请选择或新增题目标签"
                    >
                      <el-option
                        v-for="item in basicInfoForm.tagOptions"
                        :key="item"
                        :label="item"
                        :value="item"
                      >
                      </el-option>
                    </el-select>
                  </el-col>
                </el-form-item>
                <el-form-item label="题目描述" prop="description">
                  <!-- <el-input
                    type="textarea"
                    v-model="basicInfoForm.description"
                  ></el-input> -->
                  <el-button @click="editInTuiEditor()"
                    >在 TuiEditor 中编辑</el-button
                  >
                  <div style="display: inline-block; margin-left: 20px">
                    描述大小：{{
                      prettySize(getByteLength(this.basicInfoForm.description))
                    }}
                  </div>
                </el-form-item>

                <el-form-item label="输入格式描述" prop="description_input">
                  <el-input
                    type="textarea"
                    v-model="basicInfoForm.description_input"
                    :autosize="{ minRows: 5, maxRows: 15 }"
                  ></el-input>
                </el-form-item>
                <el-form-item label="输出格式描述" prop="description_output">
                  <el-input
                    type="textarea"
                    v-model="basicInfoForm.description_output"
                    :autosize="{ minRows: 5, maxRows: 15 }"
                  ></el-input>
                </el-form-item>
                <el-form-item label="示例波形 (WaveJSON)">
                  <el-input
                    type="textarea"
                    v-model="basicInfoForm.waveform"
                    :autosize="{ minRows: 5, maxRows: 15 }"
                  ></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="waveformPreview"
                    >示例波形预览</el-button
                  >
                  <el-button @click="importFromOtherProblem"
                    >从其他题目导入</el-button
                  >
                </el-form-item>
              </el-form>

              <!-- Sample waveform preview -->
              <el-dialog
                title="示例波形预览"
                :visible.sync="waveformPreviewDialogVisible"
                width="60%"
              >
                <wavedrom
                  waveId="1"
                  :parentText="basicInfoForm.waveform"
                  errorMessage="解析波形时出现错误，请确认您的 WaveJSON 格式正确"
                ></wavedrom>

                <span slot="footer" class="dialog-footer">
                  <el-button
                    type="primary"
                    @click="waveformPreviewDialogVisible = false"
                    >关闭</el-button
                  >
                </span>
              </el-dialog>

              <!-- TuiEditor Markdown editing -->
              <el-dialog
                title="题目描述编辑 (TuiEditor)"
                :visible.sync="tuiEditorDialogVisible"
                width="60%"
              >
                <tuiEditor
                  ref="toastuiEditor"
                  :initialValue="basicInfoForm.description"
                  :options="tuiEditorDefaultOptions"
                  height="600px"
                  initialEditType="wysiwyg"
                  previewStyle="vertical"
                />

                <span slot="footer" class="dialog-footer">
                  <el-button type="primary" @click="closeTuiEditor()"
                    >关闭</el-button
                  >
                </span>
              </el-dialog>
            </el-tab-pane>
            <el-tab-pane label="评测信息" name="JudgeInfoTab">
              <el-dialog
                title="选择模板"
                :visible.sync="templateSelectionDialogVisible"
                :before-close="judgeWorkspaceAbortTemplateSelection"
                :show-close="false"
                width="30%"
              >
                <div
                  v-for="(value, key) in judgeWorkspaceTemplates"
                  v-bind:key="key"
                >
                  <el-radio :label="key" v-model="templateSelectionChosen">{{
                    value.name
                  }}</el-radio>
                  <el-row style="margin-top: 6px"
                    >描述：{{ value.description }}</el-row
                  >
                </div>

                <span slot="footer" class="dialog-footer">
                  <el-button
                    type="primary"
                    plain
                    @click="
                      () => {
                        this.judgeWorkspaceImport(
                          this.templateSelectionChosen,
                          false
                        );
                        templateSelectionDialogVisible = false;
                      }
                    "
                    >导入全部</el-button
                  >
                  <el-button
                    type="primary"
                    plain
                    @click="
                      () => {
                        this.judgeWorkspaceImport(
                          this.templateSelectionChosen,
                          true
                        );
                        templateSelectionDialogVisible = false;
                      }
                    "
                    >仅导入测试用例</el-button
                  >
                  <el-button
                    plain
                    @click="templateSelectionDialogVisible = false"
                    >取消</el-button
                  >
                </span>
              </el-dialog>

              <el-row>
                <el-container>
                  <el-aside>
                    <el-row style="margin: 20px">
                      <el-button-group>
                        <!-- Add {file, testcase} -->
                        <el-button
                          plain
                          size="small"
                          @click="judgeWorkspaceShowTemplateSelection"
                          >导入模板</el-button
                        >
                      </el-button-group>
                    </el-row>
                    <el-row>
                      <el-tree
                        :data="judgeInfoHierarchy"
                        :props="{
                          children: 'children',
                          label: 'name',
                        }"
                        :expand-on-click-node="false"
                        default-expand-all
                        highlight-current
                      >
                        <span
                          class="judge-workspace-treenode"
                          slot-scope="{ node, data }"
                          @click="handleTreeHierarchyClick(node, data)"
                        >
                          <span>{{ node.label }}</span>
                          <span>
                            <el-button
                              type="text"
                              size="mini"
                              @click.stop="() => judgeWorkspaceAddFile(data)"
                              v-if="
                                !!data.fileAppendable && data.fileAppendable
                              "
                            >
                              添加
                            </el-button>
                            <el-button
                              type="text"
                              size="mini"
                              @click.stop="
                                () => judgeWorkspaceDeleteFile(node, data)
                              "
                              v-if="
                                !!data.isFile !== 'undefined' && data.isFile
                              "
                            >
                              删除
                            </el-button>
                            <el-button
                              type="text"
                              size="mini"
                              @click.stop="
                                () => judgeWorkspaceAddTestcase(data)
                              "
                              v-if="
                                !!data.testcaseAppendable !== 'undefined' &&
                                data.testcaseAppendable
                              "
                            >
                              添加
                            </el-button>
                            <el-button
                              type="text"
                              size="mini"
                              @click.stop="
                                () => judgeWorkspaceDeleteTestcase(node, data)
                              "
                              v-if="
                                !!data.isTestCase !== 'undefined' &&
                                data.isTestCase
                              "
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
                      <el-input
                        placeholder="example.py"
                        v-model="currentWorkspace.fileNode.fileName"
                      >
                        <template slot="prepend">文件名</template>
                        <template slot="append">{{ prettyModeName }}</template>
                      </el-input>
                    </el-row>
                    <el-row>
                      <codemirror
                        ref="masterCm"
                        v-model="currentWorkspace.fileNode.content"
                        :options="cmOptionsByFileName"
                        v-on:changes="handleEditorContentChange"
                      ></codemirror>
                    </el-row>
                  </el-main>
                </el-container>
              </el-row>
            </el-tab-pane>
          </el-tabs>
          <!-- 这里的操作比较 dirty，是直接用 absolute 定位扔到那个位置，这里要注意叠放次序保证按钮在上（就是先写 el-tabs 后写 el-button），否则会按不到 -->
          <!-- Ref: https://segmentfault.com/q/1010000020057405 -->
          <el-button
            type="success"
            size="medium"
            @click="submitAll"
            :loading="submitButtonBusy"
            style="
              font-weight: bold;
              position: absolute;
              right: 25px;
              top: 17px;
            "
            >提交</el-button
          >
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
import { Datetime } from "vue-datetime";
import wavedrom from "@/components/utils/wavedrom";
import "vue-datetime/dist/vue-datetime.css";

import { mapState } from "vuex";
import Userhyperlink from "../utils/userhyperlink.vue";

import { Editor } from "@toast-ui/vue-editor";
import "@toast-ui/editor/dist/toastui-editor.css";

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
    wavedrom,
    tuiEditor: Editor,
  },
  data() {
    return {
      basicInfoForm: {
        name: "",
        description: "",
        description_input: "",
        description_output: "",
        deadlineEnabled: false,
        deadline_time: "",
        waveform: "",
        level: 1,
        tags: [],
        tagOptions: ["组合逻辑", "时序逻辑"],
      },
      basisInfoRules: {
        name: [{ required: true, message: "请输入题目名称", trigger: "blur" }],
        description: [
          { required: true, message: "请输入题目描述", trigger: "blur" },
        ],
        description_input: [
          { required: true, message: "请输入题目输入描述", trigger: "blur" },
        ],
        description_output: [
          { required: true, message: "请输入题目输出描述", trigger: "blur" },
        ],
      },
      /**
       * Used to illustrate {problem, testcase} related files and grades
       */
      judgeInfoHierarchy: [
        {
          name: "题目",
          type: "Problem",
          children: [
            {
              name: "模板代码文件",
              type: "ProblemMeta",
              patchKey: "template_code_file",
              fileAppendable: true,
              isMultiple: false,
              children: [],
            },
            {
              name: "评测所用文件",
              type: "ProblemMeta",
              patchKey: "judge_files",
              fileAppendable: true,
              isMultiple: true,
              children: [],
            },
          ],
        },
        {
          get name() {
            return (
              "测试用例 " +
              "(需要删除: " +
              this.serverTestcaseTobeDeleted.length +
              ")"
            );
          },
          type: "TestCases",
          testcaseAppendable: true,
          // Used purely for local identification, remote have no such mechanics
          testcaseNextID: 0,
          // To be deleted in server in next sync
          serverTestcaseTobeDeleted: [],
          children: [],
        },
      ],
      judgeWorkspaceTemplates: {},
      templateSelectionDialogVisible: false,
      templateSelectionChosen: "",
      currentWorkspace: {
        fileNode: {
          // one-off default for now
          fileName: "",
          content: "在左侧创建文件以开始编辑。",
          contentChanged: () => {
            // No-op for this placebo
          },
        },
        enableNotification: false,
      },
      // BasicInfoTab, JudgeInfoTab
      currentTabPageName: "BasicInfoTab",
      submitButtonBusy: false,
      waveformPreviewDialogVisible: false,
      tuiEditorDialogVisible: false,
      tuiEditorDefaultOptions: {
        minHeight: "200px",
        language: "en-US",
        useCommandShortcut: true,
        usageStatistics: true,
        hideModeSwitch: false,
        toolbarItems: [
          ["heading", "bold", "italic", "strike"],
          ["hr", "quote"],
          ["ul", "ol", "task", "indent", "outdent"],
          ["table", "image", "link"],
          ["code", "codeblock"],
          ["scrollSync"],
        ],
      },
    };
  },
  computed: {
    prettyModeName() {
      let currentCmOptions = this.cmOptionsByFileName;
      if (currentCmOptions.mode == "null") {
        return "无高亮";
      } else {
        let mode = currentCmOptions.mode;
        return mode.substring(0, 1).toUpperCase() + mode.substring(1);
      }
    },
    cmOptionsByFileName() {
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
    inProblemEditMode() {
      return this.$route.params.problemid != null;
    },
    ...mapState(["loggedIn", "userID", "username", "isSuperUser"]),
  },
  created() {
    if (this.$route.params.problemid != null) {
      this.fillBasicInfoByProblem(this.$route.params.problemid);
      this.fillJudgeInfoByProblem(this.$route.params.problemid);
    }
  },
  methods: {
    editInTuiEditor() {
      this.tuiEditorDialogVisible = true;
    },
    closeTuiEditor() {
      let mdData = this.$refs.toastuiEditor.invoke("getMarkdown");
      this.basicInfoForm.description = mdData;
      this.tuiEditorDialogVisible = false;
    },
    getByteLength(str) {
      // https://stackoverflow.com/questions/5515869/string-length-in-bytes-in-javascript/23329386#23329386
      // returns the byte length of an utf8 string
      let s = str.length;
      for (let i = str.length - 1; i >= 0; i--) {
        let code = str.charCodeAt(i);
        if (code > 0x7f && code <= 0x7ff) s++;
        else if (code > 0x7ff && code <= 0xffff) s += 2;
        if (code >= 0xdc00 && code <= 0xdfff) i--; //trail surrogate
      }
      return s;
    },
    prettySize(size) {
      let unit = "B";
      let units = ["B", "KiB", "MiB", "GiB", "TiB"];
      while ((unit = units.shift()) && size > 1024) {
        size = size / 1024;
      }
      return (unit === "B" ? size : size.toFixed(2)) + " " + unit;
    },
    waveformPreview() {
      this.waveformPreviewDialogVisible = true;
    },
    importFromOtherProblem() {
      this.$message.error("尚未实现！");
    },
    getModeByExtension(extName) {
      const mmap = {
        py: "python",
        v: "verilog",
        sh: "shell",
      };
      if (typeof mmap[extName] != "undefined") {
        return mmap[extName];
      } else {
        return "null";
      }
    },
    // Ref: https://stackoverflow.com/questions/8349571/codemirror-editor-is-not-loading-content-until-clicked
    handleTabPageClick(tabInst, event) {
      // console.log(tabInst, event);
      if (tabInst.name == "JudgeInfoTab") {
        this.$refs.masterCm.refresh();
      }
    },
    handleTreeHierarchyClick(node, data) {
      if (typeof data.isFile != "undefined" && data.isFile) {
        this.currentWorkspace.enableNotification = false;
        this.$set(this.currentWorkspace, "fileNode", data);
        this.$nextTick(() => {
          this.currentWorkspace.enableNotification = true;
        });
      }
    },
    handleEditorContentChange(changeObj) {
      if (this.currentWorkspace.enableNotification) {
        this.currentWorkspace.fileNode.contentChanged();
      }
    },
    // Judge File Related
    judgeWorkspaceAddFile(data) {
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
          return (
            this.fileName +
            (this.serverFileID != null
              ? " (ID: " + this.serverFileID + ")"
              : "") +
            (this.inSyncWithServer ? " (Sync)" : " (Not Sync)")
          );
        },
        contentChanged: function () {
          this.inSyncWithServer = false;
          if (typeof data.inSyncWithServer != "undefined") {
            data.inSyncWithServer = false;
          }
        },
      };
      if (typeof data.inSyncWithServer != "undefined") {
        data.inSyncWithServer = false;
      }
      data.children.push(newFile);
      if (!data.isMultiple) {
        data.fileAppendable = false;
      }
      return newFile;
    },
    judgeWorkspaceDeleteFile(node, data) {
      const parent = node.parent;
      const children = parent.data.children;
      // Compare Object means compare reference
      const index = children.findIndex((d) => d === data);
      children.splice(index, 1);
      if (typeof parent.data.inSyncWithServer != "undefined") {
        parent.data.inSyncWithServer = false;
      }

      if (!parent.data.isMultiple) {
        parent.data.fileAppendable = true;
      }
    },
    judgeWorkspaceAddTestcase(data) {
      const newTestcase = {
        isTestCase: true,
        inSyncWithServer: false,
        serverTestCaseID: null,
        isMultiple: true,
        fileAppendable: true,
        localTestcaseID: data.testcaseNextID++,
        children: [],
        get name() {
          return (
            "Testcase #" +
            this.localTestcaseID +
            (this.serverTestCaseID != null
              ? " (ID: " + this.serverTestCaseID.toString() + ")"
              : "") +
            (this.inSyncWithServer ? " (Sync)" : " (Not Sync)")
          );
        },
      };
      data.children.push(newTestcase);
      return newTestcase;
    },
    judgeWorkspaceDeleteTestcase(node, data) {
      const parent = node.parent;
      const children = parent.data.children;
      // Compare Object means compare reference
      const index = children.findIndex((d) => d === data);
      children.splice(index, 1);

      if (data.serverTestCaseID != null) {
        parent.data.serverTestcaseTobeDeleted.push(data.serverTestCaseID);
      }
    },
    judgeWorkspaceShowTemplateSelection() {
      this.judgeWorkspaceGetTemplatesBrief().then(() => {
        this.templateSelectionDialogVisible = true;
      });
    },
    judgeWorkspaceAbortTemplateSelection(done) {
      // no-op to force click "Cancel"
      return;
    },
    judgeWorkspaceGetTemplatesBrief() {
      return this.$axios({
        url: "testcase-templates/index.json",
        baseURL: process.env.BASE_URL,
      })
        .then((response) => {
          this.judgeWorkspaceTemplates = response.data;
        })
        .catch((error) => {
          this.$message.error(
            "获取模板时出现错误：" + JSON.stringify(error.response.data)
          );
        });
    },
    judgeWorkspaceGetTemplate(templateName) {
      return this.$axios({
        url:
          "testcase-templates/" +
          this.judgeWorkspaceTemplates[templateName].url +
          "/index.json",
        baseURL: process.env.BASE_URL,
      })
        .then((response) => {
          this.judgeWorkspaceTemplates[templateName]["content"] = response.data;
        })
        .catch((error) => {
          this.$message.error(
            "获取模板 " +
              templateName +
              " 时出现错误：" +
              JSON.stringify(error.response.data)
          );
        });
    },
    /**
     * judgeWorkspaceImport
     * testcaseOnly - add a new testcase, ignore others
     * TODO: use relative position
     */
    judgeWorkspaceImport(templateName, testcaseOnly) {
      return this.judgeWorkspaceGetTemplate(templateName).then(() => {
        let problemPromises = [];
        if (!testcaseOnly) {
          // erase existing problem files
          this.$set(this.judgeInfoHierarchy[0].children[0], "children", []);
          this.judgeInfoHierarchy[0].children[0].fileAppendable = true;
          this.$set(this.judgeInfoHierarchy[0].children[1], "children", []);
          this.judgeInfoHierarchy[0].children[1].fileAppendable = true;

          problemPromises = [
            // template_code_file
            this.$axios({
              url:
                "testcase-templates/" +
                this.judgeWorkspaceTemplates[templateName].url +
                "/" +
                this.judgeWorkspaceTemplates[templateName].content
                  .template_code_file,
              baseURL: process.env.BASE_URL,
            }).then((response) => {
              let fileInst = this.judgeWorkspaceAddFile(
                this.judgeInfoHierarchy[0].children[0]
              );
              fileInst.fileName =
                this.judgeWorkspaceTemplates[
                  templateName
                ].content.template_code_file;
              fileInst.content = response.data;
            }),
            // judge_files
            ...this.judgeWorkspaceTemplates[
              templateName
            ].content.judge_files.map((filename) => {
              return this.$axios({
                url:
                  "testcase-templates/" +
                  this.judgeWorkspaceTemplates[templateName].url +
                  "/" +
                  filename,
                baseURL: process.env.BASE_URL,
              }).then((response) => {
                let fileInst = this.judgeWorkspaceAddFile(
                  this.judgeInfoHierarchy[0].children[1]
                );
                fileInst.fileName = filename;
                fileInst.content = response.data;
              });
            }),
          ];
        }

        let testInst = this.judgeWorkspaceAddTestcase(
          this.judgeInfoHierarchy[1]
        );

        const testcasePromises = [
          // testcase_files
          ...this.judgeWorkspaceTemplates[
            templateName
          ].content.testcase_files.map((filename) => {
            return this.$axios({
              url:
                "testcase-templates/" +
                this.judgeWorkspaceTemplates[templateName].url +
                "/" +
                filename,
              baseURL: process.env.BASE_URL,
            }).then((response) => {
              let fileInst = this.judgeWorkspaceAddFile(testInst);
              fileInst.fileName = filename;
              fileInst.content = response.data;
            });
          }),
        ];

        Promise.all([...problemPromises, ...testcasePromises])
          .then(() => {
            this.$message.success("模板导入成功！");
          })
          .catch((error) => {
            this.$message.error("模板导入失败! " + error.response.data);
          });
      });
    },

    // Returns a Promise with problemID on fulfilled
    submitBasicInfo() {
      let basicInfo = {
        name: this.basicInfoForm.name,
        deadline_time: this.basicInfoForm.deadlineEnabled
          ? this.basicInfoForm.deadline_time
          : null,
        level: this.basicInfoForm.level,
        tags: this.basicInfoForm.tags.join("|"),
        description: this.basicInfoForm.description,
        description_input: this.basicInfoForm.description_input,
        description_output: this.basicInfoForm.description_output,
        app_data: this.basicInfoForm.waveform,
      };

      if (this.inProblemEditMode) {
        // should override existing ones
        let problemID = this.$route.params.problemid;

        return this.$axios
          .patch("/problems/" + problemID + "/", {
            id: problemID,
            ...basicInfo,
          })
          .then((response) => {
            return response.data.id; // return problemID on resolved
          });
      } else {
        return this.$axios
          .post("/problems/", {
            ...basicInfo,
          })
          .then((response) => {
            return response.data.id; // return problemID on resolved
          });
      }
    },
    // returns Promise with fileID on fulfilled
    submitFile(fileID, fileContent, fileName) {
      // TODO: Patch file instead of add - use /api/files/{}/
      let formData = new FormData();
      formData.append(
        "file",
        new Blob([fileContent], { type: "text/plain" }),
        fileName
      );
      return this.$axios.post("/files/", formData).then((response) => {
        return response.data.id;
      });
    },

    // returns Promise
    /**
     * TODO: use relative position
     */
    submitJudgeWorkspace(problemID) {
      let problemPromises = [];
      let testcasePromises = [];

      // Problem files
      this.judgeInfoHierarchy[0].children.forEach((element) => {
        let name = element.name;
        let patchKey = element.patchKey;
        let isMultiple = element.isMultiple;

        if (!isMultiple && element.children.length > 1) {
          throw "Expected single element on " + name;
        }

        if (element.children.length == 0) {
          return;
        }

        let filesPromises = [];

        element.children.forEach((fileDesc) => {
          filesPromises.push(
            new Promise((resolve, reject) => {
              // Already uploaded, so no need to do it twice
              if (fileDesc.inSyncWithServer && fileDesc.serverFileID != null) {
                resolve(fileDesc.serverFileID);
              } else {
                this.submitFile(
                  fileDesc.serverFileID,
                  fileDesc.content,
                  fileDesc.fileName
                )
                  .then((fileID) => {
                    fileDesc.serverFileID = fileID;
                    fileDesc.inSyncWithServer = true;
                    resolve(fileID);
                  })
                  .catch((error) => {
                    reject(error);
                  });
              }
            })
          );
        });

        // Patch it when everything ready
        problemPromises.push(
          Promise.all(filesPromises).then((values) => {
            let body = {};
            if (isMultiple) {
              body[patchKey] = values;
            } else {
              body[patchKey] = values[0];
            }

            return this.$axios.patch("/problems/" + problemID + "/", body);
          })
        );
      });

      // Testcase preparation
      let testcasePreparation = Promise.all([
        ...this.judgeInfoHierarchy[1].serverTestcaseTobeDeleted.map(
          (testcaseID) => {
            return this.$axios.delete("/problem-testcases/" + testcaseID + "/");
          }
        ),
      ]).then((val) => {
        this.judgeInfoHierarchy[1].serverTestcaseTobeDeleted = [];
        return val;
      });

      // Testcase files
      this.judgeInfoHierarchy[1].children.forEach((element) => {
        // Submit all files
        let filesPromises = [];

        element.children.forEach((fileDesc) => {
          filesPromises.push(
            new Promise((resolve, reject) => {
              // Already uploaded, so no need to do it twice
              if (fileDesc.inSyncWithServer && fileDesc.serverFileID != null) {
                resolve(fileDesc.serverFileID);
              } else {
                this.submitFile(
                  fileDesc.serverFileID,
                  fileDesc.content,
                  fileDesc.fileName
                )
                  .then((fileID) => {
                    fileDesc.serverFileID = fileID;
                    fileDesc.inSyncWithServer = true;
                    resolve(fileID);
                  })
                  .catch((error) => {
                    reject(error);
                  });
              }
            })
          );
        });

        // Patch or make it when everything ready
        problemPromises.push(
          Promise.all(filesPromises).then((values) => {
            if (element.serverTestCaseID == null) {
              return this.$axios
                .post("/problem-testcases/", {
                  type: "SIM",
                  testcase_files: values,
                  problem: problemID,
                })
                .then((response) => {
                  element.serverTestCaseID = response.data.id;
                  element.inSyncWithServer = true;
                  return element.serverTestCaseID;
                });
            } else {
              // patch existing server testcase
              // TODO: use inSyncWithServer and maintain properly
              return this.$axios
                .patch("/problem-testcases/" + element.serverTestCaseID + "/", {
                  testcase_files: values,
                  problem: problemID,
                })
                .then((response) => {
                  element.inSyncWithServer = true;
                });
            }
          })
        );
      });

      return Promise.all([
        ...problemPromises,
        testcasePreparation,
        ...testcasePromises,
      ]).then((arrayOfResults) => {
        return problemID;
      });
    },
    submitAll() {
      console.log("submitAll() called.");

      this.submitButtonBusy = true;
      // validate forms
      this.$refs["basicInfoForm"]
        .validate()
        .then(
          () => {
            this.submitBasicInfo()
              .then(
                (problemID) => {
                  // submit everything else
                  return this.submitJudgeWorkspace(problemID);
                },
                (error) => {
                  this.$message.error("提交基本信息失败：" + error);
                  console.log("ERROR:", error.response.data);
                }
              )
              .then((problemID) => {
                this.$message.success("提交成功！");
                this.$router.push({
                  name: "problemdetail",
                  params: { problemid: problemID },
                });
              });
          },
          (error) => {
            this.$message.error("校验基本信息失败：" + error);
          }
        )
        .finally(() => {
          this.submitButtonBusy = false;
        });
    },
    fillBasicInfoByProblem(problemID) {
      this.$axios
        .get("/problems/" + problemID)
        .then((response) => {
          let problem = response.data;

          let formNewVal = {
            name: problem.name,
            description: problem.description,
            description_input: problem.description_input,
            description_output: problem.description_output,
            deadlineEnabled: problem.deadline_time != null,
            deadline_time: problem.deadline_time,
            waveform: problem.app_data,
            level: problem.level,
            tags:
              problem.tags.split("|").length == 1
                ? []
                : problem.tags.split("|"),
          };

          this.basicInfoForm = formNewVal;
        })
        .catch((error) => {
          this.$message.error(
            "题目信息获取失败：" + JSON.stringify(error.response.data)
          );
        });
    },
    /*
     * This only works with problem owned by the current logged user
     */
    fillJudgeInfoByProblem(problemID) {
      this.$axios
        .get("/problems/" + problemID)
        .then((response) => {
          let problem = response.data;

          const downloadFile = (fileID) => {
            return this.$axios.get("/files/" + fileID).then((response) => {
              // response['Content-Disposition'] = 'attachment; filename="%s"'
              let content_disp = response.headers["content-disposition"];

              return {
                fileName: content_disp.slice(22, content_disp.length - 1),
                content: response.data,
              };
            });
          };

          // [ { id: 5, files: [1,2,3] } , ...]
          let testcaseFiles = problem.testcases.map((testcase) => {
            return {
              id: testcase.id,
              files: testcase.testcase_files,
            };
          });

          let judgeFiles = problem.judge_files;
          let templateCodeFile = problem.template_code_file;

          let problemPromises = [
            // template_code_file
            downloadFile(templateCodeFile).then((val) => {
              let fileInst = this.judgeWorkspaceAddFile(
                this.judgeInfoHierarchy[0].children[0]
              );
              fileInst.fileName = val.fileName;
              fileInst.content = val.content;
              fileInst.serverFileID = templateCodeFile;
              fileInst.inSyncWithServer = true;
            }),
            // judge_files
            ...judgeFiles.map((fileID) => {
              downloadFile(fileID).then((val) => {
                let fileInst = this.judgeWorkspaceAddFile(
                  this.judgeInfoHierarchy[0].children[1]
                );
                fileInst.fileName = val.fileName;
                fileInst.content = val.content;
                fileInst.serverFileID = fileID;
                fileInst.inSyncWithServer = true;
              });
            }),
          ];

          // TODO: do this !!
          let testcasePromises = [
            ...problem.testcases.map((testcase) => {
              let testInst = this.judgeWorkspaceAddTestcase(
                this.judgeInfoHierarchy[1]
              );

              return Promise.all([
                ...testcase.testcase_files.map((fileID) => {
                  return downloadFile(fileID).then((val) => {
                    let fileInst = this.judgeWorkspaceAddFile(testInst);
                    fileInst.fileName = val.fileName;
                    fileInst.content = val.content;
                    fileInst.inSyncWithServer = true;
                    fileInst.serverFileID = fileID;
                  });
                }),
              ]).then((val) => {
                testInst.inSyncWithServer = true;
                testInst.serverTestCaseID = testcase.id;
                return val;
              });
            }),
          ];

          return Promise.all([...problemPromises, ...testcasePromises]);
        })
        .catch((error) => {
          this.$message.error(
            "题目信息获取失败：" + JSON.stringify(error.response.data)
          );
        });
    },
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

.active,
.collapsible:hover {
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
