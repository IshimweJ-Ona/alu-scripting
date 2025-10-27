#!/usr/bin/python3
"""
Function that queries the Reddit API and prints the titles of the first 10
hot posts listed for a given subreddit.
"""

import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    If not a valid subreddit, prints None.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        'User-Agent': 'python:1-top_ten:v1.0 (by /u/Background_Panic9162)'
    }
    params = {'limit': 10}

    response = requests.get(url, headers=headers,
                            params=params, allow_redirects=False)

    # Check for invalid subreddit or API error
    if response.status_code != 200:
        print("None")
        return

    try:
        results = response.json().get("data", {}).get("children", [])
        if not results:
            print("None")
            return

        for post in results:
            print(post.get("data", {}).get("title"))
    except Exception:
        print("None")
