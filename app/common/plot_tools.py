__author__ = 'Lesko'
import pygal
from pygal.style import CleanStyle
import data_tools
import num_tools


def plot_last_heat_dividers():
    bar_chart = pygal.Bar(show_legend=False, width=600, height=300, explicit_size=True, style=CleanStyle,
                          y_labels_major_every=3, show_minor_y_labels=False)
    bar_chart.title = "Delilniki toplote - zadnje stanje [enot]"
    data_in = data_tools.get_last_readings("heat")
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
    bar_chart.title = "Stevec vode - zadnje stanje [m3]"
    data_in = data_tools.get_last_readings("water")
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
    line_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                            y_labels_major_every=2, show_minor_y_labels=False)
    line_chart.title = "Poraba toplote [enot/dan]"
    text = "<hr>Povprecna poraba [enot/dan]<br />"
    for loc in locations:
        data_in = data_tools.get_heat_data(loc)
        data = []
        time_delta = []
        for d in data_in:
            data.append(d[0])
            time_delta.append(d[1])
        data, _, dt = num_tools.running_consumption(data, time_delta)
        line_chart.add(loc, data)
        text += loc.capitalize() + ": %3.3f<br />" % num_tools.mean(data)
    line_chart.x_labels = map(str, dt)
    out = "<div id=\"plot\">"
    out += line_chart.render(is_unicode=True) + "<br />" + text
    out += "</div>"
    return out


def plot_water_consumption():
    topla_hladna = data_tools.get_water_data("topla voda"), data_tools.get_water_data("hladna voda")
    topla_hladna_str = ["topla voda", "hladna voda"]
    line_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                            y_labels_major_every=2, show_minor_y_labels=False)
    line_chart.title = "Poraba vode [liter/dan]"
    text = "<hr>Povprecna poraba [liter/dan]<br />"
    for x, tp in enumerate(topla_hladna):
        cons = []
        timestamp = []
        for d in tp:
            cons.append(d[0] * 1000)
            timestamp.append(d[1])
        data, _, dt = num_tools.running_consumption(cons, timestamp)
        line_chart.add(topla_hladna_str[x], data)
        text += topla_hladna_str[x].capitalize() + ": %3.3f<br />" % num_tools.mean(data)
    line_chart.x_labels = map(str, dt)
    out = "<div id=\"plot\">"
    out += line_chart.render(is_unicode=True) + "<br />" + text
    out += "</div>"
    return out


def plot_heat():
    locations = ["kuhinja", "hodnik", "kopalnica", "soba"]
    line_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                            y_labels_major_every=2, show_minor_y_labels=False,
                            x_label_rotation=35)
    line_chart.title = "Delilniki toplote - cez cas [enot]"
    for loc in locations:
        data_in = data_tools.get_heat_data(loc)
        data = []
        timestamp = []
        for d in data_in:
            data.append(d[0])
            timestamp.append(d[1])
        line_chart.add(loc, data)
    line_chart.x_labels = [x.strftime("%Y-%m-%d %H:%M") for x in timestamp]
    return line_chart.render(is_unicode=True)


def plot_water():
    topla_hladna = data_tools.get_water_data("topla voda"), data_tools.get_water_data("hladna voda")
    topla_hladna_str = ["topla voda", "hladna voda"]
    line_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                            y_labels_major_every=2, show_minor_y_labels=False,
                            x_label_rotation=35)
    line_chart.title = "Stevec vode - cez cas [m3]"
    for x, tp in enumerate(topla_hladna):
        data = []
        timestamp = []
        for d in tp:
            data.append(d[0])
            timestamp.append(d[1])
        line_chart.add(topla_hladna_str[x], data)
    line_chart.x_labels = [x.strftime("%Y-%m-%d %H:%M") for x in timestamp]
    return line_chart.render(is_unicode=True)


if __name__ == '__main__':
    plot_heat_consumption()
    plot_water_consumption()