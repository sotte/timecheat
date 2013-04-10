timecheat
=========

Generates work time sheets you have to hand in to your employer. 

Put each holiday in a holiday file (each line a date in german format, e.g.
23.12.2013).

With --output you can specify different output formats. There is 'latex', 'text'
and 'template'. If you use a template the tag #MONTH# is replaced by the current
month, #TIMETABLE# is replaced by a 5 column latex table (without \begin and
\end etc.) holding the actual time data.

The script adheres the LOCALE variable. E.g. if you set it to 'de_DE' german day
names are used. 

Right now the sheet is always generated for the current month. Might change
soon.
