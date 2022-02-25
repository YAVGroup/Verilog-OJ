<template>
  <div>
    <el-row type="flex" justify="center">
      <el-col class="main-topic" :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <el-row class="main-title">{{ title }}</el-row>
        <el-row class="topic-info">
          <el-button @click="topicCreator" type="text">{{ creator }}</el-button>
          : {{ updatetime }}
        </el-row>
        <el-row>
          <markdownIt :mdSource="description"></markdownIt>
        </el-row>
      </el-col>
    </el-row>
    <template v-for="(comment, i) in comments">
      <el-row :key="comment.id" type="flex" justify="center">
        <el-col
          class="comment"
          :xs="24"
          :sm="20"
          :md="16"
          :lg="12"
          :xl="12"
          :id="`comment_floor_${i + 1}`"
        >
          <el-row class="comment-info">
            <el-button
              @click="commentReplyer(comment.user_belong.id)"
              type="text"
              >{{ comment.user_belong.username }}</el-button
            >
            : {{ comment.update_time }} #{{ i + 1 }}
          </el-row>
          <el-row v-if="comment.parent_floor"
            >回复 #{{ comment.parent_floor }}
          </el-row>
          <el-row>
            <markdownIt :mdSource="comment.text"></markdownIt>
          </el-row>
        </el-col>
      </el-row>
    </template>
    <el-row> &nbsp; </el-row>
  </div>
</template>

<style scope>
.el-tag {
  text-align: center;
  font-weight: bold;
}

.main-topic,
.comment {
  margin-top: 15px;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}

.main-title {
  font-size: 20px;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

.topic-info,
.comment-info {
  font-size: 0.8em;
}
</style>

<script>
import moment from "moment";
import { mapState } from "vuex";

import markdownIt from "@/components/utils/markdownIt";

export default {
  name: "topic",
  components: {
    markdownIt,
  },
  methods: {
    getTopic() {
      let url = "/topic/" + this.id;
      this.$axios.get(url).then((response) => {
        this.creator = response.data.user_belong.username;
        this.creator_id = response.data.user_belong.id;
        this.title = response.data.title;
        this.description = response.data.description;
        this.createtime = moment(response.data.create_time).format(
          "YYYY-MM-DD HH:mm:ss"
        );
        this.updatetime = moment(response.data.update_time).format(
          "YYYY-MM-DD HH:mm:ss"
        );
      });
    },

    topicCreator: function () {
      this.$router.push({
        name: "user",
        params: { userid: this.creator_id },
      });
    },

    commentReplyer: function (user_id) {
      this.$router.push({
        name: "user",
        params: { userid: user_id },
      });
    },

    getComments() {
      let url = "/comment/?topic=" + this.id;
      this.$axios.get(url).then((response) => {
        const comment_ids = [];
        for (let i = 0; i < response.data.length; i++) {
          response.data[i].update_time = moment(
            response.data[i].update_time
          ).format("YYYY-MM-DD HH:mm:ss");
          comment_ids[response.data[i].id] = i + 1; // 这个 id 对应的本 topic 的楼层号
          if (response.data[i].parent) {
            response.data[i].parent_floor =
              comment_ids[response.data[i].parent];
          }
        }
        this.comments = response.data;
      });
    },
  },
  data() {
    return {
      id: null,
      creator: "",
      title: "",
      description: "",
      createtime: "",
      updatetime: "",
      isadmin: false,

      comments: [],
    };
  },
  computed: {
    ...mapState(["loggedIn", "userID", "username", "isSuperUser"]),
  },
  created() {
    this.id = this.$route.params.topicid;
    this.getTopic();
    this.getComments();
  },
};
</script>
