#!/usr/bin/env python3

"""
Example signal:

{
    'name': 'root', 
    'type': {'name': 'struct'}, 
    'children': [
        {
            'name': 'testbench', 
            'type': {'name': 'struct'}, 
            'children': [
                {
                    'name': 'x', 
                    'type': {'width': 3, 'name': 'reg'}, 
                    'data': [
                        (0, 'bx'), (1, 'b0'), (2, 'b1'), (3, 'b10'), (4, 'b11'), (5, 'b100'), (6, 'b101'), (7, 'b110'), (8, 'b111')
                    ]
                }, 
                {
                    'name': 'y', 
                    'type': {
                        'width': 8, 
                        'name': 'wire'
                    }, 
                    'data': [
                        (0, 'bx'), (1, 'b1'), (2, 'b10'), (3, 'b100'), (4, 'b1000'), (5, 'b10000'), (6, 'b100000'), (7, 'b1000000'), (8, 'b10000000')
                    ]
                }
            ]
        }
    ]
}

"""


from pyDigitalWaveTools.vcd.parser import VcdParser

class VcdSignalTraversalError(Exception):
    pass

class VcdSignalComparationError(Exception):
    pass

def find_signal_inst(data_obj, signal_path):
    components = signal_path.split("/")
    cur = data_obj
    for i in range(0, len(components) - 1):
        if cur['name'] != components[i]:
            raise VcdSignalTraversalError("{} mismatch with {} while traversing {}".format(
                cur['name'], components[i], signal_path))

        if not 'children' in cur.keys():
            raise VcdSignalTraversalError("{} have no data k-v pair while traversing {}".format(
                cur['name'], signal_path))

        found = False
        for child in cur['children']:
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

class VcdComparator:

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
        self.signals_ref = [find_signal_inst(self.data_ref, i) for i in signal_names]
        self.signals_ut = [find_signal_inst(self.data_ut, i) for i in signal_names]

    def compare(self):
        try:
            # compare all signals
            for i in range(0, len(self.signals_ref)):
                self.compare_signals(self.signals_ref[i], self.signals_ut[i])
            return (True, "No error")
        except VcdSignalComparationError as e:
            return (False, "{}".format(e))

import json

class VcdSignalValueParseError(Exception):
    pass

class VcdConverter:

    def __init__(self, data_vcd):
        self.output = {'signal': []}
        self.data_vcd = data_vcd

    def emitWaveDict(self):
        return self.output

    def mergeWaveDict(self, wdict):
        self.output['signal'] += wdict['signal']

    def emitWaveJson(self):
        return json.dumps(self.output)

    def parseValue(self, val_str):
        """ Note: b111xx1 -> x """
        if val_str[0] == "b":
            if val_str.find("x") != -1:
                return "x"
            return int(val_str[1:], base=2)
        elif len(val_str) == 1:
            if val_str[0] == "x":
                return "x"
            else:
                return int(val_str, base=2)
        else:
            raise VcdSignalValueParseError("Unknown value type")

    def toBinRepr(self, val, width):
        if val == 'x':
            return 'x' * width

        striped = bin(val)[2:]
        assert(width >= len(striped))
        return "0" * (width - len(striped)) + striped

    def addToWaveJsonSeparate(self, signal_names, prefix=""):
        # find common time_max
        time_max = 0
        for signal_name in signal_names:
            sig_inst = find_signal_inst(self.data_vcd, signal_name)
            time_max = max(time_max, sig_inst['data'][-1][0])

        for signal_name in signal_names:
            sig_jsons = []
            sig_inst = find_signal_inst(self.data_vcd, signal_name)


            width = sig_inst['type']['width']
            # decompose
            for i in range(0, width):
                sig_jsons.append({})
                sig_jsons[i]['name'] = prefix + sig_inst['name'] + "[" + str(i) + "]"

            local_time_max = sig_inst['data'][-1][0]
            waves = ["" for i in range(0, width)]
            cur_step_ptr = 0

            # "x" or int or "SOME.."
            cur_wave = "SOMETHING_NEVER_HAPPEN"

            # TODO: Avoid multiple transitions at same timestep
            for i in range(0, local_time_max + 1):
                if sig_inst['data'][cur_step_ptr][0] > i:
                    # maintain current value
                    for i in range(0, width):
                        waves[i] += "."
                else:
                    new_wave = self.parseValue(sig_inst['data'][cur_step_ptr][1])
                    if new_wave == cur_wave:
                        waves[i] += "."
                    else:
                        # do bitwise comparation
                        if cur_wave == "SOMETHING_NEVER_HAPPEN":
                            # new_wave_bin[0] is MSB
                            new_wave_bin = self.toBinRepr(new_wave, width)
                            for i in range(0, width):
                                waves[i] += new_wave_bin[::-1][i]
                        else:
                            cur_wave_bin = self.toBinRepr(cur_wave, width)
                            new_wave_bin = self.toBinRepr(new_wave, width)

                            for i in range(0, width):
                                old = cur_wave_bin[::-1][i]
                                new = new_wave_bin[::-1][i]
                                if old != new:
                                    waves[i] += new
                                else:
                                    waves[i] += '.'

                        cur_wave = new_wave

                    cur_step_ptr += 1

            for i in range(local_time_max, time_max + 1):
                for i in range(0, width):
                    waves[i] += "."

            for i in range(0, width):
                sig_jsons[i]['wave'] = waves[i]


            self.output['signal'] += sig_jsons
      
        return time_max



    def addToWaveJsonSeparate_modify(self, signal_names, time_max, prefix=""):
        # find common time_max
        time_max = time_max

        for signal_name in signal_names:
            sig_jsons = []
            sig_inst = find_signal_inst(self.data_vcd, signal_name)


            width = sig_inst['type']['width']
            # decompose
            for i in range(0, width):
                sig_jsons.append({})
                sig_jsons[i]['name'] = prefix + sig_inst['name'] + "[" + str(i) + "]"

            local_time_max = sig_inst['data'][-1][0]
            waves = ["" for i in range(0, width)]
            cur_step_ptr = 0

            # "x" or int or "SOME.."
            cur_wave = "SOMETHING_NEVER_HAPPEN"

            # TODO: Avoid multiple transitions at same timestep
            for i in range(0, local_time_max + 1):
                if sig_inst['data'][cur_step_ptr][0] > i:
                    # maintain current value
                    for i in range(0, width):
                        waves[i] += "."
                else:
                    new_wave = self.parseValue(sig_inst['data'][cur_step_ptr][1])
                    if new_wave == cur_wave:
                        waves[i] += "."
                    else:
                        # do bitwise comparation
                        if cur_wave == "SOMETHING_NEVER_HAPPEN":
                            # new_wave_bin[0] is MSB
                            new_wave_bin = self.toBinRepr(new_wave, width)
                            for i in range(0, width):
                                waves[i] += new_wave_bin[::-1][i]
                        else:
                            cur_wave_bin = self.toBinRepr(cur_wave, width)
                            new_wave_bin = self.toBinRepr(new_wave, width)

                            for i in range(0, width):
                                old = cur_wave_bin[::-1][i]
                                new = new_wave_bin[::-1][i]
                                if old != new:
                                    waves[i] += new
                                else:
                                    waves[i] += '.'

                        cur_wave = new_wave

                    cur_step_ptr += 1

            for i in range(local_time_max, time_max + 1):
                for i in range(0, width):
                    waves[i] += "."

            for i in range(0, width):
                sig_jsons[i]['wave'] = waves[i]


            self.output['signal'] += sig_jsons
      

    def addToWaveJsonAggregated(self, signal_names, prefix=""):
        """ Aggregated view, which uses '=' on every timeslice. """
        # find common time_max
        time_max = 0
        for signal_name in signal_names:
            sig_inst = find_signal_inst(self.data_vcd, signal_name)
            time_max = max(time_max, sig_inst['data'][-1][0])

        for signal_name in signal_names:
            sig_json = {}
            sig_inst = find_signal_inst(self.data_vcd, signal_name)
            sig_json['name'] = prefix + sig_inst['name']

            # [0, time_max]
            local_time_max = sig_inst['data'][-1][0]
            wave = ""
            cur_step_ptr = 0
            cur_wave = "SOMETHING_NEVER_HAPPEN"
            data = []

            # TODO: Avoid multiple transitions at same timestep
            for i in range(0, local_time_max + 1):
                if sig_inst['data'][cur_step_ptr][0] > i:
                    # maintain current value
                    wave += "."
                else:
                    new_wave = self.parseValue(sig_inst['data'][cur_step_ptr][1])
                    if new_wave == cur_wave:
                        wave += "."
                    else:
                        wave += "="
                        data.append(new_wave)
                        cur_wave = new_wave

                    cur_step_ptr += 1

            for i in range(local_time_max, time_max + 1):
                wave += "."

            sig_json['wave'] = wave
            sig_json['data'] = data

            self.output['signal'].append(sig_json)

    def addCompare(self,signal_names,prefix1,prefix2,width):
        #have to be the same length and width

        for signal_name in signal_names:

            signal1 = prefix1 + signal_name
            signal2 = prefix2 + signal_name

            for j in range(width):
                name1 = signal1 +'['+str(j) +']' 
                get1 = ""
                wave1 = ""
                name2 = signal2 +'['+str(j) +']' 
                get2 = ""
                wave2 = ""

                for each in self.output['signal']:
                    if each['name'] == name1:
                        get1 = each['wave']
                    if each['name'] == name2:
                        get2 = each['wave']

                temp1 = list(get1)
                temp2 = list(get2)
                for i in range(len(get1)):
                    if temp1[i] == '.':
                        wave1 += wave1[i-1]
                    else:
                        wave1 += temp1[i]
                
                    if temp2[i] == '.':
                        wave2 += wave2[i-1]
                    else:
                        wave2 += temp2[i]

                sig_json = {}
                sig_json['name'] = "missmatch_" + signal_name + '[' + str(j) + ']'
                wave = ""
                get = ""
                for i in range(len(wave1)):
                    if wave1[i]==wave2[i]:
                        if get == "0":
                            wave += "." 
                            get = "0"
                        else:
                            wave += "0"
                            get = "0"
                    else:
                        if get == "1":
                            wave+= "."
                            get = "1"
                        else:
                            wave+= "."
                            get = "1"
                sig_json['wave'] = wave
                self.output['signal'].append(sig_json)



if __name__ == "__main__":
    sample_vcd = {'name': 'root', 'type': {'name': 'struct'}, 'children': [{'name': 'testbench', 'type': {'name': 'struct'}, 'children': [{'name': 'x', 'type': {'width': 3, 'name': 'reg'}, 'data': [(0, 'bx'), (1, 'b0'), (2, 'b1'), (3, 'b10'), (4, 'b11'), (5, 'b100'), (6, 'b101'), (7, 'b110'), (8, 'b111')]}, {'name': 'y', 'type': {'width': 8, 'name': 'wire'}, 'data': [(0, 'bx'), (1, 'b1'), (2, 'b1x'), (3, 'b100'), (4, 'b1000'), (5, 'b10000'), (6, 'b100000'), (7, 'b1000000'), (8, 'b10000000')]}]}]}
    sample_vcd2 = {'name': 'root', 'type': {'name': 'struct'}, 'children': [{'name': 'testbench', 'type': {'name': 'struct'}, 'children': [{'name': 'a', 'type': {'width': 1, 'name': 'reg'}, 'data': [(0, 'x'), (1, '0'), (2, '1'), (3, '0'), (4, '1')]}, {'name': 'b', 'type': {'width': 1, 'name': 'reg'}, 'data': [(0, 'x'), (1, '0'), (3, '1')]}, {'name': 'out', 'type': {'width': 1, 'name': 'wire'}, 'data': [(0, 'x'), (1, '1'), (2, '0'), (4, '1')]}]}]}
    vc = VcdConverter(sample_vcd)
    vc.addToWaveJsonSeparate(['root/testbench/x', 'root/testbench/y'], "mysig_")
    vc.addToWaveJsonAggregated(['root/testbench/x', 'root/testbench/y'], "mysig_")
    print(vc.emitWaveJson())

    vc2 = VcdConverter(sample_vcd2)
    vc2.addToWaveJsonSeparate(['root/testbench/a', 'root/testbench/b', 'root/testbench/out'], "mysig_")
    vc2.addToWaveJsonAggregated(['root/testbench/a', 'root/testbench/b', 'root/testbench/out'], "mysig_")
    print(vc2.emitWaveJson())

