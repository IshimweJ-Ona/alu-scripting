#!/usr/bin/python3
"""
Script that queries the Reddit api and returns the number of subscribers for 
a given subreddit.
"""

import requests


def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    And if subreddit is invalid it returns 0.
    """
    if not isinstance(subreddit, str) or subreddit == "":
        return 0
    
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'MyRedditBot/1.0 (by u/Jonathan)'}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            return 0
        
        data = response.json().get("data")
        return data.get("subscribers", 0)
    except Exception:
        return 0
