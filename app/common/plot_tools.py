__author__ = 'Lesko'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.
import pygal
from pygal.style import CleanStyle
import data_tools
import num_tools


def plot_last_heat_dividers():
    bar_chart = pygal.Bar(show_legend=False, width=600, height=300, explicit_size=True, style=CleanStyle,
                          y_labels_major_every=3, show_minor_y_labels=False)
    bar_chart.title = "Ogrevanje - zadnje stanje [enot]"
    data_in = data_tools.get_last_readings(data_tools.get_sensor_ids("heat"))
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
    data_in = data_tools.get_last_readings(data_tools.get_sensor_ids("water"))
    legend = []
    data = []
    for d in data_in:
        legend.append(d)
        data.append(data_in[d])
    bar_chart.add('Zadnji podatki', data)
    bar_chart.x_labels = legend
    return bar_chart.render(is_unicode=True)


def plot_water_consumption():
    topla_hladna = data_tools.get_water_data("topla voda"), data_tools.get_water_data("hladna voda")
    topla_hladna_str = ["topla voda", "hladna voda"]
    line_chart0 = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                             y_labels_major_every=2, show_minor_y_labels=False)
    line_chart1 = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                             y_labels_major_every=2, show_minor_y_labels=False)
    line_chart2 = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                             y_labels_major_every=2, show_minor_y_labels=False)
    line_chart0.title = "Poraba vode [liter/dan]"
    line_chart1.title = "3 dnevno povprecje\nPoraba vode [liter/dan]"
    line_chart2.title = "6 dnevno povprecje\nPoraba vode [enot/dan]"
    text = "<hr>Povprecna poraba [liter/dan]<br />"
    for x, tp in enumerate(topla_hladna):
        cons = []
        timestamp = []
        for d in tp:
            cons.append(d[0] * 1000)
            timestamp.append(d[1])
        data, _, dt = num_tools.running_consumption(cons, timestamp)
        line_chart0.add(topla_hladna_str[x], data)
        text += topla_hladna_str[x].capitalize() + ": %3.3f [st.dev: %3.3f]<br />" % (num_tools.mean(data), num_tools.st_dev(data))
        print topla_hladna_str[x].capitalize(), num_tools.st_dev(data)

        data1 = num_tools.Simplemovingaverage(3, data)
        data1 = data1.calculate()
        line_chart1.add(topla_hladna_str[x], data1)
        data2 = num_tools.Simplemovingaverage(6, data)
        data2 = data2.calculate()
        line_chart2.add(topla_hladna_str[x], data2)
    line_chart1.x_labels = map(str, dt)
    line_chart2.x_labels = map(str, dt)
    text += "<br />"*2
    out = "<div id=\"plot\">"
    out += line_chart0.render(is_unicode=True) + text + "<hr>"
    out += line_chart1.render(is_unicode=True) + "<hr>"
    out += line_chart2.render(is_unicode=True)
    out += "</div>"
    return out


def plot_heat_consumption():
    locations = ["kuhinja", "hodnik", "kopalnica", "soba"]
    line_chart0 = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                             y_labels_major_every=2, show_minor_y_labels=False)
    line_chart1 = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                             y_labels_major_every=2, show_minor_y_labels=False)
    line_chart2 = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                             y_labels_major_every=2, show_minor_y_labels=False)
    line_chart0.title = "Ogrevanje [enot/dan]"
    line_chart1.title = "3 dnevno povprecje\nOgrevanje [enot/dan]"
    line_chart2.title = "6 dnevno povprecje\nOgrevanje [enot/dan]"
    text = "<hr>Povprecna poraba [enot/dan]<br />"
    for loc in locations:
        data_in = data_tools.get_heat_data(loc)
        data = []
        time_delta = []
        for d in data_in:
            data.append(d[0])
            time_delta.append(d[1])
        data, _, dt = num_tools.running_consumption(data, time_delta)
        line_chart0.add(loc, data)
        text += loc.capitalize() + ": %3.3f [st.dev: %3.3f]<br />" % (num_tools.mean(data), num_tools.st_dev(data))
        print loc.capitalize(), num_tools.st_dev(data)

        data1 = num_tools.Simplemovingaverage(3, data)
        data1 = data1.calculate()
        line_chart1.add(loc, data1)
        data2 = num_tools.Simplemovingaverage(6, data)
        data2 = data2.calculate()
        line_chart2.add(loc, data2)
    line_chart1.x_labels = map(str, dt)
    line_chart2.x_labels = map(str, dt)
    out = "<div id=\"plot\">"
    out += line_chart0.render(is_unicode=True) + text + "<hr>"
    out += line_chart1.render(is_unicode=True) + "<hr>"
    out += line_chart2.render(is_unicode=True)
    out += "</div>"
    return out


def plot_heat():
    locations = ["kuhinja", "hodnik", "kopalnica", "soba"]
    line_chart = pygal.Line(width=600, height=300, explicit_size=True, style=CleanStyle,
                            y_labels_major_every=2, show_minor_y_labels=False,
                            x_label_rotation=35)
    line_chart.title = "Ogrevanje - cez cas [enot]"
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