<template>
  <div>
    <el-row
      type="flex"
      justify="end"
      align="middle"
      style="text-align: right; margin-bottom: 5px; margin-top: 15px"
    >
      <el-col
        :xs="{ span: 12, pull: 0 }"
        :sm="{ span: 7, pull: 0 }"
        :md="{ span: 6, pull: 0 }"
        :lg="{ span: 5, pull: 3 }"
        :xl="{ span: 3, pull: 6 }"
      >
        <el-button
          style="margin-left: 15px"
          plain
          @click="resetsearch"
          size="mini"
          >刷新</el-button
        >
      </el-col>
    </el-row>
    <el-row type="flex" justify="center">
      <el-col :xs="24" :sm="24" :md="24" :lg="18" :xl="12">
        <el-table
          :default-sort="{ prop: 'updatetime', order: 'descending' }"
          :data="tableData"
          :row-style="ratingcolor"
          @row-click="rowClick"
          v-loading="loading"
        >
          <el-table-column
            prop="user_belong.username"
            label="用户"
            :min-width="150"
          ></el-table-column>
          <el-table-column
            prop="title"
            label="主题"
            :min-width="240"
          >
          </el-table-column>
          <el-table-column
            prop="problem_belong.name"
            label="题目"
            :min-width="240"
          >
            <template slot-scope="scope">
              <font color="#409EFF">
                <b style="cursor: pointer">{{
                  scope.row.problem_belong.name
                }}</b>
              </font>
            </template>
          </el-table-column>
          <!-- <el-table-column prop="result" label="状态" :min-width="240">
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
          </el-table-column> -->
          <el-table-column
            prop="updatetime"
            label="最后更新时间"
            :min-width="180"
          ></el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-row> &nbsp; </el-row>
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
  name: "discussion",
  methods: {
    rowClick(row, col, e) {
      if (col.label == "题目") {
        if (this.contest != "0") return;
        this.$router.push({
          name: "problemdetail",
          params: { problemid: row.problem_belong.id },
        });
        return;
      }
      if (col.label == "用户") {
        this.$router.push({
          name: "user",
          params: { userid: row.user_belong.id },
        });
        return;
      }
      this.$router.push({
        name: "topic",
        params: { topicid: row.id },
      });
    },

    resetsearch() {
      this.currentpage = 1;
      this.searchform.problem = "";
      this.searchform.language = "";
      this.searchform.result = "";
      this.getstatusdata();
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

    getstatusdata() {
      this.loading = true;
      let url =
        "/topic/?problem=" +
        this.problemid +
        "&limit=" +
        this.pagesize +
        "&offset=" +
        (this.currentpage - 1) * this.pagesize;
      this.$axios.get(url).then((response) => {
        for (var i = 0; i < response.data.results.length; i++) {
          response.data.results[i].updatetime = moment(
            response.data.results[i].update_time
          ).format("YYYY-MM-DD HH:mm:ss");
        }
        this.tableData = response.data.results;
        this.totalstatus = response.data.count;
        this.loading = false;
      });
    },
  },
  data() {
    return {
      problemid: null,
      isadmin: false,
      tableData: [],
      currentpage: 1,
      pagesize: 30,
      totalstatus: 10,
      contest: "0",
      searchdialogVisible: false,
      loading: false,
      searchform: {
        user: "",
        result: "",
        problem: "",
        language: "",
      },
    };
  },
  computed: {
    ...mapState(["loggedIn", "userID", "username", "isSuperUser"]),
  },
  created() {
    this.problemid = this.$route.params.problemid;
    this.getstatusdata();
  },
};
</script>
