__author__ = 'Lesko'
import datetime


def mean(data):
    return sum(data) / float(len(data))


def diff(data):
    previous, data = data[0], data[1:]
    out_data = []
    for x in data:
        out_data.append(x - previous)
        previous = x
    return out_data


def running_consumption(data, time_series):
    """Calculates running consumption E/day

    :param data:
    :param time_series:
    """

    data_d = diff(data)
    time_d = diff(time_series)
    out_data = []
    for d_d, t_d in zip(data_d, time_d):
        # print type(t_d)
        # print d_d, "|", t_d, "|", float(t_d.total_seconds())/60/60, (float(d_d)/float(t_d.total_seconds()))*60*60*24
        out_data.append((float(d_d)/float(t_d.total_seconds()))*60*60*24)
    return out_data


if __name__ == '__main__':
    data = [8, 15, 23, 26]

    # print mean(data)
    #
    # print diff(data)

    time_data = ["2014-12-06 19:33:31.642896",
                 "2014-12-07 09:28:42.378834",
                 "2014-12-08 17:55:55.261066",
                 "2014-12-09 12:55:57.269066"]
    for x, date in enumerate(time_data):
        time_data[x] = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")

    print running_consumption(data=data, time_series=time_data)

    # print days_hours_minutes(time_data[1] - time_data[0])