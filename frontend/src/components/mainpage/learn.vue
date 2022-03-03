<template>
  <div>
    <el-row> &nbsp; </el-row>
    <el-row>
      <el-col :xs="0" :sm="2" :md="4" :lg="6" :xl="6" class="placeholder">
        <!-- placeholder only -->
        &nbsp;
      </el-col>
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <el-row>
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
        </el-row>

        <el-row>
          <el-card shadow="never" v-if="books.length == 0">目前尚无可学习的题目集。</el-card>

          <el-col
            :span="6"
            v-for="book in books"
            :key="book.id">
            <el-card
              shadow="never"
              >{{ book.name }}</el-card>
          </el-col>
          
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
