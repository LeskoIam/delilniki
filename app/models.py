__author__ = 'Lesko'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.
from app import db


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    location = db.Column(db.String(64), index=True)
    type = db.Column(db.String(64), index=True)
    data_points = db.relationship('SensorData', backref='sensor', lazy='dynamic')

    def __init__(self, name, location, type):
        self.name = name
        self.location = location
        self.type = type

    def __repr__(self):
        return '<Sensor %r>' % self.name


class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Integer())
    unit = db.Column(db.String(32), index=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

    def __init__(self, timestamp, value, unit, sensor_id):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit
        self.sensor_id = sensor_id

    def __repr__(self):
        return '<SensorData %r %r %r>' % (self.id, self.value, self.unit)