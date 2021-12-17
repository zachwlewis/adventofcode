"""
adventofcode.com
Day 16
https://adventofcode.com/2021/day/16
"""

import fr
from bits import BITSPacket

inputs: list[str] = fr.read_as_list('input16')



def dump_inputs(inputs):
    
    for idx, data in enumerate(inputs):
        bt = BITSPacket()
        #print(f'Packet {idx + 1} >>>>>>>>>>')
        bt.read_data(data)
        print(f'Packet {idx + 1}: {bt.pretty()}')

def version_sum(bp: BITSPacket) -> int:
    v_sum: int = bp.header.version
    for sp in bp.subpackets:
        v_sum += version_sum(sp)

    return v_sum

# dump_inputs(inputs)

pkt: BITSPacket = BITSPacket()
pkt.read_data(inputs[0])
print(version_sum(pkt))
print(pkt.evaluate())
