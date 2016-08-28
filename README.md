# BrowserActivity_DayofWeek

Extracts history activity for Safari and Chrome on OS X/macOS and plots proportional amount of activity for different days of the week.

![Figure 1](https://i.imgur.com/wUEHNIg.png)

I don't really know what this says about my behaviour and would like to process the data more in future versions to gain more insight.

## To use:
1. Download this script or `git clone https://github.com/jasonrwang/BrowserActivity_DayofWeek.git` so you have a local copy
2. Use Terminal to navigate to find main.py
3. Type in `python main.py`

Alternatively, if you download this to your Downloads folder, use `python ~/Downloads/main.py` from Terminal

## Changelog
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

