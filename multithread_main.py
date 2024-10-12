import logging.config
import subprocess
import sys

import board
import neopixel
from dadou_utils.utils.shutdown_restart import ShutDownRestart

from dadou_utils.utils_static import SHUTDOWN_PIN, RESTART_PIN, STATUS_LED_PIN, DEVICES_LIST, LIGHTS_PIN, LIGHTS, \
    LIGHTS_LED_COUNT, LOGGING_CONFIG_FILE, TIME

from dadourobot.sequences.animation_manager import AnimationManager
from dadourobot.actions.lights import Lights
from hardrive.files.hardrive_json_manager import HardDriveJsonManager
from dadourobot.input.global_receiver import GlobalReceiver
from hardrive.hardrive_config import config, GLOBAL_LIGHTS_COUNT, HELMET_LIGHT_START, HELMET_LIGHT_END, JSON_DISK, \
    JSON_HELMET, DISK, HELMET, SHUTDOWN, PROCESS_LIST

sys.path.append('')
print(sys.path)
print(dir(board))
print('Starting Didier')

logging.config.fileConfig(config[LOGGING_CONFIG_FILE], disable_existing_loggers=False)

################################ Component initialisations ##################################

#https://imadali.net/posts/streaming-data-between-python-programs/

global_receiver = None
is_receiver = len(sys.argv) == 1

if len(sys.argv) == 1:
    logging.info("launch process")
    global_receiver = GlobalReceiver()
    for process_name in PROCESS_LIST:
        logging.warning("start {} process".format(process_name))
        process = subprocess.Popen(['python', 'multithread_main.py', process_name], stdout=subprocess.PIPE)

components = []

disk_json_manager = HardDriveJsonManager(config)
pixels = neopixel.NeoPixel(config[LIGHTS_PIN], GLOBAL_LIGHTS_COUNT, auto_write=False, brightness=0.05, pixel_order=neopixel.GRB)

for i in range(1, len(sys.argv)):
    if sys.argv[i] == DISK:
        components.append(Lights(0, HELMET_LIGHT_START - 1, disk_json_manager, pixels, JSON_DISK))
    elif sys.argv[i] == HELMET:
        components.append(Lights(HELMET_LIGHT_START, HELMET_LIGHT_END, disk_json_manager, pixels, JSON_HELMET))
    elif sys.argv[i] == SHUTDOWN:
        components.append(ShutDownRestart(config[SHUTDOWN_PIN], config[RESTART_PIN], config[STATUS_LED_PIN]))
    else:
        logging.error("wrong argument")


#devices_manager = SerialDeviceManager(DEVICES_LIST)


################################ Main loop ##################################

last_input_time = 0

while True:
    # logging.debug('run')

    try:
        if is_receiver:
            global_receiver.get_msg()

        else:
            msg = GlobalReceiver.read_msg()
            if msg and TIME in msg:
                if last_input_time != msg[TIME]:
                    last_input_time = msg[TIME]
                    logging.warning("new data {}".format(msg))
                    for component in components:
                        component.update(msg)

            for component in components:
                component.process()

        #wheel.check_stop(msg)


    except Exception as err:
        logging.error('exception {}'.format(err), exc_info=True)
