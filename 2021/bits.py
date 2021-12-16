"""
adventofcode.com
[Buoyancy Interchange Transmission System (BITS)](https://adventofcode.com/2021/day/16)
"""

from __future__ import annotations

class BITSPacket:
    """
    Nested packets following the BITS protocol.

    Packet Types
    4: literal value
    Others: Operator
    """

    TYPE_LITERAL = 4

    def __init__(self) -> None:
        self.data: str = ''
        self.binary: list[str] = ''
        self.version: int = 0
        self.type_id: int = 0
        self.subpackets: list[BITSPacket] = []

    def bin(self) -> str:
        return ''.join(self.binary)

    def parse_hex(self, data: str = '') -> None:
        """
        Populates `data` and `binary` from a hex string.
        """
        self.data = data.upper()
        self.binary = []
        for hex in list(data):
            self.binary.extend(f'{int(hex, 16):0>4b}')

    def parse_binary(self, data: str = '') -> None:
        """
        Populates `data` and `binary` from a binary string.
        """
        bits = len(data)
        offset = 0 if bits % 4 == 0 else 4 - bits % 4
        valid_data = data + '0' * offset
        print(bits, offset, valid_data)
        self.data = f'{int(valid_data, 2):x}'.upper()
        self.binary = list(valid_data)

    def read_data(self, data:str = '', mode: str = 'hex') -> None:
        self.parse_hex(data) if mode == 'hex' else self.parse_binary(data)
        
        self.version = int(''.join(self.binary[0:3]), 2)
        self.type_id = int(''.join(self.binary[3:6]), 2)

        if self.type_id != BITSPacket.TYPE_LITERAL:
            # Read the rest of the packets as a new packet
            length_type_id = self.binary[6]
            subpacket_length = 15 if length_type_id == '0' else 11
            subpacket_type = 'Length' if length_type_id == '0' else 'Count'
            print(f'Subpacket {subpacket_type}: {int("".join(self.binary[7:7+subpacket_length]), 2)}')

    def is_literal(self) -> bool:
        return self.type_id == BITSPacket.TYPE_LITERAL

    def literal(self) -> int:
        """
        Returns the literal value, or -1 if not a literal packet.
        """
        if not self.is_literal():
            return -1

        ptr: int = 6
        bits: list[str] = ['0']
        has_field: bool = True
        while has_field:
            START = ptr + 1
            END = ptr + 5
            bits.extend(self.binary[START:END])
            has_field = self.binary[ptr] == '1'
            ptr = END

        return int(''.join(bits), 2)