# OpenTimer：静态时序分析工具

## 使用简介

### 示例

```bash
# 编译安装
git clone https://github.com/OpenTimer/OpenTimer.git
cd OpenTimer
mkdir build
cd build
cmake ../
make

# 安装结果测试
make test

# 使用
../bin/ot-shell
cd example/simple
read_celllib osu018_stdcells.lib
read_verilog simple.v
read_sdc simple.sdc
report_timing
```

### ot-shell 中其它常用命令:

| Command       | Type     | Arguments           | Description                                     | Example                     |
| ------------- | -------- | ------------------- | ----------------------------------------------- | --------------------------- |
| read_celllib  | builder  | [-min \| -max] file | read the cell library for early and late splits | read_celllib mylib.lib      |
| read_verilog  | builder  | file                | read the verilog netlist                        | read_verilog mynetlist.v    |
| read_sdc      | builder  | file                | read a Synopsys Design Constraint file          | read_sdc myrule.sdc         |
| read_spef     | builder  | file                | read parasitics in SPEF                         | read_spef myparasitics.spef |
| update_timing | action   | none                | update the timing                               | update_timing               |
| report_timing | action   | [-num_paths k]      | report the critical paths                       | report_timing -num_paths 10 |
| report_tns    | action   | none                | report the total negative slack                 | report_tns                  |
| report_wns    | action   | none                | report the worst negative slack                 | report_wns                  |
| dump_graph    | accessor | [-o file]           | dump the timing graph to a DOT format           | dump_graph                  |
| dump_timer    | accessor | [-o file]           | dump the design statistics                      | dump_timer                  |

dump_graph 可用于生成 DOT 格式图片：

![ot_dump_graph](assets/ot_dump_graph.png)

### 有关 .sdc 约束文件

目前只支持以下语法：

| Command              | Type              | Description                                                    |
| -------------------- | ----------------- | -------------------------------------------------------------- |
| set_input_delay      | timing constraint | sets input delay on an input port relative to a clock signal   |
| set_output_delay     | timing constraint | sets output delay on an output port relative to a clock signal |
| create_clock         | timing constraint | creates a clock and defines its waveform in the current design |
| set_input_transition | system interface  | sets a fixed transition time on an input port                  |
| set_load             | system interface  | sets the load capacitance value on an output port              |

### 有关 .v 文件

- OpenTimer reads *gate-level* (aka structural) verilog files (.v) to initialize circuit netlists. Logics are described by gates and modules only. There are no `always` blocks or `assign` statements.

  - 需要先转为门级电路

## 项目集成

可使用 cmake 将 OpenTimer 添加为 subproject。如下修改 CMakeLists：

```CMake
cmake_minimum_required (VERSION 3.9)                  # CMake minimum version
project(app)                                          # your OpenTimer application
add_subdirectory(OpenTimer)                           # add OpenTimer project
include_directories(${PROJECT_SOURCE_DIR}/OpenTimer)  # add OpenTimer include

set(CMAKE_CXX_STANDARD 17)                            # enable c++17
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Threads REQUIRED)                        # thread library (pthread)

add_executable(app app.cpp)                           # link to your app.cpp
target_link_libraries(app OpenTimer Threads::Threads stdc++fs)
```

## 开源协议

- Synopsys TAP-in 使用 Synopsys SDC License

- NanGate 45nm Library 使用 Nangate Open Cell Library License

- OpenTimer 核心代码及其它组件使用 MIT License

可供实验使用
