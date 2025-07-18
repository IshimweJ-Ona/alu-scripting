#!/usr/bin/python3
"""
A functioon that querries the reddit api and returns the number of subscribers (not active users, total subscribers)
for a given subreddit. if invalid subreddit is given, it returns 0.
requirements: def_number_subscribers(subreddit),
             if not valid subreddit returns 0
             invalid subreddit may return a redirect to search results.and folow the redirects.
"""

import requests
import sys

def number_of_subscribers(subreddit):
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {
        "User-Agent": "python:0-subs:v1.0 (by /u/Background_Panic9162)"
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            data = response.json()
            return data['data']['subscribers']
        else:
            return 0
    except requests.RequestException:
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <subreddit>".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        print(number_of_subscribers(subreddit))
