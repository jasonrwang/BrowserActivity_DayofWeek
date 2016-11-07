#!/usr/bin/python

# To plot average Safari activity for each day of the week.

import matplotlib
import sqlite3 as lite
import numpy as np
import pylab as pl
import sys
import time
import pytz
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from matplotlib.ticker import FuncFormatter
import os

# Find the history databases
home = os.path.expanduser("~")
# Find the Safari history database which is in ~/Library/Safari/ by default
safari_database = home + "/Library/Safari/History.db"
# Find the Chrome history database which is in ~/Library/Safari/ by default
chrome_database = home + "/Library/Application Support/Google/Chrome/Default/History"

# Try to open the database
# SQLite help from http://zetcode.com/db/sqlitepythontutorial/
con = None
data = []

try:

    con = lite.connect(safari_database)
    cur =  con.cursor()
    
    cur.execute('SELECT visit_time FROM history_visits;')

    safari_data = [int(safari_data[0]) for safari_data in cur.fetchall()]
    # Convert visit_time from NSDate format to UNIX time
    safari_data = map(lambda x: x + 978307200, safari_data)

    data = data + safari_data

# Apparently python try-excepts are annoying and this needs to be declared twice
except lite.Error, e:
    
    print "Safari DB Error %s:" % e.args[0]

try:

    con = lite.connect(chrome_database)
    cur =  con.cursor()
    
    cur.execute('SELECT visit_time FROM visits;')

    chrome_data = [int(chrome_data[0]) for chrome_data in cur.fetchall()]
    # Convert visit_time from FILETIME format to UNIX time
    chrome_data = map(lambda x: (x -11644473600000000) / 1000000, chrome_data)

    data = data + chrome_data
    
except lite.Error, e:
    
    print "Chrome DB Error %s:" % e.args[0]
    
finally:
    
    if con:

        # Time filter
        utc = pytz.utc

        script_dir = os.path.dirname(__file__)
        timezone_input = os.path.join(script_dir, 'timezones.txt')
        timezone_input = open(timezone_input,'r')
        timezone_input = timezone_input.read().splitlines()
        data_filtered = list()

        # Format UNIX timestamp to datetime
        data = np.asarray(data, 'datetime64[s]')
        data = data.tolist()
        data = map(lambda x: utc.localize(x), data)
        
        # Add local time zone information to each time
        for period in range(0, len(timezone_input)):

            period_info = timezone_input[period].split(',')
            zone = timezone(period_info[2])
            time_format = '%Y-%m-%d %H:%M'
            time_lower = datetime.strptime(period_info[0], time_format)
            
            if period_info[1] in 'now':
                time_upper = datetime.fromtimestamp(time.time())
            else:
                time_upper = datetime.strptime(period_info[1], time_format)

            time_lower = zone.localize(time_lower)
            time_upper = zone.localize(time_upper)

            # Need to add error checking if upper is larger than lower!

            data_temp = [i for i in data if i >= time_lower and i <= time_upper]
            data_temp = map(lambda x: x.astimezone(zone), data_temp)
            data_filtered = data_filtered + data_temp
        
        print('Check length of data... if processed data is less than history, some has been missed; if more, some are double counted. Check timezones.txt!')
        print('Length of history data:\t\t' + str(len(data)))
        print('Length of processed data:\t' + str(len(data_filtered)))

        # Find the day of week where 0 is Monday and 6 is Sunday
        day_of_week = map(lambda x: x.weekday(), data_filtered)
        # Find the hour of the day
        time_of_day = map(lambda x: int(x.strftime('%H')), data_filtered)

        ## Plot a histogram of the results

        # Create the formatter using the function to_percent. This multiplies all the
        # default labels by 100, making them all percentages
        # Define function to format the y-axis labels to be in percent
        # http://matplotlib.org/examples/pylab_examples/histogram_percent_demo.html
        def to_percent(y, position):
        # Ignore the passed in position. This has the effect of scaling the default
        # tick locations.
            s = str(int(100 * y))
            
            # The percent symbol needs escaping in latex
            if matplotlib.rcParams['text.usetex'] is True:
                return s + r'$\%$'
            else:
                return s + '%'
        
        formatter = FuncFormatter(to_percent)

        # Day of Week
        pl.figure(1)
        names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pl.hist(day_of_week, bins = [0,1,2,3,4,5,6,7], align = "left", normed = 'true')
        pl.xlabel('Day of Week')
        pl.xticks([0,1,2,3,4,5,6,7], names, size = "small")
        pl.ylabel('Proportion of All Activity / %')
        pl.gca().yaxis.set_major_formatter(formatter)

        # Hour of Day
        pl.figure(2)
        names = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
        pl.hist(time_of_day, bins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], normed = 'true')
        pl.xlabel('Hour of Day')
        pl.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], names, size = "small")
        pl.ylabel('Proportion of All Activity / %')
        pl.gca().yaxis.set_major_formatter(formatter)
        
        # Show figures
        pl.show()

        # To split analysis up into weeks, check for when a value is less than the previous.
        print('Done.')

    con.close()