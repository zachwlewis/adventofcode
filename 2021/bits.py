"""
adventofcode.com
[Buoyancy Interchange Transmission System (BITS)](https://adventofcode.com/2021/day/16)
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass
class BITSPacketHeader:
    """
    Packet header for the [BITS protocol](https://adventofcode.com/2021/day/16).

    Contains the packet version, type_id and operator values (if an operator).
    """
    raw: str = ''
    version: int = -1
    type_id: int = -1
    operator_mode: int = -1
    operator_value: int = -1

    def is_valid(self) -> bool:
        """Is this header valid?"""
        if self.version < 0 or self.type_id < 0:
            return False

        if self.type_id != BITSPacket.TYPE_LITERAL:
            return self.operator_mode != -1 and self.operator_value != -1

        return True

    def size(self) -> int:
        """The size of the header."""
        if not self.is_valid():
            return -1

        return len(self.raw)

    @classmethod
    def from_data(cls, data: str) -> tuple[BITSPacketHeader, str]:
        """
        Takes a binary data stream and returns a header and payload.
        """

        if len(data) < 6 or int(data, 2) == 0:
            return BITSPacketHeader(), 'BAD_HEADER'
        
        version = int(data[0:3], 2)
        type_id = int(data[3:6], 2)

        if type_id == BITSPacket.TYPE_LITERAL:
            return BITSPacketHeader(data[:6], version, type_id), data[6:]
        
        operator_mode = data[6]

        if operator_mode == BITSPacket.SUBTYPE_LENGTH:
            operator_value = int(data[7:22], 2)
            return BITSPacketHeader(data[:22], version, type_id, operator_mode, operator_value), data[22:]
        else:
            operator_value = int(data[7:18], 2)
            return BITSPacketHeader(data[:18], version, type_id, operator_mode, operator_value), data[18:]


class BITSPacket:
    """
    Nested packets following the [BITS protocol](https://adventofcode.com/2021/day/16).

    Packet Types
    4: literal value
    Others: Operator
    """

    @classmethod
    def eval_sum(cls, packet: BITSPacket) -> int:
        if not packet.evaluated:

            value: int = 0
            for subpacket in packet.subpackets:
                value += subpacket.evaluate()

            packet.literal_value = value

        return packet.literal_value
    
    @classmethod
    def eval_product(cls, packet: BITSPacket) -> int:
        if not packet.evaluated:
            value = packet.subpackets[0].evaluate()
            for subpacket in packet.subpackets[1:]:
                value *= subpacket.evaluate()

            packet.literal_value = value
        return packet.literal_value

    @classmethod
    def eval_minimum(cls, packet: BITSPacket) -> int:
        if not packet.evaluated:
            values: list[int] = []
            for subpacket in packet.subpackets:
                values.append(subpacket.evaluate())

            packet.literal_value = min(values)
        return packet.literal_value

    @classmethod
    def eval_maximum(cls, packet: BITSPacket) -> int:
        if not packet.evaluated:
            values: list[int] = []
            for subpacket in packet.subpackets:
                values.append(subpacket.evaluate())

            packet.literal_value = max(values)
        return packet.literal_value

    @classmethod
    def eval_literal(cls, packet: BITSPacket) -> int:
        """Evaluates the value of the first packet"""
        packet.parse_literal()
        return packet.literal_value

    @classmethod
    def eval_greater(cls, packet: BITSPacket) -> int:
        a = packet.subpackets[0].evaluate()
        b = packet.subpackets[1].evaluate()
        packet.literal_value = 1 if a > b else 0
        return packet.literal_value

    @classmethod
    def eval_less(cls, packet: BITSPacket) -> int:
        a = packet.subpackets[0].evaluate()
        b = packet.subpackets[1].evaluate()
        packet.literal_value = 1 if a < b else 0
        return packet.literal_value

    @classmethod
    def eval_equal(cls, packet: BITSPacket) -> int:
        a = packet.subpackets[0].evaluate()
        b = packet.subpackets[1].evaluate()
        packet.literal_value = 1 if a == b else 0
        return packet.literal_value


    TYPE_SUM = 0
    TYPE_PRODUCT = 1
    TYPE_MINIMUM = 2
    TYPE_MAXIMUM = 3
    TYPE_LITERAL = 4
    TYPE_GREATER = 5
    TYPE_LESS = 6
    TYPE_EQUAL = 7

    OP_NAME = {
        TYPE_SUM: 'SUM',
        TYPE_PRODUCT: 'PRODUCT',
        TYPE_MINIMUM: 'MINIMUM',
        TYPE_MAXIMUM: 'MAXIMUM',
        TYPE_LITERAL: 'LITERAL',
        TYPE_GREATER: 'GREATER',
        TYPE_LESS: 'LESS',
        TYPE_EQUAL: 'EQUAL',
    }

    OP_SYMBOL = {
        TYPE_SUM: ' + ',
        TYPE_PRODUCT: ' × ',
        TYPE_MINIMUM: ' v ',
        TYPE_MAXIMUM: ' ^ ',
        TYPE_LITERAL: '',
        TYPE_GREATER: ' > ',
        TYPE_LESS: ' < ',
        TYPE_EQUAL: ' = ',
    }

    SUBTYPE_LENGTH = '0'
    SUBTYPE_COUNT = '1'

    def __init__(self) -> None:
        self.header: BITSPacketHeader = BITSPacketHeader()
        self.data: str = ''
        self.binary: str = ''
        self.payload: str = ''
        self.subpackets: list[BITSPacket] = []
        self.literal_value = -1
        self.literal_size = 0
        self.evaluated: bool = False

    def is_valid(self) -> bool:
        return self.header.is_valid()

    def size(self) -> int:
        if len(self.subpackets) == 0:
            # No subpackets. It's a literal
            return self.header.size() + self.literal_size
        else:
            size = self.header.size()
            for p in self.subpackets:
                size += p.size()
            return size

    def to_verbose_string(self, pre: str = '', level: str = 'low') -> str:
        """Verbose string representation of packet."""
        out: str = ''
        out += f'{pre}┏━━━ {BITSPacket.OP_NAME[self.header.type_id]}: {self.literal_value}\n'
        if level == 'high': out += f'{pre}┃  Hex    : {self.data}\n'
        if level == 'high': out += f'{pre}┃  Binary : {self.binary}\n'
        if level == 'high': out += f'{pre}┃  Size   : {self.size()}\n'
        if level == 'high': out += f'{pre}┣━ Header\n'
        if level == 'high': out += f'{pre}┃  Version: {self.header.version}\n'
        if level == 'high': out += f'{pre}┃  Type ID: {self.header.type_id}\n'
        if level == 'high': out += f'{pre}┃  OP ID  : {self.header.operator_mode}\n'
        if level == 'high': out += f'{pre}┃  OP Val : {self.header.operator_value}\n'
        if level == 'high': out += f'{pre}┃  Raw    : {self.header.raw}\n'
        if level == 'high': out += f'{pre}┣━ Payload: {" " * self.header.size()}{self.payload}\n'
        if len(self.subpackets) > 0:
            out += f'{pre}┣━ Subpackets ({len(self.subpackets)})\n'
            for sp in self.subpackets:
                out += sp.to_verbose_string(f'{pre}┃  ', level)
        out += f'{pre}┗━━━━━━━━━━━━\n'

        return out

    def pretty(self, first:bool=True) -> str:
        out = ''
        if self.header.type_id == BITSPacket.TYPE_LITERAL: out = f'{self.literal_value}'
        else:
            children = []
            for sp in self.subpackets:
                children.append(sp.pretty(False))
            
            joiner = BITSPacket.OP_SYMBOL[self.header.type_id]
            out =  f'({joiner.join(children)})'
        
        return out if not first else f'{out} => {self.literal_value}'

    def to_string(self, mode: str = 'verbose', pre: str = '') -> str:
        """
        Returns the packet information as a formatted string.
        """
        if mode == 'verbose':
            return self.to_verbose_string(pre)
        elif mode == 'binary':
            return f'{pre}{self.binary}'
        else:
            return self.data

    def parse_hex(self, data: str = '') -> None:
        """
        Populates `data` and `binary` from a hex string.
        """
        self.data = data.upper()
        binary = []
        for hex_value in list(data):
            binary.extend(f'{int(hex_value, 16):0>4b}')
            self.binary = ''.join(binary)

    def parse_binary(self, data: str = '') -> None:
        """
        Populates `data` and `binary` from a binary string.
        """
        bits = len(data)
        offset = 0 if bits % 4 == 0 else 4 - bits % 4
        valid_data = data + '0' * offset
        self.data = f'{int(valid_data, 2):x}'.upper()
        self.binary = valid_data

    def parse_subpackets(self, data: str = '') -> str:
        """Parses subpackets from the payload."""
        if self.header.operator_mode == BITSPacket.SUBTYPE_LENGTH:
            # Process the given number of bits
            bin_data = data[:self.header.operator_value]
        else:
            # Process the rest of the payload
            bin_data = data
        
        # print(f'Subpacket Header: {self.header.raw}')
        # print(f'Subpacket {self.header.operator_mode}: {self.header.operator_value}')
        # print(f'Payload: {self.payload}')
        

        
        subpacket_count:int = 0
        bp = BITSPacket()
        while len(bin_data) > 0 and bp.read_data(bin_data, 'bin') and (self.header.operator_mode == BITSPacket.SUBTYPE_LENGTH or subpacket_count < self.header.operator_value):
            # print(f'Subpacket {subpacket_count} > [{bin_data}] ({len(bin_data)})')
            bin_data = bin_data[bp.size():]
            if bp.is_valid():
                self.subpackets.append(bp)
                if self.header.operator_mode == BITSPacket.SUBTYPE_COUNT:
                    subpacket_count += 1
            bp = BITSPacket()

        return bin_data


    def read_data(self, data:str = '', mode: str = 'hex') -> bool:
        """
        Reads `data` using specified `mode`:
        - `hex`: Read `data` as hex
        - `bin`: Read `data` as binary
        """
        if len(data) < 6: return False
        if mode == 'hex':
            self.parse_hex(data)
        elif mode == 'bin':
            self.parse_binary(data)
        else:
            return

        self.header, self.payload = BITSPacketHeader.from_data(self.binary)

        if not self.header.is_valid():
            return False

        if self.header.type_id == BITSPacket.TYPE_LITERAL:
            self.parse_literal()

        elif self.header.type_id != BITSPacket.TYPE_LITERAL:
            # Read the rest of the packets as a new packet
            self.parse_subpackets(self.payload)

        self.evaluate()
        
        return True

    def is_literal(self) -> bool:
        return self.header.is_valid() and self.header.type_id == BITSPacket.TYPE_LITERAL

    def parse_literal(self) -> None:
        """
        If `type_id` is `TYPE_LITERAL`, return the integer value of the `payload`.
        Otherwise, return `-1`.
        """
        if not self.is_literal():
            self.literal_value = 0

        ptr: int = 0
        bits: list[str] = ['0']
        has_field: bool = True
        while has_field:
            start = ptr + 1
            end = ptr + 5
            bits.extend(self.payload[start:end])
            has_field = self.payload[ptr] == '1'
            ptr = end

        self.literal_value = int(''.join(bits), 2)
        self.literal_size = ptr
        self.evaluated = True

    def evaluate(self) -> int:
        if not self.evaluated:
            if self.header.type_id == BITSPacket.TYPE_SUM: BITSPacket.eval_sum(self)
            if self.header.type_id == BITSPacket.TYPE_PRODUCT: BITSPacket.eval_product(self)
            if self.header.type_id == BITSPacket.TYPE_MINIMUM: BITSPacket.eval_minimum(self)
            if self.header.type_id == BITSPacket.TYPE_MAXIMUM: BITSPacket.eval_maximum(self)
            if self.header.type_id == BITSPacket.TYPE_LITERAL: BITSPacket.eval_literal(self)
            if self.header.type_id == BITSPacket.TYPE_GREATER: BITSPacket.eval_greater(self)
            if self.header.type_id == BITSPacket.TYPE_LESS: BITSPacket.eval_less(self)
            if self.header.type_id == BITSPacket.TYPE_EQUAL: BITSPacket.eval_equal(self)
            
            self.evaluated = True

        return self.literal_value
