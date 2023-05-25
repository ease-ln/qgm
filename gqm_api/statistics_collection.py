import re
import csv
import nltk
import json
import pandas as pd
from scipy.sparse import lil_matrix

from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.metrics import f1_score
from sklearn.metrics import hamming_loss
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer

from skmultilearn.adapt import MLkNN
from skmultilearn.ensemble import RakelD
from skmultilearn.problem_transform import BinaryRelevance
from skmultilearn.problem_transform import ClassifierChain


nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

BASE_PATH = '/home/shuva/Projects/metricsRecommender/venv/'
PATH = 'MetricsRecommender/gqm_api/questions.tsv'
PATH_TO_CSV = 'MetricsRecommender/gqm_api/questions.csv'
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


def measurements(text, accuracy, f1, hamming):
    print(text + "Accuracy = ", accuracy)
    print(text + "F1 score = ", f1)
    print(text + "Hamming loss = ", hamming)


def make_predictions(x_train, y_train, x_test, y_test, classifier, text):
    classifier.fit(x_train, y_train)
    # predict
    predictions = classifier.predict(x_test)
    measurements(text=text,
                 accuracy=accuracy_score(y_test, predictions),
                 f1=f1_score(y_test, predictions, average="micro"),
                 hamming=hamming_loss(y_test, predictions)
                 )


def knn(x_train, y_train, x_test, y_test):
    classifier = MLkNN(k=3)
    # to prevent errors when handling sparse matrices.
    x_train = lil_matrix(x_train).toarray()
    y_train = lil_matrix(y_train).toarray()
    x_test = lil_matrix(x_test).toarray()
    classifier.fit(x_train, y_train)
    # predict
    knn_predictions = classifier.predict(x_test)
    measurements(text="KNN ",
                 accuracy=accuracy_score(y_test, knn_predictions),
                 f1=f1_score(y_test, knn_predictions, average="micro"),
                 hamming=hamming_loss(y_test, knn_predictions)
                 )


def create_statistics():
    dataset = binarization(pd.read_csv(BASE_PATH + PATH, sep='\t', header=None))
    x_train, x_test, y_train, y_test = train_test_split(
        dataset['content'], dataset[dataset.columns[5:]], test_size=0.1, random_state=0)
    # vectorization
    x_train, x_test = vectorization(x_train, x_test)
    # make predictions
    classifiers = {
        "Binary relevance ": BinaryRelevance(GaussianNB()),
        "Classifier chains ": ClassifierChain(GaussianNB()),
        "Label powerset ": ClassifierChain(
            classifier=RandomForestClassifier(n_estimators=100),
            require_dense=[False, True]
        ),
        "RAkEL ": RakelD(
            base_classifier=GaussianNB(),
            base_classifier_require_dense=[True, True],
            labelset_size=52
        ),
        "Decision trees ": DecisionTreeClassifier()
    }
    for text, classifier in classifiers.items():
        make_predictions(x_train, y_train, x_test, y_test, classifier, text)
    knn(x_train, y_train, x_test, y_test)
    return []

create_statistics()
