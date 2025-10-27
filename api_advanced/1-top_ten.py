#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10 hot posts
listed for a given subreddit.

Prototype: def top_ten(subreddit)
If not a valid subreddit, print None.
NOTE: Invalid subreddits may return a redirect to search results.
Ensure that you are not following redirects.
"""

import requests
import sys

def top_ten(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {
        "User-Agent": "python:top_ten:v1.0 (by /u/Background_Panic9162)"
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            if not posts:
                print("None")
            else:
                for post in posts:
                    print(post['data']['title'])
        else:
            print("None")
    except requests.RequestException:
        print("None")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
