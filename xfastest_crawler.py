import requests
from bs4 import BeautifulSoup


def get_news(url):
    news = []

    html = requests.get(url)
    sp = BeautifulSoup(html.text, 'html.parser')
    data_list = sp.select(".vw-block-grid-item")

    for data in data_list:
        date_published = data.find("time")
        if date_published is None:
            break
        else:
            title = data.find("h3", {"class": "vw-post-box-title"})
            link = title.find("a").get('href')
            title = title.text.lstrip(' ')
            news.append([date_published.text, title, link])

    return news


if __name__ == '__main__':
    home_url = "https://news.xfastest.com/"
    amd_url = "https://news.xfastest.com/category/amd/"
    news = get_news(amd_url)
    print(news)

