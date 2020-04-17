`include "Parameters.v"

module imm_test;

reg [31:0] inst;
reg [2:0] imm_type;
wire [31:0] imm;

ImmExtend imm_test_module(inst[31:7], imm_type, imm);

initial begin
    inst = 0;
    #3 $display("At time %t, value = %h (%8d)",$time, imm, $signed(imm));

    inst = 32'hFFC_60613;
    imm_type = `ITYPE;
    // -4
    #3 $display("At time %t, value = %h (%8d)",$time, imm, $signed(imm));

    inst = 32'b0000000_01010_10011_000_10000_1100011;
    imm_type = `BTYPE;
    // 16
    #3 $display("At time %t, value = %h (%8d)",$time, imm, $signed(imm));

    inst = 32'b0000000_01110_00010_010_01000_0100011;
    imm_type = `STYPE;
    // 8
    #3 $display("At time %t, value = %h (%8d)",$time, imm, $signed(imm));

    inst = 0;
    #3 $display("At time %t, value = %h (%8d)",$time, imm, $signed(imm));
end

endmodule
