Hi! This project is a part of an ongoing sociological study regarding the Vasi-Hegyhát area in Hungary.
The main focus of the project is to create a graph of all the public transportation opportunities available in the region. 
The codes are all written in python, with the help of chatGPT and without previous experties in coding. :) 

The first objective was to scrape the travel data from www.Mentrendek.hu which is the official listing website in Hungary for bus and train routes. I managed to get the data with the travel_scrape.py file. (In the first run, I used it with 0 and 1 Transfers, in the second, I only checked 0 transfer routes)
*The code is working, but it requires some extra steps to make it work correctly. After it starts the Chrome browser, you have to manually close the tutorial and the accept cookies pop up. And you have to do this quickly...
After that, it works fine. It is kind of slow, but that's because I wanted to make sure the page won't block me as fast. In my experience, you can get to around 700-800 travel request/day. After that, it says you passed your daily limit.
I used HotspotShield VPN to bypass the regulation, it worked just fine.

After I got the information (data3.xlsx), I made the code for the network analysis. You can find it as network.py 
For the attribute, I had to get the up to date data for the populations of each settlement, so I made a scraper for the following website: https://www.ksh.hu/apps/hntr.main?p_lang=HU . You can find this file as settlement_population_finder_hungary.py
This is useful if you ever want to get the exact population of a city in Hungary.
I used the excel output for the attribute (city_population), and implemented the metrics that I was curious about. For the first run, you can check the network_0_1.png file, for the second (which only has direct bus connections): network_0 .
I also made a pyvis version of the network for visualisation purposes.

There might be some better ways to do this project, make sure to share your suggestions with me if you have the time.
David

