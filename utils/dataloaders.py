import glob
import html
import os
import re

from sklearn.model_selection import train_test_split

from config import DATA_DIR


def parse_csv(data_file):
    """

    Returns:
        X: a list of tweets
        y: a list of labels corresponding to the tweets

    """
    with open(data_file, 'r') as fd:
        data = [l.strip().split('\t') for l in fd.readlines()][1:]
    X = [d[2] for d in data]
    y = [d[1] for d in data]
    return X, y


def clean_text(text):
    """
    Remove extra quotes from text files and html entities
    Args:
        text (str): a string of text

    Returns: (str): the "cleaned" text

    """
    text = text.rstrip()

    if '""' in text:
        if text[0] == text[-1] == '"':
            text = text[1:-1]
        text = text.replace('\\""', '"')
        text = text.replace('""', '"')

    text = text.replace('\\""', '"')

    text = html.unescape(text)
    text = re.sub("un\[#TRIGGERWORD#\]", 'not [#TRIGGERWORD#]', text)
    text = re.sub("Un\[#TRIGGERWORD#\]", 'not [#TRIGGERWORD#]', text)
    text = re.sub("[^\s]+\[#TRIGGERWORD#\]", ' [#TRIGGERWORD#]', text)
    text = ' '.join(text.split())
    return text


def parse_file(file):
    """
    Read a file and return a dictionary of the data, in the format:
    tweet_id:{sentiment, text}
    """

    data = {}
    lines = open(file, "r", encoding="utf-8").readlines()
    for line_id, line in enumerate(lines):
        columns = line.rstrip().split("\t")
        tweet_id = columns[0]
        sentiment = columns[1]
        text = columns[2:]
        text = clean_text(" ".join(text))
        data[tweet_id] = (sentiment, text)
    return data


def sentence_dataset(file):
    data = []
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            data.append(line.rstrip())
        return data


def load_data_from_dir(path):
    FILE_PATH = os.path.dirname(__file__)
    files_path = os.path.join(FILE_PATH, path)

    files = glob.glob(files_path + "/**/*.tsv", recursive=True)
    files.extend(glob.glob(files_path + "/**/*.txt", recursive=True))

    data = {}  # use dict, in order to avoid having duplicate tweets (same id)
    for file in files:
        file_data = parse_file(file)
        data.update(file_data)
    return list(data.values())


def load_wassa(dataset="train", split=0.1):
    """
    Read a file and return a dictionary of the data, in the format:
    line_id:{emotion, text}

    Args:
        dataset:

    Returns:

    """
    file = os.path.join(DATA_DIR, "wassa_2018", "{}.csv".format(dataset))

    X = []
    y = []
    lines = open(file, "r", encoding="utf-8").readlines()
    for line_id, line in enumerate(lines):
        columns = line.rstrip().split("\t")
        emotion = columns[0]
        text = columns[1:]
        text = clean_text(" ".join(text))
        X.append(text)
        y.append(emotion)

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=split,
                                                        stratify=y,
                                                        random_state=52)

    return X_train, X_test, y_train, y_test
