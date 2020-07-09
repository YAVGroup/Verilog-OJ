module decoder(
    input [2:0] x,
    output reg [7:0] y
    );
    integer i;
    always @ (*) begin
        for (i = 0; i < 8; i = i + 1) begin
            if (x == i[2:0]) begin
                y = 8'd0;
                y[i] = 1;
            end
        end
    end
endmodule