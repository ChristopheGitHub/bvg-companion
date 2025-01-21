# SPDX-License-Identifier: MIT
import sys
import machine
from machine import Pin, SPI  # type: ignore
import time
import requests
from time import sleep

import wifi_connect
import schedules
import display


# Diagram of the circuit: https://wokwi.com/projects/417541800209963009

# Basic initial informatino on the board.
machine.freq(80000000) # set the CPU frequency to 80 MHz - because we sustainable yo
print("Starting!")
board = sys.implementation._machine.split(' with')[0]
print(f"Running on {board} ({sys.platform}) at {machine.freq() / 1000000} MHz")

# Connect to WiFi
wifi_connect.connect_to_wifi()


# Plug into motion detector
motion_sensor = Pin(2, Pin.IN)  # GPIO 2 as input

# Stations 
stations = [
    '900075151',    # Wildenbruch
    '900075101'     # Erkstr
]

def display_new_departures(stations):

    # print("Start fetching data")
    departures = schedules.get_departure_data_from_bvg(stations)
    # print("get_departure_data_from_bvg completed")

    normalized_departures = schedules.normalize_departures(departures)
    # print("normalize_departures completed")
    # print(normalized_departures)

    filtered_results = schedules.filter_out_bus_lines(normalized_departures)
    # print("filter_out_bus_lines completed")
    # print(filtered_results)

    sorted_results = schedules.sort_results(filtered_results)
    # print("sort_results completed")
    # print(sorted_results)

    displayable_entries = display.create_displayable_entries(sorted_results)
    # print("create_displayable_entries completed")
    # print(displayable_entries)

    display.display(displayable_entries)


while True:
    if motion_sensor.value() == 1:  # Motion detected
        print("Motion detected!")
        display_new_departures(stations)
    else:
        # print("No motion...")
        time.sleep(1)  # Delay to avoid rapid polling
