`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB
// Engineer: Huang Yifan (hyf15@mail.ustc.edu.cn)
//
// Design Name: RV32I Core
// Module Name: Immediate Extend
// Tool Versions: Vivado 2017.4.1
// Description: Immediate Extension Module
//
//////////////////////////////////////////////////////////////////////////////////

//  功能说明
    //  立即数拓展，将指令中的立即数部分拓展为完整立即数
// 输入
    // Inst              指令的[31:7]
    // ImmType           立即数类型
// 输出
    // imm               补全的立即数
// 实验要求
    // 补全模块

// After reading more about RISC-V documents, I think all the Imm-extend
// should be signed extensions.
`include "Parameters.v"
module ImmExtend(
    input wire [31:7] inst,
    input wire [2:0] imm_type,
    output reg [31:0] imm
    );

    always@(*)
    begin
        case(imm_type)
            `ITYPE: imm <= {{21{inst[31]}}, inst[30:20]};
            // TODO: complete left part
            // Parameters.v defines all immediate type
            `STYPE: imm <= {{21{inst[31]}}, inst[30:25], inst[11:7]};
            `BTYPE: imm <= {{21{inst[31]}}, inst[7], inst[30:25], inst[11:8], 1'b0};
            `UTYPE: imm <= {inst[31:12], {12{1'b0}}};
            `JTYPE: imm <= {{13{inst[31]}}, inst[19:12], inst[20], inst[30:21], 1'b0};
        endcase
    end

endmodule
