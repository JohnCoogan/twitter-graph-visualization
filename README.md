Twitter Graph Visualization
===========================

The goal of this project is to apply some of the machine learning concepts I've learned so far to my own personal data. Code in this repo contains everything needed to perform the same analysis on yourself. Everything from collecting and cleaning the data, to running the analyses, to finally visualizing output is here.

Files
-----
*	**twitter.py:** Scrape and clean twitter data.
*	**analysis.py:** Read in Edge List and generate analysis and graph data.
*	**vis folder:** Visualization Files.
*	**oauth.json:** Contains personal config vars in a dictionary (not checked in)

OAuth.json
----------

	{
		"consumer_key" : "key",
		"consumer_secret" : "secret",
		"access_token" : "key",
		"access_token_secret" : "secret",
		"screen_name" : "name",
		"user_id" : 12345678
	}

TODO:
-----
*	Add Stats to visualization w/ mouse-over
*	Add switch to view by eigenvector vs. degree.
*	Clean up python flow and make modular.
*	Add description of what's going on to front-end
*	Create modular version with Twitter OAuth. (Look at rate-limits first)