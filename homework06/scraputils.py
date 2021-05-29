import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    # PUT YOUR CODE HERE
    news_list = []

    title = parser.select(".storylink")
    title_list = []
    url_list = []
    subtext = parser.select(".subtext")
    author_list = []
    points_list = []
    comments_list = []

    for x in title:
        title_list.append(x.text)
        url = x.get("href", None)
        url_list.append(url)

    for i in range(len(subtext)):
        author = subtext[i].select(".hnuser")
        if author == []:
            author = "None"
        else:
            author = author[0].text
        author_list.append(author)

        points = subtext[i].select(".score")
        if points == []:
            points = 0
        else:
            points = int(points[0].text.split()[0])
        points_list.append(points)

        comments = subtext[i].findAll("a")[-1]
        print(comments)
        if comments.text == "discuss" or comments.text == "hide":
            comments = 0
        else:
            comments = int(comments.text.split("\xa0")[0])
        print(comments)
        comments_list.append(comments)

        news_list.append({'author': author_list[i],
                          'points': points_list[i],
                          'title': title_list[i],
                          'url': url_list[i],
                          'comments': comments_list[i]})
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    # PUT YOUR CODE HERE
    more = parser.select(".morelink")
    if len(more) == 0:
        return None
    return str(more[0]["href"])


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        if next_page is None:
            n_pages = 0
        else:
            url = "https://news.ycombinator.com/" + next_page
            news.extend(news_list)
            n_pages -= 1
    return news
