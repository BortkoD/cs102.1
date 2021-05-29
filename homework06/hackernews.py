from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier, clean


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    query = request.query.decode()
    id = int(query["id"])
    label = query["label"]
    s = session()
    s.query(News).filter(News.id == id).update({News.label: label})
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    s = session()
    news = get_news("https://news.ycombinator.com/news", 3)
    for x in news:
        news_if_exist = s.query(News).filter(News.title == x.title, News.author == x.author)
        if not news_if_exist:
            s.add(x)
            s.commit()
    redirect("/news")


@route("/recommendations")
def recommendations():
    # PUT YOUR CODE HERE
    s = session()
    labeled = s.query(News).filter(News.label is not None).all()
    not_labeled = s.query(News).filter(News.label is None).all()
    model = NaiveBayesClassifier(0.05)
    X_train, y_train = [], []
    for new in labeled:
        X_train.append(new.title)
        y_train.append(new.label)
    X_train = [clean(x).lower() for x in X_train]
    model.fit(X_train, y_train)
    not_labeled = clean([x.title for x in not_labeled]).lower()
    prediction = zip(not_labeled, model.predict(not_labeled))
    for title, label in prediction:
        title.label = label
    sorted_news = sorted(not_labeled, key=lambda news: news.label)
    return template("news_template", rows=sorted_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
