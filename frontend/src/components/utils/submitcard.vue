<template>
  <el-card shadow="never">
    <el-row :gutter="15">
      <i style="padding: 5px 10px" class="el-icon-edit"></i>
      <div style="display: inline-block; font-size: 20px">{{ title }}</div>

      <div v-if="!loggedIn" style="display: inline-block; float: right">
        <el-tooltip
          class="item"
          effect="dark"
          content="登陆以进行提交"
          placement="top"
        >
          <!-- https://github.com/ElemeFE/element/issues/8557 -->
          <div style="font-weight: bold; margin-right: 10px; float: right">
            <el-button type="success" size="medium" disabled>提交</el-button>
          </div>
        </el-tooltip>
        <el-button
          type="danger"
          size="medium"
          style="font-weight: bold; margin-right: 10px; float: right"
          >清空</el-button
        >
      </div>
      <div style="display: inline-block; float: right" v-else>
        <el-button
          type="success"
          size="medium"
          @click="$emit('submit')"
          style="font-weight: bold; margin-right: 10px; float: right"
          >提交</el-button
        >
        <el-button
          type="danger"
          size="medium"
          @click="$emit('clear')"
          style="font-weight: bold; margin-right: 10px; float: right"
          >清空</el-button
        >
      </div>
    </el-row>

    <slot></slot>
  </el-card>
</template>

<script>
export default {
  name: "submitcard",
  props: {
    title: String,
    loggedIn: Boolean,
  },
};
</script>
