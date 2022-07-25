#Hynix PlotChart 
import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import mplfinance as mpf

def main():
    url = "https://finance.naver.com/item/sise_day.nhn?code=000660&page=1"
    last=max_page(url)
    data=get_data(url,last)
    display(data)
  
def max_page(url):
    headers = {
        'user-agent': "Mozilla/5.0"
    }
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "lxml")
    pgrr = soup.find("td",{"class":"pgRR"}).a['href'].split("=")
    max_page = pgrr[-1]
    return(max_page)

def get_data(url,last):
    url = url[:-7]
    df = pd.DataFrame()
    for page in range(1,int(last)+1):
        page_url = f"{url}&page={page}"
        headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        result = requests.get(page_url, headers=headers)
        data = pd.read_html(result.text, header=0)[0]
        df = df.append(data, ignore_index=True)
    df = df.dropna()
    df = df.sort_values(by="날짜")
    return (df)
    # df.append(pd.read_html(data))
    # return (df)

def display(data):
    df = data
    plt.title('Hynix (close)')
    plt.xticks(rotation=45) #rotate dates cuz other wise they'll overlap one another
    plt.plot(df['날짜'], df['종가'], 'co-') #co = cyan color
    plt.grid(color='gray', linestyle='--')
    plt.show()
main()
