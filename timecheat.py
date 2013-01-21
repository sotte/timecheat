#!/usr/bin/python2
import argparse
from random import gauss
from math import sqrt
from datetime import date, datetime, time, timedelta
import calendar
from string import strip
from printer import TextPrinter, LatexPrinter
import locale
from os import environ


def create_times(day, start, pausestart, worktime, pausetime, variance):
    start = round_to_quarter(datetime.combine(day, time(start)) +
                             timedelta(hours=gauss(0, sqrt(variance))))
    pausetime = timedelta(hours=pausetime)
    worktime = timedelta(hours=worktime)
    pausestart = round_to_quarter(datetime.combine(day, time(pausestart)) +
                                  timedelta(hours=gauss(0, sqrt(variance))))
    pauseend = pausestart + pausetime
    end = start + pausetime + worktime
    return (start, end, pausestart, pauseend)


def round_to_quarter(time):
    minutes_quarter = int(round((time.minute/60.)*4)/4*60)
    minutes_ten = int(round(time.minute/10.)*10)
    if abs(minutes_quarter-time.minute) < abs(minutes_ten-time.minute):
        minutes = minutes_quarter
    else:
        minutes = minutes_ten

    if minutes == 60:
        minutes = 0
    time = time.replace(minute=minutes)
    return time


def get_month():
    today = date.today()
    return (today.year, today.month)


def get_holidays(filename):
    holiday_file = file(filename)
    holidays = []
    for h in holiday_file.readlines():
        h = strip(h, '\n')
        holidays.append(datetime.strptime(h, '%d.%m.%Y').date())
    return holidays


def get_work_days(year, month, holiday_file):
    cal = calendar.Calendar()
    workdays = []
    holidays = get_holidays(holiday_file)
    for day in cal.itermonthdates(year, month):
        if (day.weekday() not in [calendar.SATURDAY, calendar.SUNDAY] and
                day not in holidays):
            workdays.append(day)
    return workdays


def print_sheet(printer, workdays, args):
    printer.print_header()
    week = 0
    for day in workdays:
        (s, e, ps, pe) = create_times(day, args.start[0], args.pausestart[0],
                                      args.worktime[0], args.pausetime[0],
                                      args.variance[0])
        (_, weeknumber, _) = day.isocalendar()
        if weeknumber != week:
            printer.print_divider()
            week = weeknumber
        printer.print_day(s, e, ps, pe)
    printer.print_footer()


def main():
    try:
        locale.setlocale(locale.LC_TIME, environ['LOCALE']) 
    except KeyError: # no locale set
        pass
    parser = argparse.ArgumentParser(description='Create a timesheet with ' +
                                     'gaussian distributed times for work.')
    parser.add_argument('--start', nargs=1, metavar='t_s', default=[8],
                        type=int, help='The time when work normally' +
                        ' starts. Default: 08:00 (=8).')
    parser.add_argument('--pausestart', nargs=1,  metavar='t_p',
                        default=[13], type=int, help='Time when the ' +
                        'lunch break normally starts. Default 13:00 (=13).')
    parser.add_argument('--worktime', nargs=1, metavar='t_d',  default=[8],
                        type=float, help='The duration of every work ' +
                        'day. Default: 8 hours (=8)')
    parser.add_argument('--pausetime', nargs=1, metavar='t_pt', default=[.5],
                        type=float, help='The duration of the lunch ' +
                        'break. Default: 30 min (=0.5)')
    parser.add_argument('--variance', nargs=1, metavar='var', default=[.25],
                        type=float, help='The variance of each start ' +
                        'time. Default: 15 min (=.25).')
    parser.add_argument('--output', nargs=1, metavar='format',
                        default=['text'], type=str, help='The output format.' +
                        ' May be \'text\', \'template\'  or \'latex\'. ' +
                        'Default: text')
    parser.add_argument('--template', nargs=1, metavar='file',
                        default=['worksheet.tex'], type=str, help='If output' +
                        ' is \'template\' you can specify a template file.')
    parser.add_argument('--holidays', nargs=1, metavar='file',
                        default=['holidays'], type=str, help='A file ' +
                        'holiday dates. Format is each day in a line in ' +
                        ' german order, e.g.: 24.03.2013')
    args = parser.parse_args()
    (year, month) = get_month()
    workdays = get_work_days(year, month, args.holidays[0])

    if args.output[0] == 'text':
        printer = TextPrinter()
    elif args.output[0] == 'template':
        printer = LatexPrinter(args.template[0])
    elif args.output[0] == 'latex':
        printer = LatexPrinter()
    else:
        parser.print_help()
        return
    print_sheet(printer, workdays, args)


