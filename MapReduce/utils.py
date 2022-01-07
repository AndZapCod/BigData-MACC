import pandas as pd
import csv
import os
import re

from datetime import datetime
from nltk import word_tokenize
from nltk.corpus import stopwords

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))


def read_input(input_dir, head):
    files = os.listdir(input_dir)
    data = pd.DataFrame()
    for file in files:
        path = os.path.join(input_dir, file)
        df = pd.read_csv(path, names=head, header=None)
        data = pd.concat([data, df])
    return data


def write_output(data, name='output.csv', output_dir='output'):
    path = os.path.join(output_dir, name)
    with open(path, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def text_prepare(text):
    """
        :param text: a string
        :return: modified initial string
    """

    # lowercase text
    text = text.lower()
    # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = re.sub(REPLACE_BY_SPACE_RE, ' ', text)
    # delete symbols which are in BAD_SYMBOLS_RE from text
    text = re.sub(BAD_SYMBOLS_RE, "", text)
    # delete stopwords from text
    text = [w for w in word_tokenize(text) if w not in STOPWORDS]

    return text


def norm_date(str_date, f):
    """
    :param str_date: string date with f as format
    :param f: format of the string ex. (%Y-%m-%d %H:%M:%S.%f)
    :return: string with format (%Y-%m-%d)
    """
    date = datetime.strptime(str_date, f)
    return date.strftime('%Y-%m-%d')
