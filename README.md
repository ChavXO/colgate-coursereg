# colgate-coursereg
A Python application for registering for classes at Colgate University.

## Running the programme
To start the programme type `$ ./Main.py` into your shell.



## What do I need to run the programme?
The program uses the requests library which should be available by default with all versions of Python 2.7.x. If not install the library as follows:
`pip install requests`
Or alternatively:
`easy_install requests`

Make sure you have the bs4 library downloaded on your computer.
`pip install bs4`



## How exactly does this work?
Registration usually fills up within the first minute that it opens. Usually people have their alternate pins typed into a browser waiting for their time to open. When it does they quickly enter the course registration numbers on the form  at the bottom then send in their request. This app seeks to minimise thaat time. Now you can have your CRNs queued  up and as soon as your spot opens all you have to do is press send data and everything is done in a few seconds less.



## Why can't I automatically set a time for it to run?
That would entail saving your session and then automating the process on a scheduler. While not too difficult to implement, the process could be very insecure considering that we are dealing with very sensitive data.

Check back for updates though.
