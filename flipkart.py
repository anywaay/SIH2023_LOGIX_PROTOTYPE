
from bs4 import BeautifulSoup
import requests
import json
from flask import Flask, request

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  
}

app = Flask(__name__)


@app.route('/r', methods=['POST'])
def run_script():
    try:
        data = request.get_json()  
        ls = data["array"]
        # ls= "acer Intel Core i5 15.6 Inch Laptop"/
        # ls=ls.replace(" ","+")
        search_term = ls[0]  # Get the search term from the POST request
        search_term = search_term.replace(" ", "+")
        if not search_term:
            return("No search term provided.")
        url = f"https://www.flipkart.com/search?q={search_term}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            product_cards = soup.find_all('div', class_='_1AtVbE col-12-12')

            for card in product_cards:
                product_info = {}
                title_elem = card.find('div', class_='_4rR01T')
                if title_elem:
                    
                    product_info['title'] = title_elem.text.strip()

                price_elem = card.find('div', class_='_30jeq3 _1_WHN1')
                if price_elem:
                    
                    product_info['price'] = price_elem.text.strip()

                link_elem = card.find('a', class_='_1fQZEK')
                if link_elem:
                    product_info['link'] = 'https://www.flipkart.com' + link_elem.get('href')
                results.append(product_info)

            json_data = json.dumps(results)
            if json_data:
                return json_data

        return "No JSON data available."

    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True, port=7000)
