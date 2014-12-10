__author__ = 'Lesko'

from flask.ext.wtf import Form
from wtforms import FloatField  # StringField  # , BooleanField
from wtforms.validators import DataRequired, InputRequired


class MeasurePointsForm(Form):
    kuhinja = FloatField("kuhinja", validators=[InputRequired()])
    hodnik = FloatField("hodnik", validators=[InputRequired()])
    kopalnica = FloatField("kopalnica", validators=[InputRequired()])
    soba = FloatField("soba", validators=[InputRequired()])
    hladna_voda = FloatField("hladna_voda", validators=[InputRequired()])
    topla_voda = FloatField("topla_voda", validators=[InputRequired()])
    # remember_me = BooleanField('remember_me', default=False)