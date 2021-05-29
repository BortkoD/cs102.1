import math
from collections import Counter
import csv
import string


class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.model: dict = {"labels": {}, "words": {}}

    def fit(self, X, y): # работа с обучающей выборкой
        """ Fit Naive Bayes classifier according to X, y. """
        marked_words = []  # список слов и соответствующих им отметок
        for title, label in zip(X, y):
            for word in title.split():
                mark = (word, label)  # сопоставляем всем словам из заголовка проставленную оценку
                marked_words.append(mark)

        self.unique_words = Counter(marked_words)  # соответствие (слово с опр. оценкой) - (сколько совпадений)
        # print("unique_words", self.unique_words)

        self.counted_dict = dict(Counter(y))  # возможные отметки и кол-во соответствующих элементов
        # print("counted_dict", self.counted_dict)

        words = [word for title in X for word in title.split()]
        self.counted_words = dict(Counter(words))  # словарь с соответствиями "слово"-"сколько раз встречается"
        # print("counted_words", self.counted_words)

        self.model = {"labels": {}, "words": {}}

        for mark_type in self.counted_dict:
            count = 0
            for word, label_name in self.unique_words:
                if mark_type == label_name:
                    count += self.unique_words[(word, mark_type)]  # сколько раз встречалось уникальное слово с
                    # конкретной меткой
            params = {
                "label_count": count,
                "probability": self.counted_dict[mark_type] / len(y), # вероятность того, что объект относится к
                # конкретному классу
            }
            self.model["labels"][mark_type] = params

        for word in self.counted_words:
            params = {}
            for edition in self.counted_dict:
                nc = self.model["labels"][edition]["label_count"]
                nic = self.unique_words.get((word, edition), 0)
                counted_len = len(self.counted_words)
                alpha = self.alpha
                smooth = (nic + alpha) / (nc + alpha * counted_len)
                params[edition] = smooth
            self.model["words"][word] = params

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        words = X.split()
        chance = []
        for cur_label in self.model["labels"]:
            probability = self.model["labels"][cur_label]["probability"]
            total_grade = math.log(probability, math.e)
            for word in words:
                word_dict = self.model["words"].get(word, None)
                if word_dict:
                    total_grade += math.log(word_dict[cur_label], math.e)
            chance.append((total_grade, cur_label))
        _, prediction = max(chance)
        return prediction

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        correct = []
        for one in X_test:
            correct.append(self.predict(one))
        try:
            return sum(0 if correct[i] != y_test[i] else 1 for i in range(len(X_test))) / len(X_test)
        except ZeroDivisionError:
            pass


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


def test():
    with open("./data/SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X = [clean(x).lower() for x in X]
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    model = NaiveBayesClassifier(0.05)
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))


test()
