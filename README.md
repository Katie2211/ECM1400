# ECM1400
CA3 smart alarm clock app


Read-me File

NOTE!!! - during development we came across a known Mac error with pyttsx3 and after discussion with a PA came to the conclusion that the code needs to be run on a windows computer to work, as a result I have also commented this out from testing.

Introduction 

This code is an alarm system that can keep the user up to date on important news matters, relating to coronavirus and other big headlines, as well as the option to have a weather broadcast, this information updates frequently and is sourced from a variety of hosts which will need to accessed using the users API key.

How to operate

This code runs on python 3.8.5 and requires the following to be installed:	
Pyttsx3 - this can be installed by the command pip install pyttsx3
Flask -  this can be installed by the command pip install Flask

There are a number of user inputs within the code that require certain formatting to be accepted:
The first box - this box is where the alarm name will be entered this can be any series of characters
The second box - here there needs to be a time, this can be in the form of number of hours. Number of minutes. Number of seconds
The check boxes - these remain unchanged to the original design of the template
Crosses on the notifications - these also remain unchanged as to their operation.

I realise that the boxes are the wrong way round however this was noticed too late and I cannot see the calendar so the code should be used as such.

The config file should also be amended as detailed below.

Config.json

This is where you should add in your API key, there will be dedicated spaces for this.

Design decisions 

I have also decided that notifications will be displayed with every alarm, however announcements will only occur on user set alarms. Another design decision I made was to keep headline briefings to just the BBC News when getting the news for the alarms and then for the daily briefings filtering by having just events relating to coronavirus as otherwise there is just too much information in each notification. The start of my logging is uncommented but this does change once we did more on this topic.

Meta data

Author - Katie Hopkins

Licence 

MIT License

Copyright (c) 2020 Katie Hopkins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
