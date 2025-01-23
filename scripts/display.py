from machine import Pin, I2C
import ssd1306

# Sample data to display
# data = {('M41', 'H'): [{'planned': '2025-01-08T17:54:00+01:00', 'delay': None},
#                 {'planned': '2025-01-08T18:04:00+01:00', 'delay': None}],
#  ('M41', 'S'): [{'planned': '2025-01-08T17:52:00+01:00', 'delay': 120},
#                 {'planned': '2025-01-08T17:57:00+01:00', 'delay': None},
#                 {'planned': '2025-01-08T18:02:00+01:00', 'delay': -120},
#                 {'planned': '2025-01-08T18:06:00+01:00', 'delay': None}],
#  ('M43', 'N'): [{'planned': '2025-01-08T17:52:00+01:00', 'delay': 60},
#                 {'planned': '2025-01-08T17:53:00+01:00', 'delay': 60},
#                 {'planned': '2025-01-08T18:03:00+01:00', 'delay': 60},
#                 {'planned': '2025-01-08T18:04:00+01:00', 'delay': 60}],
#  ('M43', 'W'): [{'planned': '2025-01-08T17:50:00+01:00', 'delay': 0},
#                 {'planned': '2025-01-08T17:57:00+01:00', 'delay': None},
#                 {'planned': '2025-01-08T18:00:00+01:00', 'delay': None},
#                 {'planned': '2025-01-08T18:06:00+01:00', 'delay': None},
#                 {'planned': '2025-01-08T18:09:00+01:00', 'delay': None}]}

# ESP32 Pin assignment and display initialisation
i2c = I2C(0, scl=Pin(6), sda=Pin(7))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Prepare entries to be displayed
def create_displayable_entries(bus_data):
    """Returns a table of strings, ready to be displayed."""

    display_entries = []

    # LIAM COMMENT
    # You're able to destruct tuples to avoid having to do index lookups
    # This can actually be applied to tuples, lists and anything which 
    # implements index lookups e.g. my_list[0]
    for ((bus_number, bus_direction), schedules) in bus_data.items(): 
        
        # This looks like a great place for a function to remove the repeated code blocks
        first_time = schedules[0]['planned'][14:16]
        first_delay = int(schedules[0]['delay']/60) if schedules[0]['delay'] is not None else 0
        first_calculated_time = f"{first_time}" + "+" + f"{first_delay}" if first_delay > 0 else first_time

        second_time = schedules[1]['planned'][14:16]
        second_delay = int(schedules[1]['delay']/60) if schedules[1]['delay'] is not None else 0
        second_calculated_time = f"{second_time}" + "+" + f"{second_delay}" if second_delay > 0 else second_time

        display_entries.append(f"{bus_number}({bus_direction}) {first_calculated_time} {second_calculated_time}")
        
        print("Content of displayable entries: ")
        print(display_entries)
    
    return display_entries

def display(displayable_entries):
    """Displays the entries on the screen."""

    oled.text('BVG companion ', 1, 1)

    for i, entry in enumerate(displayable_entries):
        oled.text(entry, 1, 18 + 13*i)

    oled.show()
