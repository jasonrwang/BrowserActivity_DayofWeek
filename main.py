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

# Find the history databases
from os.path import expanduser
home = expanduser("~")
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
        
        # Format UNIX timestamp to datetime
        data = np.asarray(data, 'datetime64[s]')
        data = data.tolist()

        # Find the day of week where 0 is Monday and 6 is Sunday
        day_of_week = map(lambda x: x.weekday(), data)
        # Find the hour of the day
        time_of_day = map(lambda x: int(x.strftime('%H')), data)
        
        ## Plot a histogram of the results
        
        # Day of Week
        pl.figure(1)
        names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pl.hist(day_of_week, bins = [0,1,2,3,4,5,6,7], align = "left", normed = 'true')
        pl.xlabel('Day of Week')
        pl.xticks([0,1,2,3,4,5,6,7], names, size = "small")
        pl.ylabel('Proportion of All Activity / %')

        # Hour of Day
        pl.figure(2)
        names = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
        pl.hist(time_of_day, bins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], align = "left", normed = 'true')
        pl.xlabel('Hour of Day')
        pl.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], names, size = "small")
        pl.ylabel('Proportion of All Activity / %')

        # Define function to format the y-axis labels to be in percent
        # http://matplotlib.org/examples/pylab_examples/histogram_percent_demo.html
        def to_percent(y, position):
            # Ignore the passed in position. This has the effect of scaling the default
            # tick locations.
            s = str(100 * y)

            # The percent symbol needs escaping in latex
            if matplotlib.rcParams['text.usetex'] is True:
                return s + r'$\%$'
            else:
                return s + '%'

        # Create the formatter using the function to_percent. This multiplies all the
        # default labels by 100, making them all percentages
        formatter = FuncFormatter(to_percent)

        # Set the formatter
        pl.gca().yaxis.set_major_formatter(formatter)
        
        pl.show()

        # To split analysis up into weeks, check for when a value is less than the previous.
        
        con.close()