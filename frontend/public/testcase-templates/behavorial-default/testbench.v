module testbench();
    wire out;
    top_module DUT(out);
    // http://www.referencedesigner.com/tutorials/verilog/verilog_62.php
    initial begin
        $dumpfile("out.vcd");
        // This will dump all signal, which may not be useful
        //$dumpvars;
        // dumping only this module
        //$dumpvars(1, testbench);
        // dumping only these variable
        // the first number (level) is actually useless
        $dumpvars(0, out);
    end
    integer i;
    initial begin
        #1;
    end
endmodule