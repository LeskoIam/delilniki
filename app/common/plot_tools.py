__author__ = 'Lesko'
import pygal
from pygal.style import CleanStyle
from data_tools import get_heat_data, \
    get_water_data, \
    get_last_readings
from num_tools import running_consumption


def plot_last_heat_dividers():
    bar_chart = pygal.Bar(show_legend=False, width=600, height=300, explicit_size=True, style=CleanStyle,
                          y_labels_major_every=3, show_minor_y_labels=False)
    bar_chart.title = "Delilniki toplote [enot]"
    data_in = get_last_readings("heat")
    legend = []
    data = []
    for d in data_in:
        legend.append(d)
        data.append(data_in[d])
    bar_chart.add('Zadnji podatki', data)
    bar_chart.x_labels = legend
    return bar_chart.render(is_unicode=True)


def plot_last_water_counter():
    bar_chart = pygal.Bar(show_legend=False, width=600, height=300, explicit_size=True, style=CleanStyle,
                          y_labels_major_every=3, show_minor_y_labels=False)
    bar_chart.title = "Stevec vode [m3]"
    data_in = get_last_readings("water")
    legend = []
    data = []
    for d in data_in:
        legend.append(d)
        data.append(data_in[d])
    bar_chart.add('Zadnji podatki', data)
    bar_chart.x_labels = legend
    return bar_chart.render(is_unicode=True)


def plot_heat_consumption():
    locations = ["kuhinja", "hodnik", "kopalnica", "soba"]
    bar_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                           y_labels_major_every=2, show_minor_y_labels=False)
    bar_chart.title = "Poraba toplote [enot/dan]"
    for loc in locations:
        data_in = get_heat_data(loc)
        data = []
        time_delta = []
        for d in data_in:
            data.append(d[0])
            time_delta.append(d[1])
        data, _, dt = running_consumption(data, time_delta)
        bar_chart.add(loc, data)
    bar_chart.x_labels = map(str, dt)
    return bar_chart.render(is_unicode=True)


def plot_water_consumption():
    topla_hladna = get_water_data("topla voda"), get_water_data("hladna voda")
    topla_hladna_str = ["topla voda", "hladna voda"]
    bar_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                           y_labels_major_every=2, show_minor_y_labels=False)
    bar_chart.title = "Poraba vode [liter/dan]"
    for x, tp in enumerate(topla_hladna):
        cons = []
        timestamp = []
        for d in tp:
            cons.append(d[0] * 1000)
            timestamp.append(d[1])
        data, _, dt = running_consumption(cons, timestamp)
        bar_chart.add(topla_hladna_str[x], data)
    bar_chart.x_labels = map(str, dt)
    return bar_chart.render(is_unicode=True)


def plot_heat():
    locations = ["kuhinja", "hodnik", "kopalnica", "soba"]
    bar_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                           y_labels_major_every=2, show_minor_y_labels=False)
    bar_chart.title = "Delilniki toplote cez cas [enot]"
    for loc in locations:
        data_in = get_heat_data(loc)
        data = []
        timestamp = []
        for d in data_in:
            data.append(d[0])
            timestamp.append(d[1])
        bar_chart.add(loc, data)
    bar_chart.x_labels = [x.strftime("%Y-%m-%d %H:%M") for x in timestamp]
    return bar_chart.render(is_unicode=True)


def plot_water():
    topla_hladna = get_water_data("topla voda"), get_water_data("hladna voda")
    topla_hladna_str = ["topla voda", "hladna voda"]
    bar_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                           y_labels_major_every=2, show_minor_y_labels=False)
    bar_chart.title = "Stevec vode cez cas [m3]"
    for x, tp in enumerate(topla_hladna):
        data = []
        timestamp = []
        for d in tp:
            data.append(d[0])
            timestamp.append(d[1])
        bar_chart.add(topla_hladna_str[x], data)
    bar_chart.x_labels = [x.strftime("%Y-%m-%d %H:%M") for x in timestamp]
    return bar_chart.render(is_unicode=True)



if __name__ == '__main__':
    plot_heat_consumption()
    plot_water_consumption()

