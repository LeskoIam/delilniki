__author__ = 'Lesko'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.
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