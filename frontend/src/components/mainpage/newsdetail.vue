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
        <el-row class="main-title">
          {{ newsTitle }}
        </el-row>

        <el-row>
          <div style="white-space: pre-wrap;">
            {{ newsContent }}
          </div>
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
  text-align: center;
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

export default {
  name: "newsdetail",
  methods: {
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
  },
  data () {
    return {
      newsID: 0,
      newsTitle: "Loading..",
      newsCreateTime: new Date(),
      newsContent: "Loading.."
    }
  },
  computed: {
    submitTimePretty : function () {
      let tm = this.newsCreateTime;
      return this.prettyDate(tm.toISOString());
    }
  },
  destroyed () {
  },
  created () {
    this.newsID = this.$route.params.newsid;
    this.$axios.get('/news/' + this.newsID + '/').then(response => {
      // console.log(response.data);
      this.newsTitle = response.data.title;
      this.newsCreateTime = new Date(response.data.create_time);
      this.newsContent = response.data.content;
    })
  }
};
</script>
