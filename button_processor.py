from configparser import ConfigParser
from lifxlan import Group
import os
import json

def parse_int_tuple(input):
    return tuple(int(k.strip()) for k in input[1:-1].split(','))

class AbstractButtonProcessor:
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""

    def process_press(self):
        raise NotImplementedError("Should have implemented this")

    def process_hold(self):
        raise NotImplementedError("Should have implemented this")

class ToggleButtonProcessor(AbstractButtonProcessor):
    def __init__(self, config_section, target_type, target_name, object) -> None:
        super().__init__()
        self.config_section = config_section
        self.target_name = target_name
        self.target_type = target_type
        self.light_obj = object
        self.toggle_status = True
    
    def process_press(self):
        self.light_obj.set_power(self.toggle_status,250,True)
        self.toggle_status = not self.toggle_status
        
    def process_hold(self):
        self.light_obj.set_power(False,250,True)
        self.toggle_status = True

class SceneButtonProcessor(AbstractButtonProcessor):
    def __init__(self, config_section, target_type, target_name, object) -> None:
        super().__init__()
        self.config_section = config_section
        self.target_name = target_name
        self.target_type = target_type
        self.light_obj = object
        self.config = ConfigParser()
        try:
            self.config.read("scenes/{}_{}_{}.ini".format(config_section, target_type, target_name))
        except:
            with open("scenes/{}_{}_{}.ini".format(config_section, target_type, target_name),"w"):
                pass
            
        

    def process_press(self):
        #Sets light(s) to the configured scene
        print("todo")
        print(self.config.sections())
        for section in self.config.sections():
            print(self.config[section]["power"])
            print(self.config[section]["color"])
        if type(self.light_obj) == Group:
            lights = self.light_obj.get_device_list()
        else:
            lights = [self.light_obj]
        for light in lights:
            label = light.get_label()
            power = int(self.config[label]["power"]) > 0
            
            print(power)
            light.set_power(power)
            if self.config[label]["multizone"]=="true":
                light.set_zone_colors(json.loads(self.config[label]["color"]), 1000, True)
            else:
                light.set_color(json.loads(self.config[label]["color"]), 1000, True)
            

            
        
        
    def process_hold(self):
        #Stores current light settings into a scene
        self.config = ConfigParser()
        if type(self.light_obj) == Group:
            lights = self.light_obj.get_device_list()
        else:
            lights = [self.light_obj]
        for light in lights:
            name = light.get_label()
            self.config[name] = {}
            self.config[name]["power"] = str(light.get_power())
            if light.supports_multizone():
                self.config[name]["multizone"]="true"
                self.config[name]["color"]=json.dumps(light.get_color_zones())
            else:
                self.config[name]["multizone"]="false"
                self.config[name]["color"]=json.dumps(light.get_color())
            with open("scenes/{}_{}_{}.ini".format(self.config_section, self.target_type, self.target_name), 'w') as fp:
                self.config.write(fp)
        pass
