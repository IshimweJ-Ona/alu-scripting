#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the titles
of all hot articles, and prints a sorted count of given keywords.
"""

import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively counts occurrences of keywords in hot article titles
    from a given subreddit and prints results sorted as specified.
    """
    if counts is None:
        counts = {}

    # Prepare word list: lowercase, handle duplicates
    keywords = [w.lower() for w in word_list]

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "MyRedditBot/1.0 (by u/Jonathan)"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            return  # invalid subreddit
        data = response.json().get("data", {})
        posts = data.get("children", [])
    except Exception:
        return

    # Count occurrences of keywords in titles
    for post in posts:
        title_words = post.get("data", {}).get("title", "").lower().split()
        for kw in keywords:
            counts[kw] = counts.get(kw, 0) + title_words.count(kw)

    # Recursive call if there are more pages
    after = data.get("after")
    if after:
        count_words(subreddit, word_list, after, counts)
    else:
        # Base case: no more pages, print results
        # Sum duplicates in word_list
        final_counts = {}
        for kw in keywords:
            final_counts[kw] = final_counts.get(kw, 0) + counts.get(kw, 0)

        # Sort: descending by count, then alphabetically
        sorted_counts = sorted(
            ((k, c) for k, c in final_counts.items() if c > 0),
            key=lambda x: (-x[1], x[0])
        )

        for k, c in sorted_counts:
            print(f"{k}: {c}")
