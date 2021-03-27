<template>
  <div>
    <el-row class="home-title">
      <i class="el-icon-s-comment"></i>
      通知公告
    </el-row>

    <el-row>
      <el-col :offset="1" :span="22">
        <ul class="news-item" :key="index" v-for="(item, index) in news">
          <li>
            <a @click="goToNews(item.id)">{{ item.title }}</a>
          </li>
        </ul>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "newsboard",
  data() {
    return {
      news: [],
    };
  },
  methods: {
    goToNews: function (index) {
      this.$router.push({
        name: "newsdetail",
        params: { newsid: index },
      });
    },
  },
  created() {
    this.$axios.get("/news/").then((response) => {
      this.news = response.data;
    });
  },
};
</script>

<style scoped>
.news-item {
  /* background-color: #fafafb; */
  list-style: none;
  padding-left: 5px;
  margin: 0px 0px 0px 0px;
}

.news-item a:link,
.news-item a:visited {
  color: #333;
  text-decoration: none;
}

.news-item a:hover {
  color: #333;
  text-decoration: underline;
}

.home-title {
  font-size: 20px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}
</style>
