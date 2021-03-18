#!/usr/bin/env python3
import sys

def main():
    from pyDigitalWaveTools.vcd.parser import VcdParser
    from wavedump import VcdConverter
    from pyverilog.dataflow.dataflow_analyzer import VerilogDataflowAnalyzer

    filelist = ['./problem/code_ref.v']

    topmodule = 'top_module'
    noreorder = False
    nobind = False
    include = None
    define = None

    analyzer = VerilogDataflowAnalyzer(filelist, topmodule,
                                      noreorder=noreorder,
                                      nobind=nobind,
                                      preprocess_include=include,
                                      preprocess_define=define)

    analyzer.generate()
    terms = analyzer.getTerms()

    input_list = []
    output_list = []
    compare_list = []

    for tk, tv in sorted(terms.items(), key=lambda x:str(x[0])):
      if 'Input' in tv.termtype:
        input_list.append('root/testbench/'+str(tk.scopechain[1]))

      if 'Output' in tv.termtype:
        output_list.append('root/testbench/'+str(tk.scopechain[1]))
        compare_list.append(str(tk.scopechain[1]))

    with open("./out_ref.vcd") as vcd_ref_file:
        vcd = VcdParser()
        vcd.parse(vcd_ref_file)
        data_ref = vcd.scope.toJson()

    with open("./out_code.vcd") as vcd_dut_file:
        vcd = VcdParser()
        vcd.parse(vcd_dut_file)
        data_dut = vcd.scope.toJson()

    vc_ref = VcdConverter(data_ref)
    time = vc_ref.addToWaveJsonSeparate(signal_names=input_list+output_list, prefix = "reference_")

    vc_dut = VcdConverter(data_dut)
    vc_dut.addToWaveJsonSeparate_modify(signal_names=output_list, time_max=time,prefix= "your_")

    vc_ref.mergeWaveDict(vc_dut.emitWaveDict())

    vc_ref.addCompare(compare_list,"your_","reference_",1)

    out = vc_ref.emitWaveJson()

    with open("./appdata.txt", "w") as f:
        f.write(out)

main()
