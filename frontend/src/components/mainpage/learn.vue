<template>
  <div>
    <el-row> &nbsp; </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="4" :xl="4" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="16" :xl="16">
        <!-- 筛选器 TODO -->
        <!-- <el-row>
            <el-card shadow="never">
            <el-row>
                <h3 style="display: inline-block; margin: 3px 0px">
                题目页
                </h3>
            </el-row>
            <el-row>
                <div>
                本页面采取书籍形式进行题库中题目的组织，同时附有说明性文字介绍，以期为您的数字电路设计学习过程提供一些方便。
                </div>
            </el-row>
            </el-card>
        </el-row> -->

        <el-row>
          <el-card shadow="never" v-if="books.length == 0">目前尚无可学习的题目集。</el-card>

          <el-row v-for="rowIndex in Math.ceil(books.length / 3)" :key="rowIndex">
            <el-col :span="7" v-for="(book, index) in books.slice((rowIndex - 1) * 3, rowIndex * 3)" :key="book.id" :offset="index > 0 ? 1 : 0">
              <el-card :body-style="{ padding: '0px' }" style="margin-bottom: 20px;">
                <div style="padding: 14px;">
                    <el-popover
                      placement="bottom"
                      title="题目集简介"
                      width="200"
                      trigger="hover"
                      :content="book.description_short.length > 0 ? book.description_short : '暂无简介'">
                      <el-button type="text" style="font-size: 16px;" slot="reference">{{ book.name }}</el-button>
                    </el-popover>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "learn",
  data() {
    return {
      books: [],
    };
  },
  methods: {
    
  },
  created() {
    this.$axios.get("/problem-books/").then((response) => {
      this.books = response.data;
    });
  },
};
</script>

<style scoped>

</style>
