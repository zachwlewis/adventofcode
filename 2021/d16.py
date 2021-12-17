"""
adventofcode.com
Day 16
https://adventofcode.com/2021/day/16
"""

import fr
from bits import BITSPacket

inputs: list[str] = fr.read_as_list('input16_sample')



def dump_inputs(inputs):
    
    for idx, data in enumerate(inputs):
        bt = BITSPacket()
        print(f'Packet {idx + 1} >>>>>>>>>>')
        bt.read_data(data)
        print(version_sum(bt))

def version_sum(bp: BITSPacket) -> int:
    v_sum: int = bp.header.version
    for sp in bp.subpackets:
        v_sum += version_sum(sp)

    return v_sum

# pkt: BITSPacket = BITSPacket()
# pkt.read_data(inputs[0])
# print(pkt.to_string())
# print(version_sum(pkt))

for data in inputs[7:]:
    test: BITSPacket = BITSPacket()
    test.read_data(data)
    print(test.to_string())
