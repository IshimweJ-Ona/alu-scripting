#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the titles of all hot posts,
and prints a sorted count of given keywords (case-insensitive, delimited by spaces).
"""

import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively counts occurrences of words in hot article titles.

    Args:
        subreddit (str): subreddit to query
        word_list (list): list of keywords to count
        after (str): token for next page (used for recursion)
        counts (dict): accumulator for counts (used for recursion)
    """
    if counts is None:
        counts = {}

    if not word_list or not isinstance(subreddit, str):
        return

    # Normalize keywords (lowercase)
    keywords = [w.lower() for w in word_list]

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "MyRedditBot/1.0 (by u/Jonathan)"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            return
        data = response.json().get("data", {})
        children = data.get("children", [])
    except Exception:
        return

    # Count occurrences of exact words (case-insensitive, punctuation excluded)
    for post in children:
        title = post.get("data", {}).get("title", "").lower().split()
        for word in keywords:
            counts[word] = counts.get(word, 0) + title.count(word)

    # Recursion: process next page if exists
    after = data.get("after")
    if after:
        count_words(subreddit, word_list, after, counts)
    else:
        # Base case: no more pages, print results
        # Aggregate duplicates in word_list
        final_counts = {}
        for word in keywords:
            final_counts[word] = final_counts.get(word, 0) + counts.get(word, 0)

        # Sort: descending by count, then ascending alphabetically
        sorted_counts = sorted(
            ((w, c) for w, c in final_counts.items() if c > 0),
            key=lambda x: (-x[1], x[0])
        )

        for word, count in sorted_counts:
            print(f"{word}: {count}")
