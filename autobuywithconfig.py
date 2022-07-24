#This new version of bedwarsautobuy allows you to configure your macros without editing the code itself!
#Macro information will be saved in the autobuyconfig.txt file
#You will be asked to configure macros the first time you run, then macros will be saved for subsequent runs
#If you want to reconfigure, delete the autobuyconfig.txt file and run the program again
#pip install pyautogui and keyboard before using
"""The config file format is as follows:
<number of macros>
<name of macro 1>
<number of items in the macro>
<item>,<number of times to buy>
<item>,<number of times to buy> (if buying more than 1 item(
...
<name of macro 2> (if configuring more than 1 macro)
...
"""
import pyautogui as pyautogui
import keyboard
import os.path

pyautogui.MINIMUM_DURATION = 0.05
class Item:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    def __repr__(self):
        return self.name
    def buy(self, num_items):
        pyautogui.moveTo(self.x, self.y)
        pyautogui.click(clicks=num_items, interval = 0.05)
class BuyMacro:
    def __init__(self, item_dict):
        self.item_list = list(item_dict.keys())
        self.item_nums = list(item_dict.values())
    def autobuy(self):
        for i in range(len(self.item_list)):
            self.item_list[i].buy(self.item_nums[i])
if not os.path.isfile("./autobuyconfig.txt"):
    with open('autobuyconfig.txt', 'w') as config_file:
        num_macros = int(input("How many buy macros would you like to set up?" ))
        config_file.write(str(num_macros))
        config_file.write('\n')
        for i in range(num_macros):
            macro_name = input('Name your macro (no spaces, make sure it is a unqiue name): ')
            config_file.write(f"{macro_name}\n")


            items = input("Input list of items you want to buy, separated by commas and all lowercase with underscores for spaces: ")
            item_list = [item.strip() for item in items.split(",")]
            config_file.write(f"{len(item_list)}\n")


            item_counts = input("Input list of item counts in the same order as the items, separated by commas: ")
            item_count_list = [count.strip() for count in item_counts.split(",")]
            for item, count in zip(item_list, item_count_list):
                config_file.write(f"{item},{count}\n")
            hotkey = input("Enter the hotkey to activate this macro, e.g. 'shift + b' ")
            config_file.write(f"{hotkey}\n")
        print("Configuration complete, you can now use your hotkeys!")

wool = Item("wool", 852, 441)
ladder = Item("ladder", 854, 510)
iron_sword = Item("iron_sword", 885, 478)
stone_sword = Item("stone_sword", 885, 443)
golden_apple = Item("golden_apple", 1069, 434)
pickaxe = Item("pickaxe", 955, 480)
axe = Item("axe", 955, 515)
item_list = [wool, ladder, iron_sword, stone_sword, golden_apple, pickaxe, axe]


def identify_item_obj(itemstr):
    for item_obj in item_list:
        if itemstr == item_obj.name:
            return item_obj
with open('autobuyconfig.txt', 'r') as config_file:
    num_macros = config_file.readline()
    for i in range(int(num_macros)):
        macro_name = config_file.readline().strip()
        num_items = config_file.readline().strip()
        item_dict = {}

        for x in range(int(num_items)):
            item_string, count = config_file.readline().split(',')
            item = identify_item_obj(item_string)
            item_dict[item] = int(count.strip())

        macro_setup_code = "{macro_name} = BuyMacro({item_dict})".format(macro_name = macro_name, item_dict = item_dict)
        exec(macro_setup_code)
        hotkey = config_file.readline().strip()
        exec(f"def {macro_name}_func():\n"
             f"    {macro_name}.autobuy()")
        exec(f"keyboard.add_hotkey('{hotkey}', {macro_name}_func)")


#stop the keyboard listener
keyboard.wait('end')