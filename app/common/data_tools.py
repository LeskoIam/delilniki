__author__ = 'Lesko'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.
from app import db
from app.models import SensorData, Sensor
from sqlalchemy import distinct
import datetime
import calendar
import num_tools


def get_heat_data(location):
    out = db.session.query(SensorData.value, SensorData.timestamp). \
        join(Sensor).filter(Sensor.type == "delilnik"). \
        filter(Sensor.location == location).order_by(SensorData.timestamp.asc())
    return out.all()


def get_water_data(hot_cold):
    out = db.session.query(SensorData.value, SensorData.timestamp). \
        join(Sensor).filter(Sensor.type == "merilna ura"). \
        filter(Sensor.location == "hodnik").filter(Sensor.name == hot_cold). \
        order_by(SensorData.timestamp.asc())
    return out.all()


def get_sensor_ids(heat_or_water):
    if heat_or_water.lower() == "heat":
        s_type = "delilnik"
    elif heat_or_water.lower() == "water":
        s_type = "merilna ura"
    else:
        raise AttributeError("'{t}' is not OK! Use 'heat' or 'water'".format(t=heat_or_water))
    out = db.session.query(distinct(Sensor.id)). \
        filter(Sensor.type == s_type)
    out = [x[0] for x in out.all()]
    return out


def get_sensor_location(s_id):
    out = db.session.query(Sensor.location). \
        filter(Sensor.id == s_id)
    return out.all()[0][0]


def get_sensor_type(s_id):
    out = db.session.query(Sensor.type). \
        filter(Sensor.id == s_id)
    return out.all()[0][0]


def get_sensor_name(s_id):
    out = db.session.query(Sensor.name). \
        filter(Sensor.id == s_id)
    return out.all()[0][0]


def get_last_readings(sensor_ids):
    d = {}
    for s_id in sensor_ids:
        out = db.session.query(SensorData.value,
                               Sensor.location,
                               Sensor.name). \
            join(Sensor). \
            filter(SensorData.sensor_id == s_id).order_by(SensorData.timestamp.desc()).limit(1)
        for dat in out.all():
            if "deliln" in dat.name:
                d[dat.location] = dat.value
            else:
                d[dat.name] = dat.value
    return d


def get_ndays_back_mean(heat_or_water, n_days):
    s_ids = get_sensor_ids(heat_or_water)
    start_date = datetime.datetime.today()
    date_object = datetime.timedelta(days=n_days)
    end_date = start_date - date_object
    d = {}
    for s_id in s_ids:
        location = get_sensor_location(s_id)
        s_name = get_sensor_name(s_id)
        out = db.session.query(SensorData.timestamp, SensorData.value). \
            filter(SensorData.timestamp >= end_date). \
            filter(SensorData.timestamp <= start_date).\
            filter(SensorData.sensor_id == s_id)
        out = out.all()
        data = [x[1] for x in out]
        time_delta = [x[0] for x in out]
        data, _, dt = num_tools.running_consumption(data, time_delta)
        data = num_tools.mean(data)
        if heat_or_water == "heat":
            d[location] = data
        else:
            d[s_name] = data
    return d


def get_this_month_consumption(heat_or_water):
    s_ids = get_sensor_ids(heat_or_water)
    start_of_month = datetime.date(datetime.datetime.today().year,
                                   datetime.datetime.today().month,
                                   1)
    d = {}
    for s_id in s_ids:
        location = get_sensor_location(s_id)
        s_name = get_sensor_name(s_id)
        out = db.session.query(db.func.max(SensorData.value) - db.func.min(SensorData.value)). \
            filter(SensorData.timestamp >= start_of_month). \
            filter(SensorData.sensor_id == s_id). \
            order_by(SensorData.timestamp.desc())
        consumption = out.all()[0][0]
        if heat_or_water == "heat":
            d[location] = consumption
        else:
            d[s_name] = consumption
    return d


def get_predicted_month_consumption(heat_or_water):
    data = get_ndays_back_mean(heat_or_water, 30)
    used = get_this_month_consumption(heat_or_water)
    out = {}
    for d in data:
        already_used = used[d]
        consumption_rate = data[d]
        month = datetime.datetime.today().month
        month_days = calendar.monthrange(datetime.datetime.today().year, month)[1]
        today = datetime.datetime.today().day
        predict = (consumption_rate * (month_days - today)) + already_used
        if "heat" in heat_or_water:
            out[d] = int(round(predict))
        else:
            out[d] = round(predict, 3)
    return out


def get_previous_month_consumption(heat_or_water):
    s_ids = get_sensor_ids(heat_or_water)
    month = datetime.datetime.today().month
    month -= 1
    year = datetime.datetime.today().year
    if month < 1:
        month = 12
        year -= 1
    start_of_month = datetime.date(year,
                                   month,
                                   1)
    end_of_month = datetime.date(datetime.datetime.today().year,
                                 month,
                                 calendar.monthrange(datetime.datetime.today().year,
                                                     month)[1])
    d = {}
    for s_id in s_ids:
        location = get_sensor_location(s_id)
        s_name = get_sensor_name(s_id)
        out = db.session.query(db.func.max(SensorData.value) - db.func.min(SensorData.value)). \
            filter(SensorData.timestamp >= start_of_month). \
            filter(SensorData.timestamp <= end_of_month).\
            filter(SensorData.sensor_id == s_id). \
            order_by(SensorData.timestamp.desc())
        consumption = out.all()[0][0]
        if heat_or_water == "heat":
            d[location] = consumption
        else:
            d[s_name] = consumption
    return d


if __name__ == '__main__':
    print """\na = get_water_data("topla voda")"""
    print get_water_data("topla voda")

    print """\na = get_water_data("topla voda")"""
    print get_water_data("hladna voda")

    print """\na = get_sensor_ids()"""
    a = get_sensor_ids(heat_or_water="heat")
    print a
    print """\na = get_last_readings_2(a)"""
    a = get_last_readings(a)
    print a

    print """\na = get_this_month_consumption("heat")"""
    a = get_this_month_consumption("heat")
    print a

    print """\na = get_this_month_consumption("water")"""
    a = get_this_month_consumption("water")
    print a

    print """\na = get_previous_month_consumption("water")"""
    a = get_previous_month_consumption("water")
    print a

    print """\na = get_previous_month_consumption("heat")"""
    a = get_previous_month_consumption("heat")
    print a

    print """\na = get_ndays_back_mean("heat", 30)"""
    a = get_ndays_back_mean("heat", 30)
    print a

    print """\na = get_ndays_back_mean("water", 30)"""
    a = get_ndays_back_mean("water", 30)
    print a

    print """\na = get_predicted_month_consumption("heat")"""
    a = get_predicted_month_consumption("heat")
    print a

    print """\na = get_predicted_month_consumption("water")"""
    a = get_predicted_month_consumption("water")
    print a