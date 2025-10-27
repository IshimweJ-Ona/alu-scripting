#!/usr/bin/python3
"""
A recursive function that queries the Reddit API, parses the titles of all
hot articles, and prints a sorted count of given keywords (case-insensitive).

Requirements:
- Prototype: def count_words(subreddit, word_list)
- Recursive, handles pagination via 'after'
- Words must be counted exactly (java != javascript)
- Duplicates in word_list are summed
- Results printed in descending order by count, then alphabetically
- Invalid subreddits print nothing
"""

import requests
import re
from collections import Counter
import sys


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively query Reddit API for hot posts and count occurrences
    of each keyword in word_list.
    """
    if counts is None:
        # Initialize counter with lowercase keywords
        counts = Counter([w.lower() for w in word_list])

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": 100, "after": after}

    try:
        response = requests.get(url, headers=headers,
                                params=params, allow_redirects=False)

        if response.status_code != 200:
            return

        data = response.json().get('data', {})
        posts = data.get('children', [])
        after = data.get('after', None)

        for post in posts:
            title = post['data']['title'].lower()
            for word in counts:
                # Match exact word using word boundaries
                pattern = r'\b{}\b'.format(re.escape(word))
                matches = re.findall(pattern, title)
                counts[word] += len(matches)

        if after:
            # Recursive call to process next page
            count_words(subreddit, word_list, after=after, counts=counts)
        else:
            # Print results: sorted by count desc, then alphabetically
            sorted_counts = sorted(
                [(w, c) for w, c in counts.items() if c > 0],
                key=lambda x: (-x[1], x[0])
            )
            for w, c in sorted_counts:
                print("{}: {}".format(w, c))

    except requests.RequestException:
        return
        
