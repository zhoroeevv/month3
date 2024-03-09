from bs4 import BeautifulSoup
import requests

number_news = 0
for page in range(1,21):
    url = f'https://24.kg/page_{page}/'
    respone = requests.get(url=url)
    # print(respone)
    soup = BeautifulSoup(respone.text, 'lxml')
    # print(soup)
    all_news = soup.find_all('div', class_ ='title')
    # print(all_news)
    
    for news in all_news:
        number_news += 1
        print(f"{number_news}) {news.text}")

