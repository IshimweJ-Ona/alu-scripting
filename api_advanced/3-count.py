#!/usr/bin/python3
"""
Recursive Reddit keyword counter
"""
import requests


def count_words(subreddit, word_list, after=None, counter=None):
    if counter is None:
        counter = {}
        for word in word_list:
            word_lower = word.lower()
            counter[word_lower] = counter.get(word_lower, 0)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "MyRedditBot/1.0 (by /u/Jonathan)"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            return
        data = response.json().get("data", {})
        posts = data.get("children", [])
        for post in posts:
            title = post.get("data", {}).get("title", "").lower().split()
            for word in counter.keys():
                counter[word] += title.count(word)

        after = data.get("after")
        if after:
            return count_words(subreddit, word_list, after, counter)
        else:
            filtered = {key: v for key, v in counter.items() if v > 0}
            sorted_words = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_words:
                print(f"{word}: {count}")
    except Exception:
        return
