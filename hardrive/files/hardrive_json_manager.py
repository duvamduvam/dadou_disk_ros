import logging

import jsonpath_rw_ext

# '{}_{}_{}_{}'.format(s1, i, s2, f)
from dadou_utils.files.abstract_json_manager import AbstractJsonManager
from dadou_utils.utils_static import COLOR, JSON_LIGHTS_BASE
from dadou_utils.utils_static import JSON_AUDIOS, JSON_COLORS, JSON_MAPPINGS, \
    JSON_LIGHTS
from hardrive.hardrive_config import JSON_HELMET


class HardDriveJsonManager(AbstractJsonManager):
    logging.info("start json manager")

    colors = None
    lights = None
    lights_seq = None

    def __init__(self, config):
        self.config = config
        component = [self.config[JSON_COLORS], config[JSON_LIGHTS_BASE], JSON_HELMET]

        super().__init__(config, component)

    #def get_face_seq(self, key):
    #    result = self.find(self.face_seq, 'main_seq', '$.keys[?key ~ ' + key + ']')
    #    return self.standard_return(result, False, False)

    """def get_lights(self, key):
        return self.get_dict_from_list(self.json_files[self.config[JSON_LIGHTS]], "keys", key)


    "def get_lights(self, key):
        result = jsonpath_rw_ext.match('$.lights_seq[?keys~' + key + ']', self.lights)
        # logging.debug(result)
        #return self.standard_return(result, True, key)
        if len(result) > 0:
            return result[0]

    def get_color(self, key):
        result = jsonpath_rw_ext.match('$.colors[?name~' + key + ']', self.json_files[self.config[JSON_COLORS]])
        logging.debug(result)
        if len(result) > 0:
            json_color = result[0][COLOR]
            return (int(json_color['red']), int(json_color['green']), int(json_color['blue']))
        else:
            logging.error("no color" + key)
            return None

    @staticmethod
    def get_attribut(json_object, key):
        if key in json_object:
            return json_object[key]
        else:
            return None

    def get_audio_path_by_name(self, name) -> str:
        result = jsonpath_rw_ext.match('$.audios[?name~' + name + ']', self.json_files[self.config[JSON_AUDIOS]])
        return self.standard_return(result, True, False)

    def get_audios(self, key: str) -> str:
        #result = jsonpath_rw_ext.match('$.audios[?key~' + key + ']', self.audios)
        if key:
            result = jsonpath_rw_ext.match("$.audios[?(keys[*]~'"+key+"')]", self.json_files[self.config[JSON_AUDIOS]])
            return self.standard_return(result, True, False)
        else:
            logging.error("input str None")

    def get_mappings(self, key: str, mapping_type: str) -> str:
        if key:
            result = jsonpath_rw_ext.match("$."+mapping_type+"[?(keys[*]~'"+key+"')]", self.json_files[self.config[JSON_MAPPINGS]])
            return self.standard_return(result, True, 'value')
        else:
            logging.error("input str None")"""
