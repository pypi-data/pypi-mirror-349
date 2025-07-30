import logging
import struct
from typing import Callable, List

from .protocols.data_unit.data_unit import DataUnit
from .protocols.host import BleReaderCommands
from .protocols.host.host_handler import HostHandler
from .transports.serial import SerialTransport

logger = logging.getLogger(__name__)


class KlSbleLcr:

    def __init__(self, connection_string=None):
        self._transport: SerialTransport | None = None
        self._host_controller = HostHandler()
        self.connection_string = connection_string
        if connection_string is not None:
            self.connect(connection_string)

    def set_notification_callback(self, notification_callback: Callable[[any], None]):
         self._host_controller.set_notification_callback(notification_callback)

    def connect(self, connection_string=None) -> bool:
        if connection_string:
            self.connection_string = connection_string
        # TODO: Parse connection string to determine transport type (serial only for now)
        self._transport = SerialTransport(read_callback=self._host_controller.append_data)
        return self._transport.connect(connection_string)

    def is_connected(self) -> bool:
        if self._transport is None:
            return False
        return self._transport.is_connected()

    def disconnect(self) -> bool:
        if not self.is_connected():
            logger.info('Transport already disconnected.')
            return True
        try:
            self._transport.disconnect()
            logger.info('Transport successfully disconnected.')
            return True
        except Exception as e:
            logger.warning(e)
            return False

    def _execute_command(self, command_packet: DataUnit, has_response: bool = True):
        if not self._transport.is_connected():
            if self.connection_string is None:
                logger.info('Transport is disconnected.')
                return None
            if not self._transport.connect(self.connection_string):
                logger.info('Transport is disconnected.')
                return None

        logger.info('TX -> ' + command_packet.get_command_code().name)
        self._transport.write(command_packet.bytes())
        if has_response:
            try:
                response = self._host_controller.get_response()
                logger.info('RX <- ' + str(response))
                return response
            except TimeoutError:
                logger.warning('Timeout executing ' + command_packet.get_command_code().name)
                return None

    def configure_cw(self, enable: bool, dac0_value: int, dac1_value: int):
        logging.info('configure_cw: ' + str(enable))
        payload = bytearray(bytes([enable]) + struct.pack('>H', dac0_value) + struct.pack('>H', dac1_value))
        packet = DataUnit(command_code=BleReaderCommands.SET_868_RADIO, args=payload)
        response = self._execute_command(packet, has_response=False)
        return response

    # def ping(self) -> bool:
    # TODO
    #     return ack

    # def reset(self) -> bool:
    # TODO
    #     return ack

    # def get_reader_info(self) -> ReaderInfo:
    # TODO
    #     return info

    # def get_tx_power(self) -> float:
    # TODO
    #     return dBm

    # def set_tx_power(self, dBm: float) -> bool:
    # TODO
    #    return ack

    # def start_cw(self) -> bool:
    # TODO
    #    return ack

    # def stop_cw(self) -> bool:
    # TODO
    #    return ack
