<template>
  <div class="tag-group">
    <div v-if="tagEmpty">
      {{ emptyHint }}
    </div>
    <div v-else>
      <el-tag
        v-for="(item, index) in tagSplit"
        :key="index"
        :type="item"
        effect="plain"
        size="medium"
        style="margin: 2px;"
        @click="handleTagClick(item)">
        {{ item }}
      </el-tag>
    </div>
  </div>
</template>

<script>
export default {
  name: "taglist",
  props: {
    tags: {
      type: [String],
      default: ""
    },
    emptyHint: {
      type: [String],
      default: "无"
    }
  },
  data () {
    return {
      
    }
  },
  methods: {
    handleTagClick: function (tagName) {
      // console.log(tagName);
      this.$emit('tagClicked', tagName);
    },
    goToUser: function (index) {
      this.$router.push({
        name: "user",
        params: { userid: this.userID }
      });
    }
  },
  computed: {
    tagSplit: function () {
      if (this.tags != "")
        return this.tags.split("|");
      else
        return ["无"];
    },
    tagEmpty: function () {
      return this.tags == "";
    }
  }
};
</script>

<style scoped>

</style>
