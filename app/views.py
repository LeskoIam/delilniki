__author__ = 'Lesko'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.
from flask import render_template, flash, redirect, Markup
from app import app, db
from models import SensorData, Sensor
import common.plot_tools as plot_tools
import common.data_tools as data_tools
import config
import os
import markdown

@app.route('/')
@app.route('/index')
def index():
    try:
        f = open(os.path.join(config.APP_ROOT, "README.md"), "r")
        text = f.read()
        text = Markup(markdown.markdown(text))
        f.close()
    except IOError:
        text = "Failed to load page content. Sorry..."
    data = {"title": title_handler(),
            "content": text}
    return render_template("index.html",
                           data=data)


@app.route("/value_input")
def value_input():
    data = {"title": title_handler("Show All")}
    return render_template("input_form.html", data=data)


@app.route("/show")
def show():
    sensor_data = db.session.query(SensorData, Sensor).join(Sensor).\
        order_by(SensorData.timestamp.desc()).order_by(Sensor.type).limit(18)
    month_water_consumption = data_tools.get_this_month_consumption("water")
    month_heat_consumption = data_tools.get_this_month_consumption("heat")
    trend_heat = data_tools.get_trends("heat")
    trend_water = data_tools.get_trends("water")
    previous_month_water = data_tools.get_previous_month_consumption("water")
    previous_month_heat = data_tools.get_previous_month_consumption("heat")
    data = {"title": title_handler("Show All"),

            "plot_heat": plot_tools.plot_heat(),
            "plot_water": plot_tools.plot_water(),
            # "plot_heat_dividers": plot_tools.plot_last_heat_dividers(),
            # "plot_water_counter": plot_tools.plot_last_water_counter(),
            "plot_heat_consumption": plot_tools.plot_heat_consumption(),
            "plot_water_consumption": plot_tools.plot_water_consumption(),

            "month_water_consumption": month_water_consumption,
            "month_heat_consumption": month_heat_consumption,
            "previous_month_water_consumption": previous_month_water,
            "previous_month_heat_consumption": previous_month_heat,
            # "predict_month_heat_consumption": data_tools.get_predicted_month_consumption("heat"),
            # "predict_month_water_consumption": data_tools.get_predicted_month_consumption("water"),
            "trend_heat": trend_heat,
            "trend_water": trend_water,
            "sum_month_heat": sum([x for x in month_heat_consumption.values()]),
            "sum_month_water": sum([x for x in month_water_consumption.values()]),
            "sum_predict_water": sum([x["prediction"] for x in trend_water.values()]),
            "sum_predict_heat": sum([x["prediction"] for x in trend_heat.values()]),
            "sum_last_water": sum([x for x in previous_month_water.values()]),
            "sum_last_heat": sum([x for x in previous_month_heat.values()]),

            "css": "show.css"}
    return render_template('show.html',
                           data=data,
                           sensor_data=sensor_data)
@app.route("/more")
def more():
    data = {"title": title_handler("More")}
    return render_template('more.html',
                           data=data)

#########################################################
#########################################################


def title_handler(subtitle=None):
    main = "Delilniki"
    if subtitle is None:
        return main
    return "{main}-{sub}".format(main=main,
                                 sub=subtitle)

if __name__ == '__main__':
    print title_handler()
    print title_handler("lesko")