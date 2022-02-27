<template>
  <div>
    <el-row type="flex" justify="center">
      <el-col class="main-topic" :xs="24" :sm="20" :md="16" :lg="12" :xl="12">
        <el-row class="main-title">{{ title }}</el-row>
        <el-row class="topic-info">
          <div>
            <userhyperlink
              style="display: inline"
              :userID="creator_id"
            ></userhyperlink
            >:
            <el-button @click="discussForum" type="text"
              >{{ problem }} 讨论区</el-button
            >
          </div>

          <div>创建时间 {{ createtime }}</div>
          <div>更新时间 {{ updatetime }}</div>
        </el-row>
        <el-row>
          <markdownIt :mdSource="description"></markdownIt>
        </el-row>

        <!-- 渲染每一条评论 -->
        <template v-for="(comment, i) in comments">
          <div :key="comment.id" class="comment" :id="`comment_floor_${i + 1}`">
            <el-row class="comment-info">
              <el-button
                @click="commentReplyer(comment.user_belong.id)"
                type="text"
                >{{ comment.user_belong.username }}</el-button
              >
              : {{ comment.update_time }} #{{ i + 1 }}
              <el-button type="text" class="reply-to" @click="replyTo(i)"
                >点击回复</el-button
              >
            </el-row>

            <!-- 这条评论有父评论 -->
            <el-row v-if="comment.parent_floor"
              ><el-link @click="goAnchor(comment.parent_floor)" type="primary"
                >回复 #{{ comment.parent_floor }}</el-link
              >
            </el-row>
            <el-row v-if="comment.parent_floor" class="quote-comment">
              <markdownIt
                :mdSource="
                  commentCutter(comments[comment.parent_floor - 1].text)
                "
              ></markdownIt>
            </el-row>

            <!-- 评论内容 -->
            <el-row>
              <markdownIt :mdSource="comment.text"></markdownIt>
            </el-row>
          </div>
        </template>
        <el-card shadow="never" style="margin-top: 20px">
          <!--提交界面-->
          <el-row :gutter="15">
            <i style="padding: 5px 10px" class="el-icon-edit"></i>
            <div
              id="comment-edit"
              style="display: inline-block; font-size: 20px"
            >
              评论编辑 (支持 markdown)
            </div>

            <div v-if="!loggedIn" style="display: inline-block; float: right">
              <el-tooltip
                class="item"
                effect="dark"
                content="登陆以进行提交"
                placement="top"
              >
              </el-tooltip>
            </div>
            <div style="display: inline-block; float: right" v-else>
              <el-button
                type="success"
                size="medium"
                @click="submitComment"
                style="font-weight: bold; margin-right: 10px; float: right"
                >提交</el-button
              >
              <el-button
                type="danger"
                size="medium"
                @click="commentText = ''"
                style="font-weight: bold; margin-right: 10px; float: right"
                >清空</el-button
              >
              <el-checkbox v-model="is_reply">回复楼层</el-checkbox>
              <el-input-number
                v-model="reply_to_floor"
                :min="1"
                label="回复楼层"
              ></el-input-number>
            </div>
          </el-row>

          <!--评论编辑-->
          <markdowneditor v-model="commentText"></markdowneditor>
        </el-card>
      </el-col>
    </el-row>

    <el-row> &nbsp; </el-row>
  </div>
</template>

<style scope>
.el-tag {
  text-align: center;
  font-weight: bold;
}

.main-topic,
.comment,
.add-comment {
  margin-top: 15px;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}

.main-topic pre {
  border-left: 6px solid #606266;
  padding-left: 24px;
  margin: 12px 0;
}

.main-topic code {
  line-height: 1.5em;
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

.quote-comment {
  color: #646464;
  margin: 10px 0;
  padding: 0 10px 0 15px;
  border-left: 3px solid #ccc;
}

.reply-to {
  color: #909399;
  float: right;
}
</style>

<script>
import moment from "moment";
import { mapState } from "vuex";

import markdownIt from "@/components/utils/markdownIt";
import markdowneditor from "@/components/utils/markdowneditor";
import userhyperlink from "@/components/utils/userhyperlink";

export default {
  name: "topic",
  components: {
    markdownIt,
    markdowneditor,
    userhyperlink,
  },
  methods: {
    getTopic() {
      let url = "/topic/" + this.id;
      this.$axios.get(url).then((response) => {
        this.creator_id = response.data.user_belong.id;
        this.problem = response.data.problem_belong.name;
        this.problem_id = response.data.problem_belong.id;
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

    commentReplyer: function (user_id) {
      this.$router.push({
        name: "user",
        params: { userid: user_id },
      });
    },

    discussForum: function () {
      this.$router.push({
        name: "discussion",
        params: { problemid: this.problem_id },
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

    commentCutter(s) {
      // 如果长度大于 200，则取前 200 字符，并添加省略号
      if (s.length > 200) {
        s = s.substr(0, 200) + " ......";
      }
      return s;
    },

    replyTo(i) {
      this.reply_to_floor = i + 1;
      this.is_reply = true;
      document.querySelector("#comment-edit").scrollIntoView({
        behavior: "smooth",
      });
    },

    goAnchor(id) {
      const selector = `#comment_floor_${id}`;
      document.querySelector(selector).scrollIntoView({
        behavior: "smooth",
      });
    },

    submitComment: function () {
      if (!this.loggedIn) {
        this.$message.error("请先登录！");
        return;
      }

      if (!this.commentText) {
        this.$message.error("请输入评论！");
        return;
      }

      this.$confirm("确定提交吗？", "提交", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$message({
            type: "success",
            message: "提交中...",
          });

          if (this.is_reply) {
            return this.$axios.post("/addcomment", {
              topic: this.id,
              text: this.commentText,
              parent: this.comments[this.reply_to_floor - 1].id,
            });
          }
          return this.$axios.post("/addcomment", {
            topic: this.id,
            text: this.commentText,
          });
        })
        .then((response) => {
          this.getComments();
          this.commentText = "";
        })
        .catch((error) => {
          this.$message.error(
            "提交失败：" + JSON.stringify(error.response.data)
          );
        });
    },
  },
  data() {
    return {
      id: null,
      problem: "",
      problem_id: "",
      creator_id: "",
      title: "",
      description: "",
      createtime: "",
      updatetime: "",

      comments: [],
      reply_to_floor: 1,
      is_reply: false,

      commentText: "",
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
