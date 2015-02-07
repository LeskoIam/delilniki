__author__ = 'Lesko'

from flask.ext.wtf import Form
from wtforms import FloatField
from wtforms.validators import Optional


class MeasurePointsForm(Form):
    kuhinja = FloatField("kuhinja", validators=[Optional()])
    hodnik = FloatField("hodnik", validators=[Optional()])
    kopalnica = FloatField("kopalnica", validators=[Optional()])
    soba = FloatField("soba", validators=[Optional()])
    hladna_voda = FloatField("hladna_voda", validators=[Optional()])
    topla_voda = FloatField("topla_voda", validators=[Optional()])


class ShowSelectForm(Form):
    test = FloatField("test", validators=[Optional()])