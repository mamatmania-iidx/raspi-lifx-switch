from tkgpio import TkCircuit


# initialize the circuit inside the GUI

configuration = {
    "width": 300,
    "height": 200,
    "leds": [
        {"x": 50, "y": 40, "name": "LED 1", "pin": 21},
        {"x": 100, "y": 40, "name": "LED 2", "pin": 22}
    ],
    "buttons": [
        {"x": 50, "y": 130, "name": "2", "pin": 2},
        {"x": 100, "y": 130, "name": "3", "pin": 3},
        {"x": 150, "y": 130, "name": "4", "pin": 4},
    ]
}

was_held = False
circuit = TkCircuit(configuration)
@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi
    
    from gpiozero import Button
    from time import sleep
    from lifxlan import LifxLAN, Group
    from button_processor import ToggleButtonProcessor, SceneButtonProcessor
    from configparser import ConfigParser

    config = ConfigParser()
    config.read('config.ini')

    button_config = {}


    def held(button):
        global was_held
        was_held = True
        button_config[button.pin].process_hold()
        print("button "+repr(button.pin)+" was held")

    def released(button):
        global was_held
        print(button.pin)
        if was_held:
            was_held = False
        else:
            pressed(button)

    def pressed(button):
        button_config[button.pin].process_press()
        print("button "+repr(button.pin)+" was pressed")


    lan = LifxLAN()
    #Get groups
    
    def get_lights():
        
        groups = {}
        locations = {}
        light_name_pair = {}
        lights = lan.get_devices()
        
        for i in lights:
            group = i.get_group()
            location = i.get_location()
            if group not in groups.keys():
                groups[group] = [i]
            if group in groups.keys():
                groups[group].append(i)
            if location not in locations.keys():
                locations[location] = [i]
            if location in locations.keys():
                locations[location].append(i)

        for i in groups.keys():
            groups[i] = Group(groups[i])
        for i in locations.keys():
            locations[i] = Group(locations[i])
        for i in lights:
            light_name_pair[i.get_label()] = i

        for section in config.sections():
            button = Button(config[section]['pin'])
            if config[section]['type'] == 'Group':
                target = groups[config[section]['target']]
            elif config[section]['type'] == 'Light':
                target = light_name_pair[config[section]['target']]
            if config[section]['behavior'].lower() == "toggle":
                processor = ToggleButtonProcessor
            else:
                processor = SceneButtonProcessor
            button_config[button.pin] = processor(section,config[section]['type'],\
                config[section]['target'],\
                target)
            button.when_held = held
            button.when_released = released
    
    get_lights()
    while True:
        sleep(0.2)