__author__ = 'Lesko'
from app import db
from app.models import SensorData, Sensor


def get_last_readings(heat_or_water):
    heat = False
    if heat_or_water.lower() == "heat":
        s_type = "delilnik"
        heat = True
    elif heat_or_water.lower() == "water":
        s_type = "merilna ura"
    else:
        raise AttributeError("'{t}' is not OK use 'heat' or 'water'".format(t=heat_or_water))
    out = db.session.query(SensorData.timestamp).\
        order_by(SensorData.timestamp.desc()).limit(1)

    out1 = db.session.query(SensorData.value,
                            Sensor.location,
                            Sensor.name).\
        join(Sensor).filter(SensorData.timestamp == out).filter(Sensor.type == s_type)
    d = {}
    for dat in out1.all():
        if heat:
            d[dat.location] = dat.value
        else:
            d[dat.name] = dat.value
    return d


def get_heat_consumption(location):
    out = db.session.query(SensorData.value, SensorData.timestamp).\
        join(Sensor).filter(Sensor.type == "delilnik").\
        filter(Sensor.location == location).order_by(SensorData.timestamp.asc())
    return out.all()


def get_water_consumption_data(hot_cold):
    out = db.session.query(SensorData.value, SensorData.timestamp).\
        join(Sensor).filter(Sensor.type == "merilna ura").\
        filter(Sensor.location == "hodnik").filter(Sensor.name == hot_cold).order_by(SensorData.timestamp.asc())
    return out.all()

if __name__ == '__main__':

    print get_water_consumption_data("topla voda")
    print get_water_consumption_data("hladna voda")

    a = get_last_readings("heat")
    print a, type(a)

    a = get_last_readings("water")
    print a, type(a)
    # d = {}
    # for x in a:
    #     d[x.location] = x.value
    # print d