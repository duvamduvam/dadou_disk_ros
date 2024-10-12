import logging.config
import sys

import board
import neopixel

from dadou_utils.logging_conf import LoggingConf
from dadou_utils.utils.status import Status
from dadou_utils.utils_static import SHUTDOWN_PIN, STATUS_LED_PIN, LIGHTS_PIN, LOGGING_FILE_NAME, MAIN_THREAD, \
    MULTI_THREAD, BRIGHTNESS
from dadourobot.actions.lights import Lights
from dadourobot.input.global_receiver import GlobalReceiver
from hardrive.files.hardrive_json_manager import HardDriveJsonManager
from hardrive.hardrive_config import config, GLOBAL_LIGHTS_COUNT, HELMET_LIGHT_END, JSON_HELMET

sys.path.append('')
print(sys.path)
print(dir(board))

print('Starting Disk, logs : {}'.format(config[LOGGING_FILE_NAME]))
#logging.config.fileConfig(config[LOGGING_CONFIG_FILE], disable_existing_loggers=False)
logging.config.dictConfig(LoggingConf.get(config[LOGGING_FILE_NAME], "disk"))

################################ Component initialisations ##################################
# TODO profiling
# TODO multitreading : https://makergram.com/community/topic/29/multi-thread-handling-for-normal-processes-using-python/4

components = []

disk_json_manager = HardDriveJsonManager(config)
pixels = neopixel.NeoPixel(config[LIGHTS_PIN], GLOBAL_LIGHTS_COUNT, auto_write=False, brightness=config[BRIGHTNESS], pixel_order=neopixel.GRB)

#helmet_lights = Lights(0, HELMET_LIGHT_END, disk_json_manager, pixels, JSON_HELMET)
helmet_lights = Lights(config=config, start=0, end=HELMET_LIGHT_END,
                                 json_manager=disk_json_manager, global_strip=pixels, light_type='lights_helmet', json_light=JSON_HELMET)

#TODO check best order for performances
components.extend([helmet_lights, Status(config[SHUTDOWN_PIN], config[STATUS_LED_PIN])])

config[MAIN_THREAD] = True
config[MULTI_THREAD] = False
global_receiver = GlobalReceiver(config)

################################ Main loop ##################################

while True:
    # logging.debug('run')

    try:
        msg = global_receiver.get_msg()

        if msg:
            for component in components:
                component.update(msg)

        for component in components:
            component.process()

        #wheel.check_stop(msg)


    except Exception as err:
        logging.error('exception {}'.format(err), exc_info=True)
