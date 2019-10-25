from bs4 import BeautifulSoup
import requests
import time
from random import randint
def scrape_news_summaries(s):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    time.sleep(randint(0, 2))  # relax and don't let google be angry
    r = requests.get("http://www.google.com/search?q="+s+"&tbm=nws", headers=headers)
    print(r.status_code)  # Print the status code
    content = r.text
    news_summaries = []
    news_link = []
    news_photo = []
    soup = BeautifulSoup(content, "html.parser")
    llLrAF_a = soup.findAll("h3", attrs = {"class": "r"})
    st_divs = soup.findAll("div", {"class": "st"})
    for st_div in st_divs:
        news_summaries.append(st_div.text)
    return news_summaries
    for l in soup.find_all("a", {"class": "lLrAF"}):
        news_link.append(l.get('href'))
    return news_link    
    for l in soup.find_all("img", {"class": "th"}):
        news_photo.append(l.get('src'))
    return news_photo    
  
l = scrape_news_summaries("sheila")
#l = scrape_news_summaries("""T-Notes""")
for n in l:
    print(n)