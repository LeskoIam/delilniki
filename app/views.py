__author__ = 'Lesko'
from flask import render_template, flash, redirect
from app import app, db
from .forms import MeasurePointsForm
from models import SensorData, Sensor
import datetime
import common.num_tools as num_tools
import common.plot_tools as plot_tools

@app.route('/')
@app.route('/index')
def index():
    data = {"title": title_handler()}
    return render_template("index.html",
                           data=data)


@app.route('/value_input', methods=['GET', 'POST'])
def value_input():
    data = {"title": title_handler("Value Input")}
    form = MeasurePointsForm()
    if form.validate_on_submit():
        # Kuhinja
        sensor_id_kuhinja = Sensor.query.filter_by(location="kuhinja", type="delilnik").first()
        timestamp = datetime.datetime.utcnow()
        data = SensorData(timestamp, form.kuhinja.data, None, sensor_id_kuhinja.id)
        db.session.add(data)

        # Hodnik
        sensor_id_hodnik = Sensor.query.filter_by(location="hodnik", type="delilnik").first()
        data = SensorData(timestamp, form.hodnik.data, None, sensor_id_hodnik.id)
        db.session.add(data)

        # Kopalnica
        sensor_id_kopalnica = Sensor.query.filter_by(location="kopalnica", type="delilnik").first()
        data = SensorData(timestamp, form.kopalnica.data, None, sensor_id_kopalnica.id)
        db.session.add(data)

        # Soba
        sensor_id_soba = Sensor.query.filter_by(location="soba", type="delilnik").first()
        data = SensorData(timestamp, form.soba.data, None, sensor_id_soba.id)
        db.session.add(data)

        # Topla voda
        sensor_id_topla_voda = Sensor.query.filter_by(location="hodnik",
                                                      type="merilna ura",
                                                      name="topla voda").first()
        data = SensorData(timestamp, form.topla_voda.data, "m3", sensor_id_topla_voda.id)
        db.session.add(data)

        # Hladna voda
        sensor_id_hladna_voda = Sensor.query.filter_by(location="hodnik",
                                                       type="merilna ura",
                                                       name="hladna voda").first()
        data = SensorData(timestamp, form.hladna_voda.data, "m3", sensor_id_hladna_voda.id)
        db.session.add(data)

        db.session.commit()
        flash("Uspesno ste vnesli podatke!")
        return redirect('/index')
    return render_template('input_form.html',
                           form=form,
                           data=data)


@app.route("/show")
def show():
    sensor_data = db.session.query(SensorData, Sensor).join(Sensor).order_by(SensorData.timestamp.desc()).order_by(Sensor.type)
    #print sensor_data[0][0].timestamp
    data = {"title": title_handler("Show All"),
            "plot_heat": plot_tools.plot_heat(),
            "plot_water": plot_tools.plot_water(),
            "plot_heat_dividers": plot_tools.plot_last_heat_dividers(),
            "plot_water_counter": plot_tools.plot_last_water_counter(),
            "plot_heat_consumption": plot_tools.plot_heat_consumption(),
            "plot_water_consumption": plot_tools.plot_water_consumption()}
    return render_template('show.html',
                           data=data,
                           sensor_data=sensor_data)


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