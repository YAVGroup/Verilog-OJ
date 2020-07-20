# Testcases for Verilog OJ Judger

## 简介

本文件夹为判题模块的测试框架。

`runner.py` 为运行、展开和折叠测试文件的脚本程序。

测试框架的基本原理是，Hook 掉判题模块和后端通信的环节，通过读取 `cases` 文件夹中的具体的测试样例的 `config` 字典得到所需要的和后端交互的所有信息（文件、编号等），同时将本应该上传的结果输出到 stdout。

为了方便调试，`runner.py` 的 `unfold` 功能可以将 `cases` 里面那些具体的测试样例的字典中存放的各个文件展开到一个文件夹去，方便编辑。

## 测试点一览

下面所说的各个文件，请自行用 `unfold` 功能展开到一个文件夹中，这样才能对得上号。

### ICarus 波形比较测试 (`icarus_test.py`)

通过比较标准 decoder 和用户编写的 decoder 在 iVerilog 仿真器的波形是否一致，来判断用户的得分。

其中用到的 `wavedump.py` 为基于 pyDigitalWaveTools 的 VCD 波形比较器，我对其进行了[修改](https://github.com/libreliu/pyDigitalWaveTools)，目前请先使用

```
git clone https://github.com/libreliu/pyDigitalWaveTools
cd pyDigitalWaveTools
pip install -e .
```

套餐进行安装，并请在使用的时候不要删除这个文件夹（`pyDigitalWaveTools`）。

如果用户的波形和标准波形正确（具体的说，这里要配置比较哪个波形，在 `vcd_main.py` 中有），那么就得 1 分，否则得 0 分。