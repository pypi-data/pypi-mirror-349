from typing import List, Any
from enum import Enum

from crccheck.crc import Crc16Ibm3740

from . import DATA_UNIT_HEADER


class DataUnit:
    def __init__(self,
                 command_code,
                 args: List[Any] | bytearray = None):
        self.command_code = command_code
        self.command_buffer = bytearray()
        self.command_buffer.append(DATA_UNIT_HEADER)
        self.command_buffer.append(command_code.value)
        self.command_buffer.append(0)    # Dummy length
        if args is not None:
            for arg in args:
                if isinstance(arg, list):
                    for item in arg:
                        self.command_buffer.append(item)
                elif isinstance(arg, bytes):
                    for item in arg:
                        self.command_buffer.append(item)
                elif isinstance(arg, bytearray):
                    self.command_buffer += bytearray(arg)
                elif isinstance(arg, Enum):
                    self.command_buffer.append(arg.value)
                else:
                    self.command_buffer.append(arg)
        # Set real payload/argument length
        # self.command_buffer[2] = (len(self.command_buffer) - 3).to_bytes(length=1, byteorder='little')
        self.command_buffer[2] = len(self.command_buffer) - 3

        # Get CRC16 of packet
        crc16 = self.crc16(self.command_buffer[1:])
        self.command_buffer += int(crc16).to_bytes(2, 'little')

    def get_command_code(self):
        return self.command_code
    def bytes(self):
        return self.command_buffer

    # def get_packet_command(self):
    #     return RadioCommands(self.command_buffer[0])

    def __str__(self):
        return self.command_buffer.hex(sep=' ').upper()

    @staticmethod
    def crc16(data: bytes):
        crc = Crc16Ibm3740.calc(data)
        return crc