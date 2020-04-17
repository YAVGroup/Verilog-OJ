`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB
// Engineer: Huang Yifan (hyf15@mail.ustc.edu.cn)
//
// Design Name: RV32I Core
// Module Name: Parameters
// Tool Versions: Vivado 2017.4.1
// Description: Const Parameters
//
//////////////////////////////////////////////////////////////////////////////////

// 功能说明
    // 为了代码可读性，定义了常量值
// 实验要求
    // 无需修改

`ifndef CONST_VALUES
`define CONST_VALUES
// ALU_func[3:0]
    `define ADD   4'd3
    `define AND   4'd7
    `define CSRRC 4'd14
    `define EMPTY 4'd15
    `define LUI   4'd10
    `define OR    4'd6
    `define SLL   4'd0
    `define SLT   4'd8
    `define SLTU  4'd9
    `define SRA   4'd2
    `define SRL   4'd1
    `define SUB   4'd4
    `define XOR   4'd5

// br_type[2:0]
    `define BEQ       3'd1
    `define BGE       3'd5
    `define BGEU      3'd6
    `define BLT       3'd3
    `define BLTU      3'd4
    `define BNE       3'd2
    `define NOBRANCH  3'd0

// imm_type[2:0]
    `define BTYPE  3'd3
    `define ITYPE  3'd1
    `define JTYPE  3'd5
    `define RTYPE  3'd0
    `define STYPE  3'd2
    `define UTYPE  3'd4

// load_type[2:0]  six kind of ways to save values to Register
    `define LB          3'd1	//	load 8bit from Mem then signed extended to 32bit
    `define LBU         3'd4	//	load 8bit from Mem then unsigned extended to 32bit
    `define LH          3'd2	//	load 16bit from Mem then signed extended to 32bit
    `define LHU         3'd5    //	load 16bit from Mem then unsigned extended to 32bit
    `define LW          3'd3	//	write 32bit to Register
    `define NOREGWRITE  3'b0	//	Do not write Register

// OPCODE const list
    `define OPCODE_ADD   3'b000
    `define OPCODE_AND   3'b111
    `define OPCODE_OR    3'b110
    `define OPCODE_SLL   3'b001
    `define OPCODE_SLT   3'b010
    `define OPCODE_SLTU  3'b011
    `define OPCODE_SR    3'b101
    `define OPCODE_XOR   3'b100

    `define OPCODE_BEQ   3'b000
    `define OPCODE_BGE   3'b101
    `define OPCODE_BGEU  3'b111
    `define OPCODE_BLT   3'b100
    `define OPCODE_BLTU  3'b110
    `define OPCODE_BNE   3'b001

    `define OPCODE_BYTE  3'b000
    `define OPCODE_HIGH  3'b001
    `define OPCODE_UBYTE 3'b100
    `define OPCODE_UHIGH 3'b101
    `define OPCODE_WORD  3'b010

    `define OPCODE_CSRRC  3'b011
    `define OPCODE_CSRRCI 3'b111
    `define OPCODE_CSRRS  3'b010
    `define OPCODE_CSRRSI 3'b110
    `define OPCODE_CSRRW  3'b001
    `define OPCODE_CSRRWI 3'b101
`endif

