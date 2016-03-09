import json
import sys

from flask import Flask
from flask import request

from datasets import TEMPERATURE_DATA

app = Flask("MimicGraphiteApi")


@app.route("/metrics", methods=["GET"])
@app.route("/metrics/find", methods=["GET"])
def metrics_find():
    query = request.args.get('query')
    metrics = []
    if query == "*":
        metrics = [{"text": "temperature", "expandable": True}]
    elif query == "temperature.*":
        metrics = [{"text": "kyiv", "expandable": False},
                   {"text": "odesa", "expandable": False}]
    return json.dumps(metrics)


@app.route("/render", methods=["GET", "POST"])
def render():
    target = request.form.getlist('target') or []

    # Extend to the date boundaries by one day to make graph consistent.
    from_ = int(request.form.get('from')) - 86400
    until = int(request.form.get('until')) + 86400

    # This option is not taken into account, since Grafana requests for maximum
    # 1920 data points and the mimic backend doesn't provide more than 70.
    # max_data_points = int(request.form.get('maxDataPoints'))

    data = {
        city: [(temp, time) for temp, time in datapts if from_ <= time <= until]
        for city, datapts in TEMPERATURE_DATA.items()}

    response = []

    temp_kyiv = {'target': 'Temperature in Kyiv, Ukraine (Celsius)',
                 'datapoints': data['Kyiv']}
    temp_odesa = {'target': 'Temperature in Odesa, Ukraine (Celsius)',
                  'datapoints': data['Odesa']}
    abs_temp_kyiv = {
        'target': 'Absolute temperature in Kyiv, Ukraine (Celsius)',
        'datapoints': [(abs(k), v) for k, v in data['Kyiv']]}

    abs_temp_odesa = {
        'target': 'Absolute temperature in Odesa, Ukraine (Celsius)',
        'datapoints': [(abs(k), v) for k, v in data['Odesa']]}

    if "*" in target:
        response += [temp_kyiv, temp_odesa, abs_temp_kyiv, abs_temp_odesa]

    if "temperature.*" in target:
        response += [temp_kyiv, temp_odesa]

    if "absolute(temperature.*)" in target:
        response += [abs_temp_kyiv, abs_temp_odesa]

    if "temperature.kyiv" in target:
        response.append(temp_kyiv)

    if "temperature.odesa" in target:
        response.append(temp_odesa)

    if "absolute(temperature.kyiv)" in target:
        response.append(abs_temp_kyiv)

    if "absolute(temperature.odesa)" in target:
        response.append(abs_temp_odesa)
    return json.dumps(response)


if __name__ == '__main__':

    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError:
        print(
            "Mimic Graphite API server execution options:\n\n{0} HOST PORT\n".
            format(sys.argv[0]))
        sys.exit(1)

    app.run(host=host, port=port)
    print(u"Mimic Graphite API server is running on {0}:{1}".format(host, port))
