problem_file_content = b'''
module decoder(
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

submit_file_content = b'''
module decoder(
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

testcase_file_testbench_content = b'''
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
'''

testcase_file_wavedump_content = b'''#!/usr/bin/env python3

from pyDigitalWaveTools.vcd.parser import VcdParser

class VcdSignalTraversalError(Exception):
    pass

class VcdSignalComparationError(Exception):
    pass

class VcdComparator:
    def find_signal_inst(self, data_obj, signal_path):
        components = signal_path.split("/")
        cur = data_obj
        for i in range(0, len(components) - 1):
            if cur['name'] != components[i]:
                raise VcdSignalTraversalError("{} mismatch with {} while traversing {}".format(
                    cur['name'], components[i], signal_path))
            
            if not 'data' in cur.keys():
                raise VcdSignalTraversalError("{} have no data k-v pair while traversing {}".format(
                    cur['name'], signal_path))
            
            found = False
            for child in cur['data']:
                if child['name'] == components[i+1]:
                    found = True
                    cur = child
                    break
            
            if not found:
                raise VcdSignalTraversalError("{} have no children called {} while traversing {}".format(
                    cur['name'], components[i+1], signal_path))

        if cur['name'] != components[-1]:
            raise VcdSignalTraversalError("{} mismatch with {} while traversing {}".format(
                cur['name'], components[-1], signal_path))

        return cur

    def compare_signals(self, ref, ud):
        # compare width
        if ref['type']['width'] != ud['type']['width']:
            raise VcdSignalComparationError("Signal {} have different width between ref ({}) and ud ({})".format(
                ref['name'], ref['type']['width'], ud['type']['width']))
        
        # No need to compare sigType (reg/wire.. anything else?)

        # signal comparation
        # TODO: support for different types ('b0' with 'b000' or 'd0' or something...)
        
        # Since value change dump theoretically only generates data when changes
        # so direct diffing should work
        for i, val in enumerate(ref['data']):
            if ud['data'][i] != val:
                raise VcdSignalComparationError("Signal {} have difference on time {} (ref={}, ud={})".format(
                    ref['name'], val[0], val, ud['data'][i]))

    def dump_hierarchy(self, data_obj):
        # TODO: only dump names
        print(data_obj.toJSON())

    def __init__(self, vcd_ref, vcd_ut, signal_names):
        """Initialize signals for comparation
        vcd_ref: the reference vcd file
        vcd_ut: the vcd file under test
        signal_names: the signal for comparation, uses "/" to express hierarchy.
                 and the top module name shall also be included.
        """

        with open(vcd_ref) as vcd_ref_file:
            vcd = VcdParser()
            vcd.parse(vcd_ref_file)
            self.data_ref = vcd.scope.toJson()
            print(self.data_ref)

        with open(vcd_ut) as vcd_ut_file:
            vcd_ut = VcdParser()
            vcd_ut.parse(vcd_ut_file)
            self.data_ut = vcd_ut.scope.toJson()
            print(self.data_ut)

        # find all signals
        self.signals_ref = [self.find_signal_inst(self.data_ref, i) for i in signal_names]
        self.signals_ut = [self.find_signal_inst(self.data_ut, i) for i in signal_names]
    
    def compare(self):
        try:
            # compare all signals
            for i in range(0, len(self.signals_ref)):
                self.compare_signals(self.signals_ref[i], self.signals_ut[i])
            return (True, "No error")
        except VcdSignalComparationError as e:
            return (False, "{}".format(e))

'''

testcase_file_vcd_main_content = b'''#!/usr/bin/env python3
import sys

def main():

    from wavedump import VcdComparator
    cmpr = VcdComparator("./out_ref.vcd", "./out_dut.vcd", ['root/testbench/x', 'root/testbench/y'])
    ret, msg = cmpr.compare()
    return (ret, msg)

ret, msg = main()
print(msg)
print("Ret status: {}".format(ret))
sys.exit(0 if ret is True else 1)
'''

testcase_file_main_content = b'''#!/bin/bash
iverilog ./testcase/testbench.v ./problem/decoder_ref.v -o ref_run
vvp ref_run
mv out.vcd out_ref.vcd

iverilog ./testcase/testbench.v ./submit/decoder.v -o dut_run
vvp dut_run
mv out.vcd out_dut.vcd

python3 ./testcase/vcd_main.py         # This will compare out_ref.vcd and out_dut.vcd

if [ $? -ne 0 ]; then
  echo "0" > score.txt
else
  echo "1" > score.txt
fi
'''

config = {
    'submission_id': 0,
    'testcase_id': 0,
    'submission_detail': {
        'id': 0,
        'problem': {
            'id': 0,
            'problem_files': [
                {'uuid': "001"}             # decoder_ref.v
            ],
            'testcase_id': 0
        },
        'user': {
            'id': 0,
            'student_id': "PB17000232"
        },
        'submit_time': "20101001",
        'submit_files': [
            {'uuid': "002"}                 # decoder.v
        ],
        'testcase_files': [
            {'uuid': "003"},                # wavedump.py
            {'uuid': "004"},                # vcd_main.py
            {'uuid': "005"},                # main.sh
            {'uuid': "006"}                 # testbench.v
        ]
    },
    'file_map': {
        '001': {
            "filename": "decoder_ref.v",
            "content": problem_file_content
        },
        '002': {
            "filename": "decoder.v",
            "content": submit_file_content
        },
        '003': {
            "filename": "wavedump.py",
            "content": testcase_file_wavedump_content
        },
        '004': {
            "filename": "vcd_main.py",
            "content": testcase_file_vcd_main_content
        },
        '005': {
            "filename": "main.sh",
            "content": testcase_file_main_content
        },
        '006': {
            "filename": "testbench.v",
            "content": testcase_file_testbench_content
        }
    }
}