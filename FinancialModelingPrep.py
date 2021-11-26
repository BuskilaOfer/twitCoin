import json
from urllib.request import urlopen


def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


class FinancialModelingPrep:

    def __init__(self):
        self.url = "https://financialmodelingprep.com/api/v3/quote/"
        self.apikey = "9c33655ac70d040280297ef04cf3ceff"

    def get_stock_price(self, stock_name):
        stock_url = self.url + str(stock_name) + "?apikey=" + self.apikey
        parsed_data = get_jsonparsed_data(stock_url)[0]
        price = parsed_data["price"]
        return int(price)


if __name__ == '__main__':
    fmp = FinancialModelingPrep()
    bitcoin_price = fmp.get_stock_price("BTCUSD")
    print(bitcoin_price)
