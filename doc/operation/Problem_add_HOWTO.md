# Verilog OJ 系统出题指南

> 本指南适用于 git revision 85b71a9 (截至 2020/10/2 的最新版本），后续更新将会反映在 Changelog 中

## CHANGELOG

- v1.0 第一版指南发布

## 综述

Verilog OJ 的题目保存在 Django 的 problem 模型中，目前主要以出题者编写 Yaml 并导入的方法来构造题目，之后可能会加入更多提升易用性的功能。

题目的信息在 problem 和 testcase 中保存，一个 problem 可以引用多个 testcase，这些 testcase 的先后顺序将以 testcase 本身的 id 决定。

problem 和 testcase 都会引用一定数量的文件。在判题时，判题机会先准备好如下的目录树：

```
/problem/*    题目中所有的 judge_files
/testcase/*   本 testcase 中所有的 files
/submit/*     用户提交的所有 files
```

其中每个 testcase 都会作为一个独立的判题任务传送给判题机。

submit 中保存着用户提交的文件，对于现在的版本而言，用户只能提交一个名为 code.v 的文件，其内容就是用户在 Verilog OJ 的代码编辑框中编辑的内容。

### Yaml 提交入口

现在 Yaml 提交还只能通过 Django admin 进行。您可以用管理员账号登陆 `http://202.38.75.113/admin-django/` 并且在 problem 选项卡中找到 Yaml 导入的相关设定。在框中粘贴您的 Yaml，并点击提交即可。

### 一个简单的 Yaml 描述的题目

在阅读此段落前，可以考虑先阅读 [3-8 Decoder 的 Yaml 导入文件](https://github.com/lluckydog/Verilog-OJ/blob/ad8232c2e182b4eb7150b9a3a4b285992c796eef/assets/decoder_38.yml) 作为起手。

Yaml 中的 `app_data` 字段为传递给 OJ 中 Sample Waveform 的 WaveJSON 数据。WaveJSON 的相关信息可以从 WaveDrom 项目处寻得。此处需要注意所有字符串字面值必须用双引号括起来（""），否则即使在 WaveDrom 的编辑器中可以渲染的字符串在这里也可能会出现问题。

> 当出现问题时，前端会显示 “Sorry, no waveform available”，同时在控制台打出报错信息。控制台即按 F12 打开的审查元素界面中的 Console。

Yaml 的 testcases 对应着测试点信息。其中 `main.sh` 会被判题机在按目录树下载好文件后运行。运行的目录为包含 testcase 文件夹的那个目录（下面简称 `/`）。

当判题结束时，main.sh 应该返回 0 作为正常退出的标志。同时，还应放置如下文件：

- `/score.txt`，其中包含本测试所获得分，介于 0 和测试点总分数之间
- `/possible_error.txt`，其中包含可能的错误
  - 如果没有错误，里面应为 `NONE`
  - 出现编译（由于 Verilog 语法错误，而使得解析器无法正常解析）错误，里面应为 `CE`
  - 编译无错但运行的结果和答案不一致，里面应为 `WA`
- `/app_data.txt`，其中包含本测试点所需要输出的波形（WaveJSON 格式，将被显示在本提交的本测试点测试详情中）

测试脚本的 stdout 和 stderr 将会被记录，并且作为测试点的 log_data 提交给后端，最终用户可以在后端一并看到这些内容。

### 波形比较设施

判题机上安装了 libreliu 魔改的 pyDigitalWaveTools 的 0.5 版本（[链接在此](https://github.com/libreliu/pyDigitalWaveTools)）。此版本和最新的 pip 直接安装的 pyDigitalWaveTools 有少许不兼容之处，建议如果使用的话，clone 此版本到本地后用 `pip install -e .` 安装之。

我们编写的几个题目，其判题都使用了如下模式：
1. 用 testbench.v 在 iverilog 上仿真一遍出题者编写的 code_ref.v，得到 vcd 波形文件输出 out_ref.vcd
2. 用 testbench.v 在 iverilog 上仿真一遍做题者编写的 code.v，得到 vcd 波形文件输出 out_dut.vcd
3. 用基于 pyDigitalWaveTools 编写的 Python 比较脚本比较两个波形中某些信号是否一致，如果不一致返回 1，一致返回 0
   并且根据此信息，进行本题答案赋分
4. 用 vcd_visualize.py 将 vcd 的某些信号转换为 WaveJSON 放入 app_data.txt 中，以供用户参考

您在本系统出自己的题目时，也可以参照此模式。
