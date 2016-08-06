#!/usr/bin/python

# To plot average Safari activity for each day of the week.

import matplotlib
import sqlite3 as lite
import numpy as np
import pylab as pl
import sys
import datetime
from matplotlib.ticker import FuncFormatter

# Find the Safari history database which is in ~/Library/Safari/ by default
from os.path import expanduser
home = expanduser("~")
database = home + "/Library/Safari/History.db"

# Try to open the database
# SQLite help from http://zetcode.com/db/sqlitepythontutorial/
con = None

try:

    con = lite.connect(database)
    cur =  con.cursor()
    
    cur.execute('SELECT visit_time FROM history_visits;')

    data = [int(data[0]) for data in cur.fetchall()]
    # Convert visit_time from NSDate format to UNIX time
    data = map(lambda x: x + 978307200, data)
    data = np.asarray(data, 'datetime64[s]')
    data = data.tolist()

    # Find the day of week where 0 is Monday and 6 is Sunday
    day_of_week = map(lambda x: x.weekday(), data)

    # Plot a histogram of the results
    names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pl.hist(day_of_week, bins = [0,1,2,3,4,5,6,7], align = "left", normed = 'true')
    pl.xlabel('Day of Week')
    pl.xticks([0,1,2,3,4,5,6,7], names, size = "small")
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

except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()