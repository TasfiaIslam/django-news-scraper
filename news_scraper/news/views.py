from django.shortcuts import render
from django.http import HttpResponse
from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import requests
import re

from decouple import config

# Views


def home(request):

    url = "https://www.dhakatribune.com/articles/sport/cricket/"  # url
    source = requests.get(url).text  # url source

    # beautifulsoup
    soup = BeautifulSoup(source, 'html.parser')

    news_divs = soup.find_all('div', class_='top-news-cont list-para')
    img_divs = soup.find_all('div', class_='top-news')

    # empty lists to append later
    paras = []
    headings = []
    images = []
    detail_urls = []

    for i in range(len(news_divs)):

        news = news_divs[i]

        headings.append(news.a.h4.text)
        paras.append(news.p.text)
        detail_urls.append('https://www.dhakatribune.com'+news.a['href'])

        for j in range(len(img_divs)):
            img_section = img_divs[j]

            img = img_section.a.img
            img_url = img['src']
            images.append(img_url)

    mylist = zip(headings, paras, images, detail_urls)

    api = NewsApiClient(api_key=config('API_KEY'))
    topheadlines = api.get_top_headlines(sources='al-jazeera-english')

    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])

    mylist2 = zip(news, desc, img, url)

    context = {'mylist': mylist, 'mylist2': mylist2}

    return render(request, 'news/index.html', context)
