from bs4 import BeautifulSoup as bs
import csv 
import requests 

def get_tickers():
    tickers = []
    with open('tickers.csv') as ticker_file:
        for ticker in ticker_file:
            tickers.append(ticker.strip())
    return tickers

def to_csv(stocks):
    with open('dividends.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(stocks[0].keys())
        for stock in stocks:
            writer.writerow(stock.values())

def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')

def get_data(ticker):
    url = 'https://www.lse.co.uk/share-fundamentals.asp?shareprice='
    soup = get_soup(url + ticker)
    try: 
        table = soup.find_all('table', attrs={'class', 'sp-fundamentals-info__table'})[1]
        dividend = table.find_all('tr')[5].find('td').text
        div_yield = table.find_all('tr')[6].find('td').text

        print(f'Dividend for {ticker} : {dividend}')

        return {
                'ticker': ticker, 
                'dividend': dividend, 
                'yield': div_yield
               }
    except: 
        print('No information available for ', ticker)


if __name__ == '__main__':
    dividends = []
    for ticker in get_tickers():
        dividends.append(get_data(ticker))
    to_csv(dividends)
