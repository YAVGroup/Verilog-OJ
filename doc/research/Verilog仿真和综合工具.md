# Verilog仿真和综合工具的调查

​																																						——by 丁伯尧 张灏文

## 综合

使用工具yosys对Verilog代码文件进行综合。

#### 安装

```bash
sudo apt-get install yosys

# 如果无法运行，可能需要安装的依赖如下
sudo apt-get install build-essential clang bison flex \
	libreadline-dev gawk tcl-dev libffi-dev git \
	graphviz xdot pkg-config python3 libboost-system-dev \
	libboost-python-dev libboost-filesystem-dev zlib1g-dev
```

#### 使用

```bash
# 你需要如下指令来进行对Verilog代码的综合
yosys

yosys> read_verilog YOUR_MODULE.v
yosys> synth -top YOUR_TOP_MODULE
```

## 仿真

使用iverilog和gktwave进行波形仿真

#### 安装

```bash
sudo apt-get install iverilog
sudo apt-get install gtkwave
```

#### 使用

在使用iverilog进行仿真之前，需要在仿真文件中加入如下语句：

```verilog
initial
begin            
    $dumpfile("wave.vcd");        	//生成的vcd文件名称
    $dumpvars(0, DUT);    			//tb模块名称
end 
```

随后可以使用如下命令进行仿真

```bash
iverilog -o OUTPUT_FILE YOUR_tb.v YOUR_MODULE.v
vvp OUTPUT_FILE -vcd
gtkwave wave.vcd
```

注：vvp命令有几种参数，其特定如下

* -vcd  将wave dump format（波形镜像格式）设置成 vcd。默认参数。特点是生成文件大，但能最好的适应第三方工具

* -lxt,-lxt-speed,-lxt-space 将波形镜像格式设置成 lxt。顾名思义 lxt-speed拥有较高的执行与读取速度，lxt-space 占用较小的空间

* -lxt2 比lxt慢，但是比vcd快，比lxt节省空间。递增式写入，即可以一边仿真，一边读取波形数据，进行显示。
* -none 禁止一切波形镜像的生成，可以加快仿真速度

## 生成原理图

使用netlistsvg工具对综合后的verilog文件生成原理图

#### 安装

```bash
# 需要先安装npm
sudo apt-get install npm

# 安装netlistsvg
npm install -g netlistsvg
```

#### 使用

```bash
# 在使用yosys仿真之后，需要先生成json文件
yosys> write_json YOUR_JSON.json

# 随后使用该工具生成原理图
netlistsvg YOUR_JSON.json -o YOUR_PICTURE
```

