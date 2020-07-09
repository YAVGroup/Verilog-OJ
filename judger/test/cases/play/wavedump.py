#!/usr/bin/env python3

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
            
            if not 'children' in cur.keys():
                raise VcdSignalTraversalError("{} have no children while traversing {}".format(
                    cur['name'], signal_path))
            
            try:
                cur = cur['children'][components[i+1]]
            except KeyError as e:
                raise VcdSignalTraversalError("{} have no children called {} while traversing {} (e: {})".format(
                    cur['name'], components[i+1], signal_path, e))

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

if __name__ == "__main__":
    cmpr = VcdComparator("./out.vcd", "", [''])