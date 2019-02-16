### This is to generate the text of daily water-decision post
import requests, os, pytz, datetime

from datetime import datetime as dt
from pytz import timezone

import reddit_config as c
#import history_format as hf

# Date time set up
date_format = '%H:%M:%S MST'
title_format = '%Y-%m-%d'
PST = timezone('US/Mountain')

utc_now = dt.now(tz=pytz.utc)
now_pst = utc_now.astimezone(PST)

def ord(n):
    if 4<=n%100<=20:
        return str(n)+"th"
    else:
        return str(n)+{1:"st",2:"nd",3:"rd"}.get(n%10,"th")

ord_date = ord(int(now_pst.strftime('%-d')))

now_formatted = now_pst.strftime(date_format)
end_time = now_pst + datetime.timedelta(0, 20*3600)
end_time_formatted = end_time.strftime(date_format)

# Weather update
url='http://api.openweathermap.org/data/2.5/weather?zip=80302,us&APPID=%s'
url = url%(os.environ['weather_api_key'])
r = requests.get(url)
description = r.json()['weather'][0]['main']

# Daily Water Thread
title = """
Today is {0}, {1} {2}. Do you want to water the plant today? 
"""

title = title.format(now_pst.strftime('%A'),
                     now_pst.strftime('%B'), 
                     ord_date) 
                    
#history = hf.history_table

body = """
Hello, and welcome back!

It is **{0}** in Colorado and the weather report today calls for: *{1}*.

Please vote for whether or not you think our new plant should be watered today.

To vote for **water** please comment `yes`, `aye`, or `prost` on this post.

To vote for **no water today** please comment `no`, `nein`,  `not on your nelly` on this post.

This post will stay up for 23 hours and then it, and all votes,  post will be locked.
u/takecareofmyplant will tally all the **water** or **no water** votes in top level comments
on this thread. 

If **water** is the majority, u/takecareofmyplant will turn on the
pump and water the plant. If not, we will check in again tomorrow!


**To help take care of the plant, please vote below!**

****

****

Check out the [PLANT CAM](http://www.takecareofmyplant.com) to help guide your decision! 

Show your support for sensible watering policy by purchasing a [JEFF PIN!](https://www.etsy.com/listing/487532734/not-on-your-nelly-enamel-pin?ref=shop_home_active_1)
"""

body = body.format(now_formatted, description, end_time_formatted, 'this section under construction')

# Wrapup
body_edit = """
Hello again, it is **{0}** and I've just finished counting your votes.


Here are the results:


Yes | No
---|--
{1} | {2}


If the majority votes in favor of watering, the water pump will automatically switch on for 15 seconds tomorrow morning at 8 AM Mountain Time. 

Don't forget to check out [THE WEBSITE](http://www.takecareofmyplant.com)! You can see how the water affects the soil moisture, and see how the plant responds on the livestream!


Thanks for taking care of my plant!!
"""

continuous_vote_display = """

%s

%s

""".format(now_formatted)


