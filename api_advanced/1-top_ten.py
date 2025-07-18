#!/usr/bin/python3
"""
function that querries the reddit api and prints the titles of the first 110 hot posts listed for the subdreddit.
requirements: def_top_ten(subreddit),
             if not a valid subreddit, print none
                invalid subreddit may return a redirect to search results.and follow the redirects.
"""
import requests
import sys

def top_ten(subreddit):
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {
        "User-Agent": "python:1-top_ten:v1.0 (by/u/Background_Panic9162)"
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
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
    top_ten = __import__('1-top_ten').top_ten
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])

