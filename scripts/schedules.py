import urequests as requests

base_schedule_url = 'http://v6.bvg.transport.rest/stops/STATION/departures?duration=20&linesOfStops=false&remarks=true&language=en'
aggregated_buses = {}

def get_departure_data_from_bvg(stations):

    """Calls the BVG API for each of the stations provided and returns a list of all the departures
     at the provided stations. Format is most likely BVG-specific. """

    departure_data = []

    for station in stations:
        station_url = base_schedule_url.replace("STATION", station)
        response = requests.get(station_url)
        data = response.json()

        departure_data.extend(data['departures'])
    
    return departure_data

def normalize_departures(departures):

    """
    Return aggregated results in the form:
    BusNumber(BusDirection) [Time & delay, Time & delay, ...]
    
    """

    for departure in departures:

            # Extract desired properties
            bus_number = departure['line']['name']
            bus_direction = departure['direction']
            bus_direction_mapping = {
                'Eichenstr./Puschkinallee':'N',
                'U Berliner Str.': 'W', 
                'Stralau, Tunnelstr.': 'N',
                'U Boddinstr.': 'W',
                'S+U Hauptbahnhof': 'H',
                'Sonnenallee/Baumschulenstr.':'S'
                # 'S Schöneweide': 
            }
            bus_direction_normalized = bus_direction_mapping.get(bus_direction, "?")
            bus_planned_time = departure['plannedWhen']
            bus_delay = departure['delay']

            # Form aggregated results to return
            if (bus_number, bus_direction_normalized) not in aggregated_buses:
                aggregated_buses[bus_number, bus_direction_normalized] = []
            aggregated_buses[bus_number, bus_direction_normalized].append({'planned': bus_planned_time, 'delay': bus_delay})

    return aggregated_buses

def sort_results(results):
    sorted_buses_data = {}

    for (key, times) in sorted(results.items()):

        sorted_times = sorted(times, key= lambda x: x['planned'])

        sorted_buses_data[key] = sorted_times

    return sorted_buses_data

def filter_out_bus_lines(results):

    for key in list(results.keys()):
        if key[0] not in ('M41', 'M43') or key[1] == "?":
            del results[key]

    return results