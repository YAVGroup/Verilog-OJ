module testbench();
    reg [2:0] x;
    wire [7:0] y;
    decoder DUT(x, y);

    // http://www.referencedesigner.com/tutorials/verilog/verilog_62.php
    initial begin
        $dumpfile("out.vcd");
        // This will dump all signal, which may not be useful
        //$dumpvars;

        // dumping only this module
        //$dumpvars(1, testbench);

        // dumping only these variable
        // the first number (level) is actually useless
        $dumpvars(0, x, y);
    end

    integer i;
    initial begin
        for (i = 0; i < 8; i = i + 1) begin
            #1 x = i;
        end
    end

endmodule