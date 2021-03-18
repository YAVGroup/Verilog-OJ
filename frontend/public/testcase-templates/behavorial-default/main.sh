#!/bin/bash
iverilog ./testcase/testbench.v ./problem/code_ref.v -o ref_run
vvp ref_run
mv out.vcd out_ref.vcd

iverilog ./testcase/testbench.v ./submit/code.v -o code_run

if [ $? -ne 0 ]; then
  echo "CE" > possible_error.txt
  exit 1
fi

vvp code_run

if [ $? -ne 0 ]; then
  echo "CE" > possible_error.txt
  exit 1
fi

mv out.vcd out_code.vcd

python3 ./testcase/vcd_main.py         # This will compare out_ref.vcd and out_code.vcd

if [ $? -ne 0 ]; then
  echo "0" > score.txt
  echo "WA" > possible_error.txt
else
  echo "10" > score.txt
  echo "NONE" > possible_error.txt
fi

python3 ./testcase/vcd_visualize.py    # This will output app_data.txt