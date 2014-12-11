__author__ = 'Lesko'

from flask.ext.wtf import Form
from wtforms import FloatField
from wtforms.validators import InputRequired


class MeasurePointsForm(Form):
    kuhinja = FloatField("kuhinja", validators=[InputRequired()])
    hodnik = FloatField("hodnik", validators=[InputRequired()])
    kopalnica = FloatField("kopalnica", validators=[InputRequired()])
    soba = FloatField("soba", validators=[InputRequired()])
    hladna_voda = FloatField("hladna_voda", validators=[InputRequired()])
    topla_voda = FloatField("topla_voda", validators=[InputRequired()])