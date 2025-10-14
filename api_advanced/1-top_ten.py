#!/usr/bin/python3
"""
Module that queries the Reddit API and prints the titles
of the first 10 hot posts for a given subreddit.
"""

import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    If the subreddit is invalid, returns None.
    """
    if not isinstance(subreddit, str) or subreddit == "":
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'MyRedditBot/1.0 (by u/Jonathan)'}
    params = {'limit': 10}

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False
        )

        if response.status_code != 200:
            return None

        posts = response.json().get("data", {}).get("children", [])
        if not posts:
            return None

        for post in posts:
            print(post.get("data", {}).get("title"))

    except Exception:
        return None
