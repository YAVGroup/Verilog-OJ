<template>
  <div>
    <el-table :data="portInfo">
      <el-table-column label="端口名称" min-width="200px">
        <template slot-scope="scope">
          <el-input v-model="scope.row.name"></el-input>
        </template>
      </el-table-column>
      <el-table-column label="输入/输出" min-width="140px">
        <template slot-scope="scope">
          <el-switch
            active-text="output"
            inactive-text="input"
            v-model="scope.row.output"
          >
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column label="wire/reg" min-width="60px">
        <template slot-scope="scope">
          <el-checkbox v-model="scope.row.reg">reg</el-checkbox>
        </template>
      </el-table-column>
      <el-table-column label="位宽" min-width="260px">
        <template slot-scope="scope">
          <el-checkbox style="padding-right: 20px" v-model="scope.row.bus"
            >bus</el-checkbox
          >
          <el-input-number
            v-if="scope.row.bus"
            v-model="scope.row.busInfo.end"
            style="width: 80px"
            controls-position="right"
          ></el-input-number>
          <span
            v-if="scope.row.bus"
            style="padding-left: 5px; padding-right: 5px"
            >:</span
          >
          <el-input-number
            v-if="scope.row.bus"
            v-model="scope.row.busInfo.begin"
            style="width: 80px"
            controls-position="right"
          ></el-input-number>
        </template>
      </el-table-column>
      <el-table-column min-width="60px">
        <template>
          <el-button type="danger" icon="el-icon-delete" circle></el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-row>
      <el-col style="display: flex; justify-content: center">
        <el-button type="success" icon="el-icon-plus" round>添加端口</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      portInfo: [
        {
          name: "out",
          output: true,
          reg: true,
          bus: true,
          busInfo: {
            begin: 0,
            end: 1,
          },
        },
      ],
    };
  },
};
</script>
