<template>
  <div>
    <el-row> &nbsp; </el-row>
    <el-row :gutter="15">
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <!-- 上方选页
        <el-pagination @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"
                       :current-page="currentpage"
                       :page-sizes="[15, 20, 30, 50]"
                       :page-size="pagesize"
                       layout="total, sizes, prev, pager, next, jumper"
                       :total="totalproblem"></el-pagination> -->
        <el-button
          round
          icon="el-icon-document-add"
          style="float: right"
          @click="newProblem"
          size="medium"
        >
          添加题目
        </el-button>
        <!--表格-->
        <el-table
          :data="tableData"
          :row-class-name="tableRowClassName"
          @cell-mouse-enter="changestatistices"
          @cell-click="problemclick"
          size="medium"
        >
          <el-table-column prop="id" label="ID" :width="50"></el-table-column>
          <el-table-column prop="name" label="题名"></el-table-column>
          <el-table-column prop="level" label="难度" :width="100">
            <template slot-scope="scope1">
              <el-tag
                id="leveltag"
                size="medium"
                :type="problemlevel(scope1.row.level)"
                disable-transitions
                hit
                >{{ scope1.row.level }}</el-tag
              >
            </template>
          </el-table-column>
          <el-table-column
            prop="rate"
            label="通过 / 提交"
            :width="100"
          ></el-table-column>
          <el-table-column prop="tags" label="Tag">
            <template slot-scope="scope">
              <el-tag
                id="protag"
                v-for="(name, index) in scope.row.tags"
                :key="index"
                size="medium"
                disable-transitions
                hit
                >{{ name }}</el-tag
              >
            </template>
          </el-table-column>
          <el-table-column
            prop="total_grade"
            label="总分"
            :width="70"
          ></el-table-column>
        </el-table>
        <!--下方选页-->
        <el-row> &nbsp; </el-row>
        <center>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentpage"
            :page-sizes="[15, 20, 30, 50]"
            :page-size="pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalproblem"
          ></el-pagination>
        </center>
      </el-col>
      <!--右侧栏-->
      <!-- <el-col :span="6"> -->
      <!--Statistics-->
      <!-- <el-row :gutter="15">
        <el-col>
          <prostatistice ref="prosta"></prostatistice>
        </el-col>
      </el-row> -->
      <!--搜索框-->
      <!-- <el-row>
        <el-card shadow="always">
          <el-input placeholder="Search..."
                    v-model="searchtext"
                    @keyup.native.enter="searchtitle">
            <el-button slot="append"
                       icon="el-icon-search"
                       @click="searchtitle"></el-button>
          </el-input>
        </el-card>
      </el-row> -->
      <!--tag filter-->
      <!-- <el-row :gutter="15">
        <el-col>
          <el-card shadow="always">
            <h4>Tags (Click to filter)</h4>
            <el-button id="tag"
                       v-for="(name,index) in tagnames"
                       :key="index"
                       size="mini"
                       @click="tagclick(name)"
                       :ref="name">{{ name }}</el-button>
          </el-card>
        </el-col>
      </el-row> -->
      <!-- </el-col> -->
    </el-row>
    <el-dialog title="添加题目" :visible.sync="addProblemDialog" width="60%">
      <el-row>
        <el-col :offset="2" :span="9" style="text-align: center">
          <el-button
            type="success"
            size="medium"
            class="choice"
            plain
            @click="openCombGuide"
            ><i class="el-icon-guide" style="font-size: 40pt"></i
            ><br /><br />组合逻辑向导</el-button
          >
          快速创建题目，适合判断组合逻辑电路
        </el-col>
        <el-col :offset="2" :span="9" style="text-align: center">
          <el-button
            type="primary"
            size="medium"
            class="choice"
            plain
            @click="openEditor"
          >
            <i class="el-icon-edit-outline" style="font-size: 40pt"></i
            ><br /><br />
            打开编辑器
          </el-button>
          使用编辑器，适用于复杂的判题条件
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
//prostatistice;
// import prostatistice from "@/components/utils/prostatistice";
export default {
  components: {
    // prostatistice
  },
  data() {
    return {
      currentpage: 1,
      pagesize: 15,
      totalproblem: 10,
      tableData: [],
      tagnames: [
        "ALU",
        "decoder",
        "FIFO",
        "ip",
        "MUX",
        "sort",
        "testbench",
        "tutorial",
        "VGA",
        "门级",
        "RTL级",
        "行为级",
        "七段数码管",
        "寄存器堆",
      ],
      ac: 100,
      mle: 100,
      tle: 100,
      rte: 100,
      pe: 100,
      ce: 100,
      wa: 100,
      se: 100,
      title: "Statistics",
      currenttag: "",
      searchtext: "",
      addProblemDialog: false,
    };
  },
  methods: {
    openCombGuide() {
      console.log("pushed");
    },
    // 重新获取题目列表信息
    refresh() {
      this.$axios
        .get(
          "/problems/?limit=" +
            this.pagesize +
            "&offset=" +
            (this.currentpage - 1) * this.pagesize +
            "&search=" +
            this.searchtext
        )
        .then((response) => {
          for (var i = 0; i < response.data.length; i++) {
            // mapping = {
            //   1: "Easy",
            //   2: "Medium",
            //   3: "Hard",
            //   4: "VeryHard",
            //   5: "ExtremelyHard"
            // };
            // response.data[i].level = mapping[response.data[i].level];

            if (response.data[i].level == "1") response.data[i].level = "Easy";
            if (response.data[i].level == "2")
              response.data[i].level = "Medium";
            if (response.data[i].level == "3") response.data[i].level = "Hard";
            if (response.data[i].level == "4")
              response.data[i].level = "VeryHard";
            if (response.data[i].level == "5")
              response.data[i].level = "ExtremelyHard";
            // response.data[i].level = "Easy";

            response.data[i].ac = response.data[i].ac_users.length;
            response.data[i].submitted =
              response.data[i].submitted_users.length;
            response.data[i].rate =
              response.data[i].ac + " / " + response.data[i].submitted;

            if (!response.data[i].tags) response.data[i].tags = ["无"];
            else response.data[i].tags = response.data[i].tags.split("|");
            // response.data[i].tags = ["无"];
          }

          this.tableData = response.data;
          this.totalproblem = response.data.length;
        })
        .catch((error) => {
          this.$message.error(
            "服务器错误：" + JSON.stringify(error.response.data)
          );
        });
    },
    newProblem() {
      this.addProblemDialog = true;
    },
    openEditor: function () {
      this.$router.push({
        name: "addproblem",
      });
    },
    searchtitle() {
      this.currentpage = 1;
      this.refresh();
    },
    tagclick(name) {
      if (this.currenttag.indexOf(name) >= 0) {
        this.$refs[name][0].type = "default";
        let li = this.currenttag.split("+");
        for (var i = 0; i < li.length; i++) {
          if (li[i] == name) {
            li.splice(i, 1);
            break;
          }
        }
        this.currenttag = li.join("+");
      } else {
        this.$refs[name][0].type = "primary";
        let li = this.currenttag.split("+");
        li.push(name);
        this.currenttag = li.join("+");
      }
      this.searchtext = this.currenttag;
      this.currentpage = 1;
      this.refresh();
    },
    handleSizeChange(val) {
      this.pagesize = val;
      this.refresh();
    },
    handleCurrentChange(val) {
      this.currentpage = val;
      this.refresh();
    },
    tableRowClassName({ row, rowIndex }) {
      var acpro = this.$store.state.acpro;
      if (acpro)
        if (acpro.indexOf(row.problem + "") != -1) {
          return "acrow";
        }
      return "";
    },
    problemlevel: function (type) {
      if (type == "Easy") return "info";
      if (type == "Medium") return "success";
      if (type == "Hard") return "";
      if (type == "VeryHard") return "warning";
      if (type == "ExtremelyHard") return "danger";
    },
    changestatistices: function (row, column, cell, event) {
      if (row.submission == 0) {
        this.ac = 0;
        this.mle = 0;
        this.tle = 0;
        this.rte = 0;
        this.pe = 0;
        this.ce = 0;
        this.wa = 0;
        this.se = 0;
      } else {
        this.ac = parseFloat(((row.ac * 100) / row.submission).toFixed(2));
        this.mle = parseFloat(((row.mle * 100) / row.submission).toFixed(2));
        this.tle = parseFloat(((row.tle * 100) / row.submission).toFixed(2));
        this.rte = parseFloat(((row.rte * 100) / row.submission).toFixed(2));
        this.pe = parseFloat(((row.pe * 100) / row.submission).toFixed(2));
        this.ce = parseFloat(((row.ce * 100) / row.submission).toFixed(2));
        this.wa = parseFloat(((row.wa * 100) / row.submission).toFixed(2));
        this.se = parseFloat(((row.se * 100) / row.submission).toFixed(2));
      }
      this.title = row.title;
      // this.$refs.prosta.setdata(this.$data);
    },
    problemclick: function (row, column, cell, event) {
      this.$router.push({
        name: "problemdetail",
        params: { problemid: row.id },
      });
    },
  },
  mounted() {
    this.refresh();

    // this.$axios.get("/problemtag/").then(response => {
    //   for (var i = 0; i < response.data.length; i++)
    //     this.tagnames.push(response.data[i]["tagname"]);
    // });
  },
};
</script>

<style scope>
#leveltag {
  text-align: center;
  font-weight: bold;
}
#protag {
  text-align: center;
  font-weight: bold;
  margin-right: 7px;
  margin-bottom: 7px;
}
#tag {
  text-align: center;
  font-weight: bold;
  margin-left: 2px;
  margin-bottom: 5px;
}
.el-row {
  margin-bottom: 20px;
}
.el-table .acrow {
  background: #c7ffb8;
}
.choice {
  width: 100%;
  padding: 40px;
  font-size: 12pt;
  margin-bottom: 20px;
}
</style>
