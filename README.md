# Raspberry Pi LIFX Switch

I don't want to deal with LIFX's Smart Switch, so I'll fashion one myself.

## Requirements

## Setup
1. Clone this repo.
2. Install requirements from requirements.txt.
3. Create your own config.ini file, see example.
4. Run script.py, or if you want to have fun on your own PC, the tkcircuit version on tkcircuit.py.

## More on Config.ini

### Pin
Put the GPIO pin number of your button here.

### Behaviors
* Toggle  
Toggles selected light(s) on and off. Press to toggle, hold to turn off.
* Scene
Stores state of light(s) and sets lights according to the saved state. Hold to save the current state, press to activate scene.

### Type and Group
Type: Location, Group, or Light.  
Target: Name of the specified location, group, or light.

## Limitations/Bugs?

* Multizone lights behave weirdly for scene buttons. If you set your scene with a lightstrip off, all of the zones will stay off even if you use toggle on the light afterwards.  
Have another scene handy with those lights on.

## Future updates
* GUI to edit the config.
* Web server so you can edit the configs from a web browser.
* Add Hue light support, maybe?
