from bs4 import BeautifulSoup


from bs4 import BeautifulSoup
import requests
import json
from flask import Flask, request

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  
}

app = Flask(__name__)

def flipkart(search):
    url = f"https://www.flipkart.com/search?q={search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
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
            rating=card.find('div',class_="_3LWZlK")
            if rating:
                product_info['rating'] = rating.text.strip()

            # link_elem = card.find('a', class_='IRpwTa')
            link_elem = card.find('a', class_='_1fQZEK')
            if link_elem:
                product_info['link'] = 'https://www.flipkart.com' + link_elem.get('href')
            results.append(product_info)

        return results
    return []

def ebay(search):
    url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={search}&_sacat=0&_odkw=hp&_osacat=0"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = []
        soup = BeautifulSoup(response.text, 'html.parser')
        # cards = soup.find_all(class_="s-item__info")
        cards = soup.find_all(class_="s-item")

        for card in cards:
            product = {}
            
            title_elem = card.find('div', class_="s-item__title")
            if title_elem:
                product["title"] = title_elem.text.strip()

            link_elem = card.find('a', class_="s-item__link")
            if link_elem:
                product["link"] = link_elem.get('href')

            price_elem = card.find(class_="s-item__price")
            if price_elem:
                product["price"] = price_elem.text.strip()

            rating=card.find(class_="x-star-rating")
            if rating:
                product["rating"]=rating.text.strip()
            else:
                product["rating"]="N/A"

            result.append(product)

        return result
    return []

def alibaba(search):
    url = f"https://www.alibaba.com/trade/search?spm=a2700.product_home_newuser.home_new_user_first_screen_fy23_pc_search_bar.keydown__Enter&tab=all&searchText={search}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        l = []
        soup = BeautifulSoup(response.text, 'html.parser')
        # cards = soup.find_all('div', class_="content")
        cards = soup.find_all('div', class_="item-main")

        for card in cards:
            d = {}
            title_elem = card.find('div', class_="title")
            if title_elem:
                d["title"] = title_elem.text.strip()

            price_elem = card.find('div', class_="price")
            if price_elem:
                d["price"] = price_elem.text.strip()

            link_elem = card.find('a', class_="item-title-text")
            if link_elem:
                d["link"] = link_elem.get('href')

            l.append(d)

        return l
    return []

@app.route('/ebay', methods=['POST'])
def run_script():
    try:
        data = request.get_json()  
        ls = data["array"]
        search = ls[0]
        search = search.replace(" ", "+")
        if not search:
            return "No search term provided."
        else:
            d = {}
            d["flipkart"] = flipkart(search)
            d["ebay"] = ebay(search)
            d["alibaba"] = alibaba(search)
            json_data = json.dumps(d)
            return json_data
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
