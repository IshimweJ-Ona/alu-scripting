#!/usr/bin/python3
"""
A recursive function that queries the Reddit API, parses the title of all hot articles, andprints a sorted count of given keyword(case-insensitive, delimited by spaces.Javascript should count as javascript, but java should not) 
Requirments: def count_words(subreddit, word_list)
may change the prototype but must be able to be called with subreddit supplied and list of keywords, the function must work without supplying a starting value in main
if word_list contains same word(case-insensitive), final count should be sum of each duplicate
results printed in descending order, by count, if count is the same for separate keywords, they should then be sorted alphabetically(ascending form A to Z). words with no match should be skipped and not printed. words must be printeed in lowercase
Results are based on the number of times a keyword appears, not titles it appears in. java java java counts as 3 separate occurrences of java.
To make life easier, java. or java! or java_ should not count as java
If no posts match or the subreddit is invalid, print nothing.
Invalid subreddits may return a redirect to search results. Ensure that you are NOT following redirects.
"""
import requests
import sys

def count_words(subreddit, word_list):
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "USER-AGENT": "python:3-count:v1.0 (by /u/Background_Panic9162)"
    }
    params = {
        "limit": 100  # Maximum number of posts per request
    }
    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            if not posts:
                return
            word_count = {word.lower():0 for word in word_list}
            for post in posts:
                title = post['data']['title'].lower()
                for word in word_list:
                    word_lower = word.lower()
                    # Count occurrences of the word in the title
                    word_count[word_lower] += title.split().count(word_lower)
            # Filter out words with zero count
            word_count = {word: count for word, count in word_count.items() if count > 0}
            # Sort by count (descending) and then alphabetically (ascending)
            sorted_word_count = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_word_count:
                print("{}: {}".format(word, count))
        else:
            return
    except requests.RequestException:
        return
if __name__ == '__main__':
    count_words = __import__('3-count').count_words
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <word1> <word2> ...".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2:]
        count_words(subreddit, word_list)
       

