#!/usr/bin/env python
# coding=utf-8
import sys
from time import sleep

from lifxlan import GREEN, LifxLAN, ORANGE, RED, YELLOW


def main():
    num_lights = 1

    print("Discovering lights...")
    lifx = LifxLAN(num_lights)

    # get devices
    devices = lifx.get_lights()
    bulb = devices[0]
    print("Selected {}".format(bulb.get_label()))

    # get original state
    print("Turning on all lights...")
    original_power = bulb.get_power()
    original_color = bulb.get_color()
    bulb.set_power("on")

    sleep(2) # for looks

    print("Smooth slow rainbow")
    rainbow(bulb, 6, smooth=True)

    print("Restoring original power and color...")
    # restore original power
    bulb.set_power(original_power)
    # restore original color
    sleep(1) # for looks
    bulb.set_color(original_color)

def rainbow(bulb, duration_secs=1, smooth=False):
    colors = [GREEN, YELLOW, ORANGE, RED]
    transition_time_ms = duration_secs*1000 if smooth else 0
    rapid = True if duration_secs < 1 else False
    for color in colors:
        bulb.set_color(color, transition_time_ms, rapid)
        sleep(duration_secs)

if __name__=="__main__":
    main()