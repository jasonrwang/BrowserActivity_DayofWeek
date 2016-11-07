# BrowserActivity_DayofWeek

Extracts history activity for Safari and Chrome on OS X/macOS and plots proportional amount of activity for different days of the week and for different hours of a day (localized by time zone).

![Figure 1](https://i.imgur.com/wUEHNIg.png)

![Figure 2](https://i.imgur.com/GsyhATl.png)

I don't really know what this says about my behaviour and would like to process the data more in future versions to gain more insight.

## To use:
1. Download this script or `git clone https://github.com/jasonrwang/BrowserActivity_DayofWeek.git` so you have a local copy
2. Use Terminal to navigate to find main.py
3. Type in `python main.py`

Alternatively, if you download this to your Downloads folder, use `python ~/Downloads/main.py` from Terminal

## Timezones:
Input into timezones.txt a comma separated list of timezones you were in. If you were only in one timezone, you will still need to use this.

Format: `start_time,end_time,time_zone`
Times should be in ISO 8601 () format or 'now' (without quotations). Timezones should be in [Olson time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Use `0,now,[Your timezone code]` as a default.

## Changelog
v0.4.2 Limited timezone support
* Added time zone support as defined in timezones.txt
* Can filter all data to a single time period as well if it is in the same time zone
* Timezones can be improved if it was easier to input!

v0.4.1 	Hour of Day Analysis added
* Also analyzes and displays information about usage at different hours during a day
* Uses naive datetimes i.e. does not account for history in different timezones

v0.3	Chrome added, Rename
* Also gathers information from Google Chrome
* Processes sum of Chrome and Safari data
* Rename to BrowserActivity_DayofWeek from SafariActivity_DayofWeek

v0.2	Percent Use
* Displays output in percentage of total instead of raw value since it is more valuable and protects privacy

v0.1	Basic functionality added:
* Finds `History.db` file from `~/Library/Safari/` automatically
* Will catch if the database cannot be opened
* Converts NSDate timestamps for history data into day of the week
	* Note that time zone differences are probably not correct since Safari likely looks to the system to determine the time and travelling users (like me) don't always update this immediately
* Matlibplot histogram works but is ugly

---
P.S. This is my first python script! I have a feeling it could be much faster since I suspect I did not use numpy to its full capabilities. Suggestions are welcome.

