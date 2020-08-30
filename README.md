# Xtrades Clipboard Convertor
A tool that saves some time copying options plays from xtrades' discord server to avoid losing time to finding it in the
offerings chart and missing a good dip.

###
###

Created by Noah Alzayer

www.NoahAlzayer.net

[xtrades_clipboard@noahalzayer.net](mailto:xtrades_clipboard@noahalzayer.net)

##
### Installation:
Simply install Python 3 if you dont't have it aleady
###
https://www.python.org/download/releases/3.0/

###
Then run xtrades_clipboard_convertor.py and the window should come up
##

### Use:
Simply copy a play from the plays channel and either press "Parse From Clipboard" or paste the contents in the field to
the right and press "Parse from Field"

The output underneath should show the results and success or any tracked failures. If successful, you should be able to
paste it in thinkorswim using the clipboard order function
###

https://www.youtube.com/watch?v=LvC2nV5DeGU

###

Then double-check the order for accuracy and submit

##

The stock plays need to be in the following format:

###
Action (BTO, STO) Ticker (TSLA, AAPL) Expiration (10/28) Stike (125c) Price (@2.50)

###
Ex - BTO HD 9/4 295C @1.07

###
The tool does some amount of automatic fixing of plays (removing spaces between the @ or the slashes for dates, 
removing removing dollar signs) then does some checking for things it won't fix automatically (different order for the
inputs) but if it catches those errors, that's where the "Parse from Field" can come in handy for doing some quick edits
to get things in order. I hope to do an upgrade at some point to have it smartly figure things out if the order isn't
exactly the same as needed, but for now, order is locked. 

###
If it does stop partway through converting without any message saying what's wrong, that means there's an "uncaught" 
error, in which case, you can email me or submit a bug in the github with the input you gave and I can try and figure 
out what went wrong
