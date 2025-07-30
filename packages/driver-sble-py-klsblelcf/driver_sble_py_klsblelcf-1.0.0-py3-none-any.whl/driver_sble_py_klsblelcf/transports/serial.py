import logging
import serial
from threading import Thread
import time

logger = logging.getLogger(__name__)


class SerialTransport:
    def __init__(self, port=None, read_callback=None):
        self._read_callback = read_callback
        self._serial: serial = serial.Serial(
            baudrate=115200,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        self._rx_thread = None
        self._rx_thread_run = False
        if port:
            self.connect(port=port)

    def connect(self, port) -> bool:
        if self._serial.isOpen():
            logger.info('Serial port already connected.')
            return False
        try:
            self._serial.port = port
            self._serial.open()
            logger.info('Serial port connected.')
            self._rx_thread = Thread(target=self._rx_thread_function, daemon=True, name='RxThread')
            self._rx_thread_run = True
            self._rx_thread.start()
            return True
        except Exception as e:
            logger.warning(e)
            return False

    def set_read_callback(self, callback):
        self._read_callback = callback

    def clear_read_callback(self):
        self._read_callback = None

    def is_connected(self) -> bool:
        return self._serial.isOpen()

    def disconnect(self) -> bool:
        self._rx_thread_run = False
        if self._rx_thread:
            self._rx_thread.join()
        if not self.is_connected():
            logger.info('Serial port already disconnected.')
            return False
        try:
            self._serial.close()
            logger.info('Serial port disconnected.')
            return True
        except Exception as e:
            logger.warning(e)
            return False

    def write(self, data: bytes) -> None:
        self._serial.write(data)
        logger.debug('TX >> ' + data.hex(sep=' ').upper())

    def _read(self) -> bytes | None:
        try:
            data = self._serial.read_all()
            if len(data) > 0:
                logger.debug('RX << ' + data.hex(sep=' ').upper())
                return data
        except Exception as e:
            logger.warning('Exception during serial port read:' + str(e))
            logger.warning('Disconnecting serial port.')
            self.disconnect()

    def _rx_thread_function(self):
        while self._rx_thread_run:
            time.sleep(0.001)
            if not self.is_connected():
                continue
            data = self._read()
            if data is None or len(data) == 0:
                continue
            if self._read_callback:
                self._read_callback(data)
            else:
                logger.warning("No read callback set")
