<template>
  <div>
    <el-input
      type="textarea"
      :rows="10"
      placeholder="请输入内容"
      :value="value"
      @input="$emit('input', $event)"
    >
    </el-input>
    <el-row style="text-align: right; margin-top: 10px">
      <el-button type="primary" @click="isPreview = !isPreview">预览</el-button>
    </el-row>
    <el-card v-if="isPreview"
      ><markdownIt :mdSource="value"></markdownIt
    ></el-card>
  </div>
</template>

<script>
import markdownIt from "@/components/utils/markdownIt";

export default {
  name: "markdowneditor",
  components: {
    markdownIt,
  },
  props: {
    value: String,
  },
  data() {
    return {
      isPreview: false,
    };
  },
  watch: {
    value(code) {
      if (code === "") {
        this.isPreview = false;
      }
    },
  },
};
</script>
