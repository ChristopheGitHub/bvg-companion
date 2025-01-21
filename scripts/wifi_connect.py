import network
import time

def connect_to_wifi():

    print("Connecting to WiFi", end="")

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')

    # Attempt connection
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)

    print(" Connected!")