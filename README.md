timecheat
=========

Generates work time sheets you have to hand in to your employer. 

Put each holiday in a holiday file (each line a date in german format, e.g.
25.12.2013).

With --output you can specify different output formats. There is 'latex', 'text'
and 'template'. If you use a template the tag #MONTH# is replaced by the current
month, #TIMETABLE# is replaced by a 5 column latex table (without \begin and
\end etc.) holding the actual time data.

The script adheres the LOCALE variable. E.g. if you set it to 'de_DE' german day
names are used. 

Its default is to generate timesheets for the last month.

    Usage: timecheat.py [-h] [--start t_s] [--pausestart t_p] [--worktime t_d]
                    [--pausetime t_pt] [--variance var] [--year year]
                    [--month month] [--output format] [--template file]
                    [--holidays [file [file ...]]]
                    [--unholidays [file [file ...]]]

    -h, --help            show this help message and exit
    --start t_s           The time when work normally starts. Default: 08:00
                          (=8).
    --pausestart t_p      Time when the lunch break normally starts. Default
                          13:00 (=13).
    --worktime t_d        The duration of every work day. Default: 8 hours (=8)
    --pausetime t_pt      The duration of the lunch break. Default: 30 min
                          (=0.5)
    --variance var        The variance of each start time. Default: 15 min
                          (=.25).
    --year year           The year for which the timesheet should be printed.
                          Default: Current year
    --month month         The month for which the timesheet should be printed.
                          Default: Current month
    --output format       The output format. May be 'text', 'template' or
                          'latex'. Default: template
    --template file       If output is 'template' you can specify a template
                          file.
    --holidays [file [file ...]]
                          A file holiday dates. Format is each day in a line in
                          german order, e.g.: 24.03.2013
    --unholidays [file [file ...]]
                          A file working dates. Format is each day in a line in
                          german order, e.g.: 24.03.2013
