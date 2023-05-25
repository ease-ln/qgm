import re
import os
import nltk
import csv
import json
import pandas as pd
from .models import Question

from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from skmultilearn.problem_transform import LabelPowerset
from sklearn.feature_extraction.text import TfidfVectorizer
from skmultilearn.problem_transform import BinaryRelevance

from scipy.sparse import lil_matrix

nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

BASE_PATH = os.path.abspath(os.getcwd())
PATH = '/gqm_api/questions.tsv'
PATH_TO_CSV = '/gqm_api/questions.csv'
stopwords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    # bring the text to the general form and remove unnecessary symbols
    text = text.lower()  # convert all words to the lower case
    text = re.sub('[\W\d]', ' ', text)  # change everything besides letters on space
    text = re.sub('\s+', ' ', text)  # combine all unnecessary spaces
    text = text.strip(' ')  # delete spaces from the beginning and the end of the sentence
    text = ' '.join(word for word in text.split() if word not in stopwords)  # remove stop words
    return text


def get_pos(word):
    # define the part of speech for each word
    pos = nltk.pos_tag([word])[0][1][0].upper()  # define the letter which stay for the part of speech of this word
    pos_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return pos_dict.get(pos, wordnet.NOUN)  # return the part of speech, if not - return NOUN


def lemmatization(text):
    lemm_text = ""  # empty twin of our question - we will build it from parts
    for word in text.split():
        lemm = lemmatizer.lemmatize(word, get_pos(word))  # reducing a word form to its standard form
        lemm_text += lemm  # add word in standard form to the twin of our question
        lemm_text += " "  # add space between words
    lemm_text = lemm_text.strip()  # delete spaces from the beginning and the end of the sentence
    return lemm_text


def create_dictionary(question):
    # decompose an object into fields
    question_id = question.id
    if not question.content:
        content = "no"
    else:
        content = question.content
    goal_id = question.goal_id
    metrics = question.metrics.all()
    # create the dictionary with metrics
    metrics_dict = {}
    i = 1
    for item in metrics:
        metrics_dict[str(i)] = item.name
        i += 1
    return {'id': question_id,
            'content': content,
            'goal_id': goal_id,
            'metrics': metrics_dict
            }


def create_csv(dataset, path):
    try:
        with open(path, 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            for item in dataset:
                writer.writerow([item['id'], item['content'], item['goal_id'], item['metrics']])
    except BaseException as e:
        print('BaseException:', path)
    else:
        print('Data has been loaded successfully !')


def binarization(dataset):
    dataset.columns = ["id", "content", "goal_id", "metrics"]
    questions_lists = []
    for item in dataset["metrics"]:
        item = item.replace('\'', '\"')  # without this wil not work¯\_(ツ)_/¯
        questions_lists.append(list(json.loads(item).values()))  # create list of lists with metrics
    dataset["metrics"] = questions_lists  # change dicts in file to lists
    # "One-Hot-Encode" metrics
    mlb = MultiLabelBinarizer()
    mlb.fit_transform(dataset["metrics"])
    y = mlb.transform(dataset["metrics"])
    for idx, tag in enumerate(mlb.classes_):
        dataset[tag] = y[:, idx]
    dataset.to_csv(BASE_PATH + PATH_TO_CSV)
    new_dataset = pd.read_csv(BASE_PATH + PATH_TO_CSV)
    dataset = new_dataset
    return dataset


def vectorization(x_train, x_test):
    vectorizer = TfidfVectorizer(max_features=3000)
    vectorizer.fit(x_train)
    vectorizer.fit(x_test)
    x_train = vectorizer.transform(x_train)
    x_test = vectorizer.transform(x_test)
    return x_train, x_test


def binary_relevance(x_train, y_train, x_test):
    classifier = BinaryRelevance(GaussianNB())
    classifier.fit(x_train, y_train)
    # predict
    predictions = classifier.predict(x_test)
    return predictions.toarray()


def create_metrics(content, question_id):
    questions = Question.objects.exclude(pk=question_id)  # get all questions and all metrics assigned to them
    # text preprocessing
    for item in questions:
        item.content = clean_text(item.content)
        item.content = lemmatization(item.content)
    questions = list(map(lambda x: create_dictionary(x), questions))  # transform QuerySet into list of dictionaries
    # create tsv file
    # if not os.path.exists(BASE_PATH + PATH):
    create_csv(questions, BASE_PATH + PATH)
    # putting tags variable into separate binary columns
    dataset = binarization(pd.read_csv(BASE_PATH + PATH, sep='\t', header=None))
    # User's new question preprocessing
    content = clean_text(content)
    content = lemmatization(content)
    # dividing into training and test sets
    x_train = dataset["content"]
    y_train = dataset[dataset.columns[5:]]
    x_test = [content]
    # vectorization
    x_train, x_test = vectorization(x_train, x_test)
    # decision trees
    predictions = binary_relevance(x_train, y_train, x_test)
    # map array of 0 and 1 into metrics names
    metrics_names = dataset.columns[5:]
    metrics = []
    counter = 0
    for item in predictions[0]:
        if item != 0:
            metrics.append(metrics_names[counter])
        counter += 1
    if not metrics:
        metrics = []
    # map metrics names to metrics ids
    # metrics = list(map(lambda x: Metrics.objects.get(name=x).id, metrics))
    return metrics
