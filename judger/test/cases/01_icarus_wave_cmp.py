problem_file = '''
module decoder_3to8_dataflow(
    input [2:0] x,
    output reg [7:0] y
    );
    always @ (*) begin
        case (x)
        3'b000: y=8'b0000_0001;
        3'b001: y=8'b0000_0010;
        3'b010: y=8'b0000_0100;
        3'b011: y=8'b0000_1000;
        3'b100: y=8'b0001_0000;
        3'b101: y=8'b0010_0000;
        3'b110: y=8'b0100_0000;
        3'b111: y=8'b1000_0000;
        endcase
    end
endmodule
'''

submit_file = '''
module decoder_3to8_dataflow(
    input [2:0] x,
    output reg [7:0] y
    );
    always @ (*) begin
        case (x)
        3'b000: y=8'b0000_0001;
        3'b001: y=8'b0000_0010;
        3'b010: y=8'b0000_0100;
        3'b011: y=8'b0000_1000;
        3'b100: y=8'b0001_0000;
        3'b101: y=8'b0010_0000;
        3'b110: y=8'b0100_0000;
        3'b111: y=8'b1000_0000;
        endcase
    end
endmodule
'''

testcase_file_main = '''#!/bin/bash
'''

config = {
    'submission_detail': {
        'id': 0,
        'problem': {
            'id': 0,
            'problem_files': [
                {'uuid': "111"}
            ],
            'testcase_id': testcase_id
        },
        'user': {
            'id': 0,
            'student_id': "PB17000232"
        },
        'submit_time': "20101001",
        'submit_files': [
            {'uuid': "222"}
        ],
        'testcase_files': [
            {'uuid': "333"}
        ]
    },
    'file_map': {
        '111': '''''',
        '222': 
    }
}