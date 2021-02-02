<template>
  <div>
    <el-row
      type="flex"
      justify="end"
      align="middle"
      style="text-align: right; margin-bottom: 5px; margin-top: 15px;"
    >
      <el-col
        :xs="{ span: 12, pull: 0 }"
        :sm="{ span: 7, pull: 0 }"
        :md="{ span: 6, pull: 2 }"
        :lg="{ span: 5, pull: 3 }"
        :xl="{ span: 3, pull: 4 }"
      >
        <el-switch
          v-model="showMeOnly"
          active-text="仅自己"
          inactive-text="所有人"
          :disabled="!this.loggedIn"
        ></el-switch>
        <el-button
          style="margin-left: 15px;"
          plain
          @click="resetsearch"
          size="mini"
          >刷新</el-button
        >
      </el-col>
    </el-row>
    <el-row type="flex" justify="center">
      <el-col :xs="24" :sm="24" :md="20" :lg="18" :xl="16">
        <el-table
          :default-sort="{ prop: 'id', order: 'descending' }"
          :data="tableData"
          :row-style="ratingcolor"
          @row-click="rowClick"
          v-loading="loading"
        >
          <el-table-column
            prop="id"
            label="ID"
            :min-width="50"
          ></el-table-column>
          <el-table-column
            prop="user_belong.username"
            label="用户"
            :min-width="150"
          ></el-table-column>
          <el-table-column
            prop="problem_belong.name"
            label="题名"
            :min-width="240"
          >
            <template slot-scope="scope">
              <font color="#409EFF">
                <b style="cursor:pointer;">{{
                  scope.row.problem_belong.name
                }}</b>
              </font>
            </template>
          </el-table-column>
          <el-table-column prop="result" label="状态" :min-width="240">
            <template slot-scope="scope">
              <el-tag
                size="medium"
                :type="statuetype(scope.row.result)"
                disable-transitions
                hit
              >
                {{ scope.row.result }}
                <i
                  class="el-icon-loading"
                  v-show="statuejudge(scope.row.result)"
                ></i>
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="submittime"
            label="提交时间"
            :min-width="180"
          ></el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-row>
      &nbsp;
    </el-row>
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

export default {
  name: "statue",
  methods: {
    rowClick(row, col, e) {
      if (col.label == "Problem") {
        if (this.contest != "0") return;
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
        name: "submission",
        params: { submissionid: row.id }
      });
    },

    searchstatus() {
      this.currentpage = 1;
      this.searchdialogVisible = false;
      this.getstatusdata();
    },

    resetsearch() {
      this.currentpage = 1;
      this.searchform.problem = "";
      this.searchform.language = "";
      this.searchform.result = "";
      this.creattimer();
    },

    handleSizeChange(val) {
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "0";
      this.pagesize = val;
      this.getstatusdata();
    },

    handleCurrentChange(val) {
      this.contest = this.$route.params.contestID;
      if (!this.contest) this.contest = "0";
      this.currentpage = val;
      this.getstatusdata();
    },

    ratingcolor({ row, rowIndex }) {
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

    statuetype: function(type) {
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

    statuejudge: function(type) {
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

    getstatusdata() {
      this.loading = true;
      let url =
        "/submissions/?limit=" +
        this.pagesize +
        "&offset=" +
        (this.currentpage - 1) * this.pagesize;
      if (this.queryUserName) {
        url += "&user=" + this.queryUserName;
      }
      this.$axios.get(url).then(response => {
        for (var i = 0; i < response.data.results.length; i++) {
          response.data.results[i].submittime = moment(
            response.data.results[i].submit_time
          ).format("YYYY-MM-DD HH:mm:ss");
          response.data.results[i].language = "Verilog";
        }
        this.tableData = response.data.results;
        this.totalstatus = response.data.count;
        this.loading = false;
      });
    }
  },
  data() {
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
      contest: "0",
      showMeOnly: false,
      queryUserName: "",
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
  computed: {
    ...mapState(["loggedIn", "userID", "username", "isSuperUser"])
  },
  watch: {
    loggedIn: function() {
      if (!this.loggedIn) {
        this.showMeOnly = false;
        this.queryUserName = "";
      }
    },
    showMeOnly: function() {
      if (this.showMeOnly) {
        this.queryUserName = this.userID;
      } else {
        this.queryUserName = "";
      }
    },
    queryUserName: function() {
      this.getstatusdata();
    }
  },
  created() {
    this.getstatusdata();
  }
};
</script>
