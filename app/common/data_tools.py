__author__ = 'Lesko'
from app import db
from app.models import SensorData, Sensor
from sqlalchemy import distinct


# def get_last_readings(heat_or_water):
#     heat = False
#     if heat_or_water.lower() == "heat":
#         s_type = "delilnik"
#         heat = True
#     elif heat_or_water.lower() == "water":
#         s_type = "merilna ura"
#     else:
#         raise AttributeError("'{t}' is not OK! Use 'heat' or 'water'".format(t=heat_or_water))
#     out = db.session.query(SensorData.timestamp).\
#         order_by(SensorData.timestamp.desc()).limit(1)
#
#     out1 = db.session.query(SensorData.value,
#                             Sensor.location,
#                             Sensor.name).\
#         join(Sensor).filter(SensorData.timestamp == out).filter(Sensor.type == s_type)
#     d = {}
#     for dat in out1.all():
#         if heat:
#             d[dat.location] = dat.value
#         else:
#             d[dat.name] = dat.value
#     return d


def get_heat_data(location):
    out = db.session.query(SensorData.value, SensorData.timestamp).\
        join(Sensor).filter(Sensor.type == "delilnik").\
        filter(Sensor.location == location).order_by(SensorData.timestamp.asc())
    return out.all()


def get_water_data(hot_cold):
    out = db.session.query(SensorData.value, SensorData.timestamp).\
        join(Sensor).filter(Sensor.type == "merilna ura").\
        filter(Sensor.location == "hodnik").filter(Sensor.name == hot_cold).\
        order_by(SensorData.timestamp.asc())
    return out.all()


def get_sensor_ids(heat_or_water):
    if heat_or_water.lower() == "heat":
        s_type = "delilnik"
    elif heat_or_water.lower() == "water":
        s_type = "merilna ura"
    else:
        raise AttributeError("'{t}' is not OK! Use 'heat' or 'water'".format(t=heat_or_water))
    out = db.session.query(distinct(Sensor.id)).\
        filter(Sensor.type == s_type)
    out = [x[0] for x in out.all()]
    return out


def get_last_readings(sensor_ids):
    d = {}
    for s_id in sensor_ids:
        out = db.session.query(SensorData.value,
                            Sensor.location,
                            Sensor.name).\
            join(Sensor).\
            filter(SensorData.sensor_id == s_id).order_by(SensorData.timestamp.desc()).limit(1)
        for dat in out.all():
            if "deliln" in dat.name:
                d[dat.location] = dat.value
            else:
                d[dat.name] = dat.value
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