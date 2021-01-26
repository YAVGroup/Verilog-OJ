<template>
  <div>
    <el-row>
      &nbsp;
    </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
    <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
    <el-dialog :visible.sync="searchdialogVisible">
      <el-form :model="searchform"
               label-position="right"
               @keyup.native.enter="searchstatus">
        <el-form-item label="User:">
          <el-input v-model="searchform.user"
                    placeholder="User..."></el-input>
        </el-form-item>
        <el-form-item label="Problem Number：">
          <el-input v-model="searchform.problem"
                    placeholder="Problem Number...or ABCDE"></el-input>
        </el-form-item>
        <el-form-item label="Language：">
          <el-select v-model="searchform.language"
                     placeholder="Choose...">
            <languageselect></languageselect>
          </el-select>
        </el-form-item>
        <el-form-item label="Result：">
          <el-select v-model="searchform.result"
                     placeholder="Choose...">
            <el-option key="0"
                       label="Accepted"
                       value="0"></el-option>
            <el-option key="1"
                       label="Wrong Answer"
                       value="-3"></el-option>
            <el-option key="2"
                       label="Waiting"
                       value="-6"></el-option>
            <el-option key="3"
                       label="Presentation Error"
                       value="-5"></el-option>
            <el-option key="4"
                       label="Compile Error"
                       value="-4"></el-option>
            <el-option key="5"
                       label="Pending"
                       value="-1"></el-option>
            <el-option key="6"
                       label="Judging"
                       value="-2"></el-option>
            <el-option key="7"
                       label="Time Limit Exceeded 1"
                       value="1"></el-option>
            <el-option key="8"
                       label="Time Limit Exceeded 2"
                       value="2"></el-option>
            <el-option key="9"
                       label="Memory Limit Exceeded"
                       value="3"></el-option>
            <el-option key="10"
                       label="Runtime Error"
                       value="4"></el-option>
            <el-option key="11"
                       label="System Error"
                       value="5"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer"
           class="dialog-footer">
        <el-button @click="searchdialogVisible = false">Cancel</el-button>
        <el-button type="primary"
                   @click="searchstatus">OK</el-button>
      </div>
    </el-dialog>

    <el-switch style="float: right; margin: 10px;"
               v-model="showall"
               active-text="仅自己"
               inactive-text="所有人"
               @change="statuechange"></el-switch>
    <el-button plain
               @click="resetsearch"
               style="float: right;margin-top:6px;margin-right:10px;"
               size="mini">刷新</el-button>
    <!-- <el-button type="primary"
               @click="searchdialogVisible = true"
               style="float: right;margin-top:6px;margin-right:15px;"
               size="mini">Filter</el-button> -->

    <!-- <el-pagination @size-change="handleSizeChange"
                   @current-change="handleCurrentChange"
                   :current-page="currentpage"
                   :page-sizes="[10, 20, 30, 50]"
                   :page-size="pagesize"
                   layout="total, sizes, prev, pager, next, jumper"
                   :total="totalstatus"></el-pagination> -->

    <el-table :default-sort="{prop: 'id', order: 'descending'}"
              :data="tableData"
              style="width: 100%"
              :row-style="ratingcolor"
              @row-click="rowClick"
              size="medium"
              v-loading="loading">
      <el-table-column prop="id"
                       label="ID"
                       :width="50"></el-table-column>
      <el-table-column prop="user_belong.username"
                       label="用户"
                       :width="70"></el-table-column>
      <el-table-column prop="problem_belong.name"
                       label="题名">
        <template slot-scope="scope">
          <font color="#409EFF">
            <b style="cursor:pointer;">{{ scope.row.problem_belong.name }}</b>
          </font>
        </template>
      </el-table-column>
      <el-table-column prop="result"
                       label="状态"
                       :width="200">
        <template slot-scope="scope">
          <el-tag size="medium"
                  :type="statuetype(scope.row.result)"
                  disable-transitions
                  hit>
            {{ scope.row.result }}
            <i class="el-icon-loading"
               v-show="statuejudge(scope.row.result)"></i>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="submittime"
                       label="提交时间"
                       :width="180"></el-table-column>
    </el-table>
    <el-row>
      &nbsp;
    </el-row>
    <center>
      <el-pagination @size-change="handleSizeChange"
                     @current-change="handleCurrentChange"
                     :current-page="currentpage"
                     :page-sizes="[10, 20, 30, 50]"
                     :page-size="pagesize"
                     layout="total, sizes, prev, pager, next, jumper"
                     :total="totalstatus"></el-pagination>
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

export default {
  name: "statue",
  methods: {
    rowClick (row, col, e) {
      if (col.label == "Problem") {
        if (this.contest != "0")
          return
        this.$router.push({
          name: "problemdetail",
          params: { problemid: row.problem_belong.id }
        });
        return;
      }

      if (col.label == "User") {
        this.$router.push({
          name: "user",
          params: { userid: row.user_belong.id }
        });
        return;
      }

      this.$router.push({
        name: 'submission',
        params: {submissionid: row.id}
      })
    },
    searchstatus () {
      this.currentpage = 1;
      this.searchdialogVisible = false;
      this.setusername(this.searchform.user);
      this.getstatusdata();
    },
    resetsearch () {
      this.currentpage = 1;
      this.searchform.user = "";
      this.setusername(this.searchform.user);
      this.searchform.problem = "";
      this.searchform.language = "";
      this.searchform.result = "";
      this.creattimer();
    },
    handleSizeChange (val) {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "0";
      if (!this.username) this.username = "";
      this.pagesize = val;
      this.getstatusdata();
    },
    handleCurrentChange (val) {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "0";
      if (!this.username) this.username = "";
      this.currentpage = val;
      this.getstatusdata();
    },
    ratingcolor ({ row, rowIndex }) {
      var back = "";
      if (row.result == "Accepted")
        back = "background:#e6ffdf;font-weight: bold;";

      if (row.rating >= 3000) return "color:red;" + back;
      if (row.rating >= 2600) return "color:#BB5E00;" + back;
      if (row.rating >= 2200) return "color:#E6A23C;" + back;
      if (row.rating >= 2050) return "color:#930093;" + back;
      if (row.rating >= 1900) return "color:#0000AA;" + back;
      if (row.rating >= 1700) return "color:#007799;" + back;
      if (row.rating >= 1500) return "color:#227700;" + back;
      if (row.rating >= 1350) return "color:#67C23A;" + back;
      if (row.rating >= 1200) return "color:#909399;" + back;
      return "color:#303133;" + back;
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
      if (type == "Time Limit Exceeded") return "warning";
      if (type == "Memory Limit Exceeded") return "warning";
      if (type == "Runtime Error") return "warning";
      if (type == "System Error") return "danger";

      return "danger";
    },
    statuejudge: function (type) {
      if (type == "Pending") return true;
      if (type == "Judging") return true;
      if (type == "Wrong Answer") return false;
      if (type == "Compile Error") return false;
      if (type == "Presentation Error") return false;
      if (type == "Waiting") return true;
      if (type == "Accepted") return false;
      if (type == "Time Limit Exceeded") return false;
      if (type == "Time Limit Exceeded") return false;
      if (type == "Memory Limit Exceeded") return false;
      if (type == "Runtime Error") return false;
      if (type == "System Error") return false;
      return false;
    },
    timer: function () {
      if (!this.username) this.username = this.$route.query.username;
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "0";
      if (!this.username) this.username = "";

      if (this.username == sessionStorage.username && sessionStorage.username)
        this.showall = true;
      else this.showall = false;
      this.getstatusdata();
    },

    getstatusdata () {
      this.loading = true;
      var url = "/submissions/?user=" +
        this.username +
        "&limit=" +
        this.pagesize +
        "&offset=" +
        (this.currentpage - 1) * this.pagesize;
        // "&problemtitle=" +
        // this.searchform.problem +
        // "&language=" +
        // this.searchform.language +
        // "&result=" +
        // this.searchform.result +
        // "&contest=" +
        // this.contest;

      this.$axios
        .get(url)
        .then(response => {
          for (var i = 0; i < response.data.length; i++) {
            response.data[i].submittime = moment(response.data[i].submit_time).format("YYYY-MM-DD HH:mm:ss");
            response.data[i].language = "Verilog";
          }
          this.tableData = response.data;
          this.totalstatus = response.data.length;
          this.loading = false;
        });
    },

    setusername (name) {   //实际为userid
      this.$route.query.username = "";
      this.username = name;
    },
    statuechange (val) {
      if (val == true) {
        if (!sessionStorage.userid) {
          this.showall = false;
          this.$message.error("请先登录！");
        } else this.setusername(sessionStorage.userid);
      } else {
        this.setusername("");
      }
      this.getstatusdata();
    },
    creattimer () {
      clearInterval(this.$store.state.timer);
      this.timer();
      // this.$store.state.timer = setInterval(this.timer, 500); 
      // 取消自动刷新
    },
  },
  data () {
    return {
      cmOptions: {
        tabSize: 4,
        mode: "text/x-c++src",
        theme: "base16-light",
        lineNumbers: true,
        readOnly: true,
        viewportMargin: Infinity,
        lineWrapping: true
      },
      isadmin: false,
      tableData: [],
      currentpage: 1,
      pagesize: 30,
      totalstatus: 10,
      username: "",
      contest: "0",
      showall: false,
      searchdialogVisible: false,
      loading: false,
      searchform: {
        user: "",
        result: "",
        problem: "",
        language: ""
      }
    };
  },
  computed: mapState([
    'loggedIn',
    'userID',
    'username',
    'isSuperUser'
  ]),
  destroyed () {
    clearInterval(this.$store.state.timer);
  },
  created () {
    //创建一个全局定时器，定时刷新状态
    this.isadmin = sessionStorage.isadmin;
    this.timer();
    // this.$store.state.timer = setInterval(this.timer, 500);
    // 取消自动刷新
  }
};
</script>
