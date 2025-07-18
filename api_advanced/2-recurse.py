#!/usr/bin/python3
"""
function querries the reddit api and returns a list containing the titles of all hot articles for a given subreddit.
if no result are found for the given subreddit, the function should return none
the reddit api pagination for separating pages of responses
requirements: def recurse(subredddit, hot_list=[])
we can add a counter but it must work without supplying a starting value in the main
if not a valid subreddit, print none
"""
import requests
import sys

def recurse(subreddit, hot_list=[], after=None):
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "python:2-recurse:v1.0 (by /u/Background_Panic9162)"
    }

    # Set up parameters for pagination
    params = {
        "limit": 100,  # Maximum number of posts per request
        "after": after  # Pagination token
    }

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirections=True)
        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            if not posts:
                print("None")
            else:
                for post in posts:
                    hot_list.append(post['data']['title'])
                    # Check if there is a next page
                after = data['data'].get('after')
                if after:
                    return recurse(subreddit, hot_list, after)
                else:
                    return hot_list
        else:
            print("None")
            return None
    except requests.RequestException:
        print("None")
        return None
if __name__ == '__main__':
    recurse = __import__('2-recurse').recurse
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")
