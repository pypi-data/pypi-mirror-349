import logging
import time

from src.driver_sble_py_klsblelcf import KlSbleLcr

logging.basicConfig(level=logging.DEBUG)


def callback(beacon):
    logging.info(beacon)


driver = KlSbleLcr('COM22')

if driver.is_connected():
    driver.set_notification_callback(callback)
    driver.configure_cw(True, 500, 500)
    time.sleep(10)
    driver.configure_cw(False, 500, 500)
