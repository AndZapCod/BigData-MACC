##########################################################
#####################  IMPORTANT  ########################
##########################################################

# Execute the following commands before do the test.
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

import pandas as pd

# Test cases

# The most negative user
user_view = pd.read_csv(
    'output/user_sentiment.csv',
    names=['user', 'neg-', 'neg', 'neutral', 'pos', 'pos+']
)

max_reg = max(zip(
    user_view['user'], user_view['neg-']
), key=lambda x: x[1])

print(max_reg[0])

# Top 5 the most positive words

word_view = pd.read_csv(
    'output/word_sentiment.csv',
    names=['word', 'sentiment', 'count']
)

words = sorted(filter(
    lambda x: x[1] == 4,
    zip(word_view['word'], word_view['sentiment'], word_view['count'])
), key=lambda x: x[2], reverse=True)

print(words[:5])

# Percentage of negative tweets in June of 2009

date_view = pd.read_csv(
    'output/sentiment_date.csv',
    names=['sentiment', 'norm_date', 'count']
)

neg_tweets = list(filter(
    lambda x: x[0] == 0 and
              x[1].split('-')[1] == '06' and
              x[1].split('-')[0] == '2009',
    zip(date_view['sentiment'], date_view['norm_date'], date_view['count'])
))

pos_tweets = list(filter(
    lambda x: x[0] == 4 and
              x[1].split('-')[1] == '06' and
              x[1].split('-')[0] == '2009',
    zip(date_view['sentiment'], date_view['norm_date'], date_view['count'])
))

print((len(pos_tweets)/(len(pos_tweets) + len(neg_tweets)) * 100))