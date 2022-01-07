##########################################################
#####################  IMPORTANT  ########################
##########################################################

# Execute the following commands before do the test.
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

from utils import *
from tqdm import tqdm
from functools import reduce

DATA_FEATURES = ['sentiment', 'id', 'date', 'flag', 'user', 'text']
DATE_FORMAT = '%a %b %d %H:%M:%S PDT %Y'


def user_sentiment_view(input_dir='input', output_dir='output'):
    print('Map-reduce user-sentiment...')
    data = read_input(
        input_dir, DATA_FEATURES)
    # Map step
    # ['sentiment','id','date','flag','user','text'] -> ['user','sentiment',1]
    map_user_sent = tqdm(zip(
        data['user'], data['sentiment']
    ), desc='Making map')

    # First reduce
    # ['user','sentiment'] -> {('user','sentiment'): count]

    def update(d, k):
        if k in d:
            d[k] += 1
        else:
            d[k] = 1
        return d

    dic_user_sent = reduce(
        lambda x, y: update(x, (y[0], y[1])),
        tqdm(map_user_sent, desc='Processing First reduce'), {}
    )

    # Second reduce
    # {('user','sentiment'): count} ->
    # ['user','neg-','neg','neutral','pos','pos+']

    def update(d, k, v):
        if k in d:
            d[k][v[0]] += v[1]
        else:
            d[k] = [0] * 5
            d[k][v[0]] = v[1]
        return d

    dic_user = reduce(
        lambda x, y: update(x, y[0], [y[1], dic_user_sent[y]]),
        tqdm(dic_user_sent.keys(), desc='Processing Second reduce 1/2'), {}
    )

    list_user = map(
        lambda x: [x, dic_user[x][0],
                   dic_user[x][1],
                   dic_user[x][2],
                   dic_user[x][3],
                   dic_user[x][4]],
        tqdm(dic_user.keys(), desc='Processing Second reduce 2/2')
    )

    write_output(list_user, 'user_sentiment.csv', output_dir)
    print('Finish')


def word_sentiment_view(input_dir='input', output_dir='output'):
    print('Map-reduce word_sentiment...')
    data = read_input(
        input_dir, DATA_FEATURES)

    # Map step
    # ['sentiment','id','date','flag','user','text'] -> ['words','sentiment',1]

    words_sent = map(
        lambda x: [
            text_prepare(x[0]),
            x[1]
        ],
        tqdm(zip(data['text'], data['sentiment']), desc='Making map')
    )

    # Reduce step
    # ['words','sentiment',1] -> ['word','sentiment','count']

    def update(d, words, sent):
        for w in words:
            k = (w, sent)
            if k in d:
                d[k] += 1
            else:
                d[k] = 1
        return d

    dict_word_sent = reduce(
        lambda x, y: update(x, y[0], y[1]),
        tqdm(words_sent, desc='Processing reduce 1/2'), {}
    )

    word_sent = map(
        lambda x: [x[0], x[1], dict_word_sent[x]],
        tqdm(dict_word_sent.keys(), desc='Processing reduce 2/2')
    )

    write_output(word_sent, 'word_sentiment.csv', output_dir)
    print('Finish')


def sentiment_date_view(input_dir='input', output_dir='output'):
    print('Map-reduce sentiment_date...')
    data = read_input(
        input_dir, DATA_FEATURES)

    # Map step
    # ['sentiment', 'id', 'date', 'flag', 'user', 'text'] ->
    # ['sentiment', 'norm_date', 1]

    map_sent_date = map(
        lambda x: (x[0], norm_date(x[1], DATE_FORMAT)),
        tqdm(zip(data['sentiment'], data['date']), desc='Making map')
    )

    # Reduce step
    # ['sentiment', 'norm_date', 1] -> ['sentiment', 'norm_date', 'count']

    def update(d, k):
        if k in d:
            d[k] += 1
        else:
            d[k] = 1
        return d

    dict_sent_date = reduce(
        lambda x, y: update(x, y),
        tqdm(map_sent_date, desc='Processing reduce 1/2'), {}
    )

    sent_date = map(
        lambda x: [x[0], x[1], dict_sent_date[x]],
        tqdm(dict_sent_date.keys(), desc='Processing reduce 2/2')
    )

    write_output(sent_date, 'sentiment_date.csv', output_dir)
    print('Finish')


if __name__ == '__main__':
    user_sentiment_view()
    word_sentiment_view()
    sentiment_date_view()
