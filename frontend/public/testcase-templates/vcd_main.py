#!/usr/bin/env python3
import sys

def main():

    from wavedump import VcdComparator
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

    compare_list = []
    for tk, tv in sorted(terms.items(), key=lambda x:str(x[0])):
      if 'Input' in tv.termtype or 'Output' in tv.termtype: 
        compare_list.append('root/testbench/'+str(tk.scopechain[1]))

    print('compare list')
    print(compare_list)
    cmpr = VcdComparator("./out_ref.vcd", "./out_code.vcd", compare_list)
    ret, msg = cmpr.compare()
    return (ret, msg)

ret, msg = main()
print(msg)
print("Ret status: {}".format(ret))
sys.exit(0 if ret is True else 1)
