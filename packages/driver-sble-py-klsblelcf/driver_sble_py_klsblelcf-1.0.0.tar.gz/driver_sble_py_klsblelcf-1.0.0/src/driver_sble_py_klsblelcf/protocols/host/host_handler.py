import logging
import queue
import struct
import time
from threading import Thread
from typing import Callable

from ..data_unit import DATA_UNIT_HEADER
from ..data_unit.data_unit import DataUnit
from . import BleReaderCommands

logger = logging.getLogger(__name__)


class HostHandler(object):
    def __init__(self):
        self.buffer = bytearray()
        self.response_queue = queue.Queue()
        self.notification_queue = queue.Queue()
        self.notification_callback = None
        self._callback_thread = Thread(target=self._callback_thread_fxn, daemon=True, name='CallbackThread')
        self._callback_thread.start()

    def set_notification_callback(self, callback) -> None:
        self.notification_callback = callback

    def _callback_thread_fxn(self) -> None:
        while True:
            if not self.notification_queue.empty():
                beacon = self.notification_queue.get()
                if self.notification_callback:
                    self.notification_callback(beacon)
            time.sleep(0.001)

    def append_data(self, data: bytearray):
        if data is not None:
            self.buffer.extend(data)
            self._try_parse_data()

    def _try_parse_data(self):
        try:
            start = self.buffer.find(bytearray([DATA_UNIT_HEADER]))
            if start > 0:
                logger.info("Syncing data unit PREAMBLE")
                self.buffer = self.buffer[start:]

            # Check if length field is present
            if len(self.buffer) < 3:
                return

            data_unit_length = self.buffer[2] + 5  # SYNC_HEADER, CMD, PAYLOAD_L, PAYLOAD, CRC16
            # Check if entire data unit is available
            if len(self.buffer) < data_unit_length:
                return

            # Check CRC
            crc_rx = struct.unpack('<H', self.buffer[data_unit_length - 2: data_unit_length])[0]
            crc_calc = DataUnit.crc16(self.buffer[1:data_unit_length - 2])

            # TODO fix CRC on FW
            if crc_rx == crc_calc or True:
                command = self.buffer[1]
                payload_length = self.buffer[2]
                payload = self.buffer[3:3 + payload_length]
                self._process_host_response(command, payload_length, payload)
                # Remove processed data
                del self.buffer[:data_unit_length]
        except Exception as e:
            logger.error(e)

    def _process_host_response(self,
                               command,
                               payload_length,
                               payload):
        host_command = BleReaderCommands(command)

        if host_command == BleReaderCommands.SET_868_RADIO:
            self.response_queue.put(True)
        elif host_command == BleReaderCommands.BEACON_DATA:
            self.notification_queue.put(payload)
