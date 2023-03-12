# a script to take user input to choose a lighbulb and a lecture and then check every second against the LectureTemperature API in order to return a result and colour the bulb accordingly.

import json
import requests
from lifxlan import LifxLAN, GREEN, YELLOW, ORANGE, RED
from time import sleep
from tcapp.models import Module
import sys


def run():
    # get lights
    # assign one lightbulb for faster demo (would otherwise leave at None to let LifxLAN find all lights)
    num_lights = 1

    print("Discovering lights...")
    lifx = LifxLAN(num_lights)

    # get devices
    devices = lifx.get_lights()

    if not devices:
        sys.exit('No lightbulbs found.')

    # print out lights
    print("Found {} light(s):".format(len(devices)))
    for idx, device in enumerate(devices, start=1):
        try:
            # 2d ensures padding for 2 digits
            print(f'  {idx:2d}. {device.get_label()}')
        except:
            pass

    # have user select light
    idx = int(input("Select a lightbulb: "))
    bulb = devices[idx - 1]

    # get original state
    original_color = bulb.get_color()
    bulb.set_power("on")

    # Fetch modules
    modules = Module.objects.all()

    # print out module options and take in user input
    print("Which module would you like to select?")
    for idx, module in enumerate(modules, start=1):
        try:
            # 2d ensures padding for 2 digits
            print(f'  {idx:2d}. {module.module_shortname}')
        except:
            pass

    idx = int(input("Select a module: "))
    module = modules[idx - 1]

    print(f"You've selected module {module.module_shortname}")

    # print out lecture options and take in user input
    lectures = module.lecture_set.all()
    print("Which lecture would you like to select?")
    for idx, lecture in enumerate(lectures, start=1):
        try:
            # 2d ensures padding for 2 digits
            print(f'  {idx:2d}. {lecture.lecture_name}')
        except:
            pass

    idx = int(input("Select a lecture: "))
    lecture = lectures[idx - 1]

    print(f"You've selected lecture {lecture.lecture_name}")

    # connect to api to retrieve temp
    print("Checking current temperature...")
    while True:
        # format url string to handle variable: https://stackoverflow.com/questions/58944189/using-variable-in-an-api-request-in-python
        url = f'http://localhost:8000/tcapp/api/lectures/{lecture.lecture_name}/temperature'
        res = requests.get(url)
        response = json.loads(res.text)
        print(response)

        # set bulb color to response temperature
        if response == 0:
            bulb.set_color(GREEN)
        elif response == 1:
            bulb.set_color(YELLOW)
        elif response == 2:
            bulb.set_color(ORANGE)
        elif response == 3:
            bulb.set_color(RED)
        else:
            bulb.set_color(original_color)

        sleep(1)
