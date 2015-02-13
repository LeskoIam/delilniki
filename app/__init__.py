from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

if __name__ == '__main__':
    # out = db.session.query(models.SensorData, models.Sensor).\
    #     join(models.Sensor).order_by(models.SensorData.timestamp).order_by(models.Sensor.type)

    # out = db.session.query(models.SensorData, models.Sensor).\
    #     join(models.Sensor).filter(models.Sensor.type == "delilnik").\
    #     filter(models.Sensor.location == "hodnik").order_by(models.SensorData.timestamp.desc()).limit(1)

    # out = db.session.query(models.SensorData.value, models.SensorData.timestamp).\
    #     join(models.Sensor).filter(models.Sensor.type == "delilnik").\
    #     filter(models.Sensor.location == "soba").order_by(models.SensorData.timestamp.asc())

    # out = db.session.query(models.SensorData.timestamp).\
    #     order_by(models.SensorData.timestamp.desc()).limit(1)
    #
    # out1 = db.session.query(models.SensorData.value,
    #                         models.SensorData.timestamp,
    #                         models.Sensor.location).\
    #     join(models.Sensor).filter(models.SensorData.timestamp == out)

    # now = datetime.today()
    # date_object = timedelta(days=3)
    # search_date = now - date_object
    # out = db.session.query(models.SensorData.value, models.SensorData.timestamp).\
    #     join(models.Sensor).\
    #     filter(models.Sensor.type == "merilna ura").\
    #     filter(models.Sensor.location == "hodnik").\
    #     filter(models.Sensor.name == "topla voda").\
    #     filter(models.SensorData.timestamp >= search_date).\
    #     order_by(models.SensorData.timestamp.asc())

    import datetime
    start_of_month = datetime.date(datetime.datetime.today().year, datetime.datetime.today().month, 1)
    print start_of_month
    out = db.session.query(db.func.max(models.SensorData.value) - db.func.min(models.SensorData.value)).\
        filter(models.SensorData.timestamp >= start_of_month).\
        filter(models.SensorData.sensor_id == 4).\
        order_by(models.SensorData.timestamp.desc())

    print out
    for a in out.all():
        print a
    print "----------"
    pass