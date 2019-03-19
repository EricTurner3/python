# # # # # # # # # # # # #
# Filename: unstructured-data-practice.py
# Author: Eric Turner
# Source Derived from: https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/
# Goal: Learn how to pre-process and clean data that is unstructured (like tweets) for analysis
# # # # # # # # # # # # #

import HTMLParser
import io

# Use Case: Analyze and extract information from a tweet

# Sample tweet is in the tweet.txt file, in UTF-8, and call .read() to extract the text
# need to use the io library because the native .open cannot read utf-8 encoding
original_tweet = io.open('tweet.txt', 'r+', encoding='utf-8').read()

# Step 1: Escape HTML Characters
html_parser = HTMLParser.HTMLParser()
escaped_tweet = html_parser.unescape(original_tweet)

print(escaped_tweet)

# Step 2 (usually): Decode and encode into a common format
# we are in unicode, which is a standard format (plus the emoji is a unicode unique character)

# Step 3: Convert known slang into context free grammer
# For this example, we will use a dictionary of common aprostrophes to convert
apostrophes = {"'s": " is", "'re": " are"}
