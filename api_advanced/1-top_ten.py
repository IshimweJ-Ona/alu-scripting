#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10 hot posts
listed for a given subreddit.
"""

import requests
import sys


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts of a subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": 10}

    try:
        response = requests.get(url, headers=headers,
                                params=params, allow_redirects=False)
        if response.status_code != 200:
            print("None")
            return

        posts = response.json().get("data", {}).get("children", [])
        if not posts:
            print("None")
            return

        for post in posts:
            print(post.get("data", {}).get("title"))

    except requests.RequestException:
        print("None")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
