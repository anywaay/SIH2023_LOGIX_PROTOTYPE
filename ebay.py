import requests
import json
from flask import Flask, request
from os.path import basename
from bs4 import BeautifulSoup
app=Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

@app.route("/ebay",methods=["POST"])
def run_script():
    try:
        data = request.get_json()  
        ls = data['array']
        search= ls[0]
        if not search:
            return "No search term provided."
        search = search.replace(" ", "+")
        url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={search}&_sacat=0&_odkw=hp&_osacat=0"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            product,result={},[]
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.body.find_all(class_="s-item__wrapper clearfix")
            for i in range(1, len(cards)):
                product["title"]= cards[i].find_all('div', class_="s-item__title")
                # print(title[0].text)
                links = cards[i].find_all(class_="s-item__link")
                for link in links:
                    product["link"]= link.get('href')
                    # print(l)
                product["price"]= cards[i].find_all(class_="s-item__price")
                # print(price[0].text)
                result.append(product)
            json_data=json.dumps(result)
            if json_data:
                return json_data

        return "No JSON data available."
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True, port=8000)