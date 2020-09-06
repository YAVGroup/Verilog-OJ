<template>
  <div>
    <el-row class="home-title">
      <i class="el-icon-thumb"></i>
      快速搜索
    </el-row>

    <el-row>
      <el-col :offset="1" :span="22">
        <el-autocomplete  v-model="input" 
                          placeholder="输入题号，快速跳转"
                          prefix-icon="el-icon-search"
                          :fetch-suggestions="querySearch"
                          @keyup.enter.native="jumpToProblem(-1)"
                          @select="handleSelect"></el-autocomplete>
        
      </el-col>
    </el-row>

  </div>
</template>

<script>
export default {
  name: "probsearch",
  data() {
    return {
      input: '',
      problemLoaded: false,
      allProblems: [],
      lastSuggestions: [],
    };
  },
  methods:{
    jumpToProblem: function(problemID) {
      if (problemID == -1) {
        if (lastSuggestions.length >= 1) {
          problemID = lastSuggestions[0].id;
        } else {
          console.warn("Invalid choice in jumpToProblem()");
        }
      }
      let realID = this.allProblems[problemID].id;
      this.$router.push({
        name: "problemdetail",
        params: { problemid: realID }
      });
    },
    handleSelect: function(item) {
      this.jumpToProblem(item.id);
    },
    prettyName: function(i) {
      return String(this.allProblems[i].id) + " | " + this.allProblems[i].name;
    },
    getAdvice: function(prefix) {
      let ret = []
      if (prefix == "" ) {
        for (let i = 0; i < this.allProblems.length; i++) {
          ret = ret.concat({'value': this.prettyName(i), 'id': i});
        }
        this.lastSuggestions = ret;
        return ret;
      }

      for (let i = 0; i < this.allProblems.length; i++) {
        let suggestions = [
          String(this.allProblems[i].id),
          this.allProblems[i].name
        ]
        for (let j = 0; j < suggestions.length; j++) {
          if (suggestions[j].toLowerCase().indexOf(prefix.toLowerCase()) === 0) {
            ret = ret.concat({'value': this.prettyName(i), 'id': i});
            break;
          }
        }
      }
      this.lastSuggestions = ret;
      return ret;
    },
    querySearch: function(queryString, cb) {
      if (!this.problemLoaded) {
        this.$axios.get('/problems/').then(response => {
          // console.log(response.data)
          let allDataLen = response.data.length;
          for (let i = 0; i < allDataLen; i++) {
            this.allProblems[i] = {
              id: response.data[i].id,
              name: response.data[i].name
            };
          }
          this.problemLoaded = true;

          // return the advice
          cb(this.getAdvice(queryString));
        })
      } else {
        cb(this.getAdvice(queryString));
      }
    }
  }
};
</script>

<style scoped>

.news-item {
  /* background-color: #fafafb; */
  list-style: none;
  padding-left: 5px;
}

.news-item a:link, .news-item a:visited {
  color: #333;
  text-decoration: none;
}

.news-item a:hover {
  color: #333;
  text-decoration: underline;
}

.home-title {
  font-size: 20px;
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}

</style>