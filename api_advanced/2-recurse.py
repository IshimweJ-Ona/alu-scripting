#!/usr/bin/python3
"""
Recursive function that queries the Reddit API and returns
a list of all hot article titles for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Returns a list containing the titles of all hot articles
    for a given subreddit. If no results, returns None.
    """
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'MyRedditBot/1.0 (by u/Jonathan)'}
    params = {'limit': 100, 'after': after}

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False
        )

        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        posts = data.get("children", [])
        after = data.get("after", None)

        for post in posts:
            hot_list.append(post.get("data", {}).get("title"))

        if after:
            # Recursive call for the next page
            return recurse(subreddit, hot_list, after)
        else:
            return hot_list if hot_list else None

    except Exception:
        return None
