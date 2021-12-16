"""
adventofcode.com
Day 16
https://adventofcode.com/2021/day/16
"""

import fr
from bits import BITSPacket

inputs: list[str] = fr.read_as_list('input16_sample')

bt = BITSPacket()

def print_packet(packet: BITSPacket):
    print(f'+-----< {packet.data} >')
    print(f'| Binary:  {packet.bin()}')
    print(f'| Version: {packet.version}')
    print(f'| Type ID: {packet.type_id}')


    if packet.is_literal():
        print(f'+-----< LITERAL: {packet.literal()} >')
    else:
        print(f'+-----< OPERATOR: {packet.type_id} >')

for input in inputs:
    bt.read_data(input)
    print_packet(bt)
    # bt.read_data('110100101111111000101', 'binary')
    # print_packet(bt)

