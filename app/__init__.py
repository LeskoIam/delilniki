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

    out = db.session.query(models.SensorData.timestamp).\
        order_by(models.SensorData.timestamp.desc()).limit(1)

    out1 = db.session.query(models.SensorData.value,
                            models.SensorData.timestamp,
                            models.Sensor.location).\
        join(models.Sensor).filter(models.SensorData.timestamp == out)

    print out1
    for a in out1.all():
        print a
    print "----------"