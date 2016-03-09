import json


def get_temperature_data():
    """Loads data from ``temperature.json`` and prepares it for consuming."""
    with open("temperature.json", 'r') as f:
        data = json.load(f)

    result = {
        city: sorted(
            [(temp, int(time)) for time, temp in datapoints.items()],
            key=lambda x: x[1])
        for city, datapoints in data.items()}
    return result


# Cache
TEMPERATURE_DATA = get_temperature_data()
