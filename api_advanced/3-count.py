#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the titles of all hot posts,
and prints a sorted count of given keywords.
"""

import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Recursive counts occurrences of words in hot article titles."""
    if counts is None:
        counts = {}

    # Normalize the word list (lowercase, handle duplicates)
    word_list = [word.lower() for word in word_list]

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'MyRedditBot/1.0 (by u/Jonathan)'}
    params = {'after': after, 'limit': 100}

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    # Stop if subreddit is invalid
    if response.status_code != 200:
        return None

    # Parse JSON data
    data = response.json().get("data", {})
    children = data.get("children", [])

    # Count words in all post titles
    for post in children:
        title = post.get("data", {}).get("title", "").lower().split()
        for word in word_list:
            counts[word] = counts.get(word, 0) + title.count(word)

    # Get next page
    after = data.get("after", None)

    if after is not None:
        # Recursive call to get next page
        count_words(subreddit, word_list, after, counts)
    else:
        # No more pages, print results
        sorted_counts = sorted(
            [(word, count) for word, count in counts.items() if count > 0],
            key=lambda item: (-item[1], item[0])
        )

        for word, count in sorted_counts:
            print(f"{word}: {count}")
