"""Welcome to the new version of autobridger! You are now able to configure your hotkeys
for both straight and diagonal bridging, as well as the stop key.
Configurations will be stored in the bridgerconfig.txt file.
If you want to change config delete the file and rerun the program.
You will only need to configure once and your hotkeys will be saved.
Press end key on your keyboard to exit program.
"""

import pydirectinput
import os.path
import keyboard
import time



#default direction
straight_bridge_keys = ['s', 'd']
if not os.path.isfile("./bridgerconfig.txt"):
    with open('bridgerconfig.txt', 'w') as config_file:
        bridge_direction = input('Do you bridge the right way (s/d)? Y/N: ')
        if bridge_direction.strip().upper() == "Y":
            straight_bridge_keys = "s,d"
        elif bridge_direction.strip().upper() == "N":
            straight_bridge_keys = "s,a"
        else:
            print('You are stupid enter Y or N next time. Delete the bridgerconfig file and rerun the program.')
            wrong_input = True
        config_file.write(f"{straight_bridge_keys}\n")

        print("You can make your hotkeys up with up to 3 keys, such as 'ctrl + shift + b'.")
        print("Separate them with spaces and a plus sign")
        print("Please only use letters, numbers, ctrl, alt and shift otherwise you may encounter issues.")

        sneak_key = input('What key do you use to sneak? ')
        config_file.write(f"{sneak_key}\n")

        straight_bridge_hotkey = input("Enter your hotkey to activate straight bridge e.g. 'ctrl + b': ")
        config_file.write(f"{straight_bridge_hotkey}\n")

        diag_bridge_hotkey = input('Enter your hotkey to activate diagonal bridge: ')
        config_file.write(f"{diag_bridge_hotkey}\n")

        stop_key = input('Enter the key you want to hold to stop bridging (only 1 key): ')
        config_file.write(f"{stop_key}\n")
        print("Configuration complete, you can now use your hotkeys!")


pydirectinput.MINIMUM_DURATION = 0.01
def speed_bridge(sn_key, sb_keys, stop):
    #sneak before moving so that you don't fall off
    pydirectinput.keyDown(sn_key, _pause=False)
    time.sleep(0.05)
    pydirectinput.keyDown(sb_keys[0], _pause=False)
    pydirectinput.keyDown(sb_keys[1], _pause=False)
        #bridge infinitely until stop button pressed:
    while True:
        #hold down shift for 0.1 seconds then right click to place block
        pydirectinput.keyDown(sn_key, _pause=False)
        time.sleep(0.1)
        pydirectinput.rightClick(_pause=False)
        pydirectinput.keyUp(sn_key, _pause=False)
        pydirectinput.keyUp(sn_key, _pause=False)
        #if stop key is pressed break the loop
        if keyboard.is_pressed(stop):
            break
        #otherwise walk for 0.2 seconds
        else:
            time.sleep(0.2)
    pydirectinput.keyUp(sb_keys[0], _pause=False)
    pydirectinput.keyUp(sb_keys[1], _pause=False)


def diagonal_bridge(sn_key, stop):
    # sneak before moving so that you don't fall off
    pydirectinput.keyDown(sn_key, _pause=False)
    time.sleep(0.05)
    # hold down s
    pydirectinput.keyDown('s', _pause=False)
    while True:
        # hold down shift for 0.15 seconds then right click to place blocks
        pydirectinput.keyDown(sn_key, _pause=False)
        time.sleep(0.18)
        pydirectinput.click(_pause=False, clicks=2, button='right', interval=0.05)
        pydirectinput.keyUp(sn_key, _pause=False)
        # release the initial shift
        pydirectinput.keyUp(sn_key, _pause=False)
        # if stop key is pressed break the loop
        if keyboard.is_pressed(stop):
            break
        # otherwise walk for 0.25 seconds
        else:
            time.sleep(0.25)
    pydirectinput.keyUp('s', _pause=False)
"""
def one_stack():
    pydirectinput.keyDown('shift', _pause=False)
    time.sleep(0.05)
    with pydirectinput.hold(['s', 'd'], _pause=False):
        while True:
            with pydirectinput.hold('shift', _pause=False):
                pydirectinput.press('space', _pause=False)
            pydirectinput.keyUp('shift', _pause=False)
            with pydirectinput.hold('shift', _pause=False):
                pydirectinput.click(_pause=False, clicks=2, button='right', interval=0.05)
            if keyboard.is_pressed('k'):
                break
"""


with open('bridgerconfig.txt', 'r') as config_file:
    sbk_string = config_file.readline().strip()
    straight_bridge_keys = sbk_string.split(',')

    sneak_key = config_file.readline().strip()

    straight_bridge_hotkey = config_file.readline().strip()

    diag_bridge_hotkey = config_file.readline().strip()

    stop_key = config_file.readline().strip()
    #hotkeys
    keyboard.add_hotkey(straight_bridge_hotkey, speed_bridge, args=[sneak_key, straight_bridge_keys, stop_key])
    keyboard.add_hotkey(diag_bridge_hotkey, diagonal_bridge, args=[sneak_key, stop_key])

#press end key to stop program
keyboard.wait('end')
