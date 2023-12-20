from bs4 import BeautifulSoup
import requests
import json
from flask import Flask, request
import pandas as pd
import csv



app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def des(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.body.find_all('table', class_="table")
        if not table:
            print("Table not found.")
            return

        heading = table[0].find_all('th')
        header = [h.text.strip() for h in heading]

        tb = table[0].find_all('tbody')
        if not tb:
            print("Table body not found.")
            return

        n = tb[0].find_all('div', class_="seller-info")
        p = tb[0].find_all('span', class_="variant-final-price")
        d = tb[0].find_all(class_="delivery-locations")
        q = tb[0].find_all(class_="quantity-based-discount")
        qa = tb[0].find_all(class_="quantity-available")
        minq = tb[0].find_all(class_="moq")
        ofp = tb[0].find_all(class_="offer-product")
        ori = tb[0].find_all(class_="country-of-origin")

        data1 = []
        with open("seller_data.csv", "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            for i in range(0, len(n)):
                if q[i].text == "\n":
                    q[i] = "N/A"
                else:
                    q[i] = q[i].text.strip()

                data = [
                    n[i].text.strip().replace('\n', ' '),
                    p[i].text.strip()[1:],
                    d[i].text.strip(),
                    q[i],
                    qa[i].text.strip(),
                    minq[i].text.strip(),
                    ofp[i].text.strip(),
                    ori[i].text.strip()
                ]
                print(data)
                csv_writer.writerow(data)
                data1.append(data)

        excel_file = 'seller_data.xlsx'
        df = pd.read_csv("seller_data.csv")

        for i in range(0, len(df['Offer Price'])):
            df['Offer Price'][i] = pd.to_numeric(df['Offer Price'][i].replace(",", ""), errors='coerce')

        # Sort the DataFrame based on the 'Offer Price' column
        df_sorted = df.sort_values(by='Offer Price')

        reseller_rows = df_sorted[df_sorted['Offer Product As'].str.lower().eq('resellers')]
        oem_rows = df_sorted[df_sorted['Offer Product As'].str.lower().eq('oem')]

        # Check if there are any matching rows before accessing the first one
        if not reseller_rows.empty:
            reseller_row = reseller_rows.iloc[0].to_dict()
        else:
            reseller_row = None

        if not oem_rows.empty:
            oem_row = oem_rows.iloc[0].to_dict()
        else:
            oem_row = None

        result1 = {
            "First_Reseller": reseller_row,
            "First_OEM": oem_row
        }

        json_data = json.dumps(result1, indent=2, default=str)
        return json_data

    else:
        print("Failed to fetch the webpage")

def extract_product_details(div, featuredictionary):
    pdetails = div.find_all('div', class_="product-details")
    for product in pdetails:
        instock = product.find_all('span', class_="pdp-availability")
        for i in instock:
            stocka = i.find_all('strong', class_="green")
            if stocka:
                featuredictionary['in_stock'] =""+ stocka[0].text.strip().replace('\n', ' ')
            else:
                featuredictionary['in_stock']="N/A"
        minq = product.find_all('span', class_="moq_data")
        if minq:
            featuredictionary['minimum_quantity'] = ""+minq[0].text.strip()
        else:
            featuredictionary['minimum_quantity']="N/A"
        productid = product.find_all('span', class_="item_sku")
        if productid:
            featuredictionary['product_id'] = ""+productid[0].text.strip()
        else:
            featuredictionary['product_id']="N/A"
        origin = product.find_all('span', class_="origin_country_data")
        if origin:
            featuredictionary['origin'] = ""+origin[0].text.strip()
        else:
            featuredictionary['origin']="N/A"
        price = product.find_all('span', class_="m-w")
        if price:
            featuredictionary['price'] = ""+price[0].text.strip()
        else:
            featuredictionary['price']="N/A"
        mit = product.find_all('span', class_="mii_percentage_data")
        if mit:
            featuredictionary['mit'] = ""+mit[0].text.strip()
        else:
            featuredictionary['mit']="N/A"
        pricefor = product.find_all('div', class_="pdp-qty-message")
        if pricefor:
            featuredictionary['pricefor'] = ""+pricefor[0].text.strip().replace('\n', ' ')
        else:
            featuredictionary['pricefor']="N/A"

def extract_seller_details(div, featuredictionary):
    sellerdetails = div.find_all('div', class_='seller-details')
    for detail in sellerdetails:
        sellertype = detail.find_all('span', class_='sold_as_summary')
        if sellertype:
            featuredictionary['sellertype'] = sellertype[0].text.strip().replace('\n', ' ')
        else:
            featuredictionary['sellertype']="N/A"
        verificationstatus = detail.find_all('div', class_="seller-verified-status")
        if verificationstatus:
            featuredictionary['verificationstatus'] = verificationstatus[0].text.strip()
        else:
            featuredictionary['verificationstatus'] ="N/A"
        rating = detail.find_all('span', class_="badge")
        if rating:
            featuredictionary['rating'] = rating[0].text.strip()
        else:
            featuredictionary['rating']='0'
        sellerslink = detail.find_all('a', class_="sellers_summary")
        if sellerslink:
            first_seller_link = sellerslink[0].get('href')
            if first_seller_link:
                featuredictionary['sellerslink'] = 'https://mkp.gem.gov.in' + first_seller_link
            else:
                featuredictionary['sellerslink'] = 'No seller link available'
        else:
            featuredictionary['sellerslink'] = 'No seller link available'

def extract_images(div, featuredictionary):
    images = div.find_all('img')
    i=1
    for image in images:
        im = image.get('src')
        featuredictionary[f'img{i}'] = im
        i=i+1

def extract_features(soup, featuredictionary):
    features = soup.body.find_all('div', id='feature_groups')
    row = features[0].find_all('tr')
    for r in row:
        data = r.find_all('td')
        if data[0] and data[1]:
            featuredictionary[data[0].text.strip().replace(' ', '_').replace('&', '_').replace(':', '_').replace('.', '_').replace('±', '_').replace('#', '_').replace('@', '_').replace('-', '_').replace('+', '_').replace('/', '_').replace('(', '_').replace(')', '_')] = data[1].text.strip()

def gem_scraper(url):
    response = requests.get(url, headers=headers)
    featuredictionary = {}
    itemdetails = ""
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        itemdetails = soup.body.find_all('div', class_='page_bg')
        for div in itemdetails:
            titles = div.find_all('h1', class_='like-h3')
            for title in titles:
                title_text = title.contents[0].strip() if title.contents else ""
                brand = title.find_all('span', class_="brand-name")
                model = title.find_all('span', class_="model")
                featuredictionary['name'] = title_text
                if brand:
                    featuredictionary['brand'] = brand[0].text.strip()
                if model:
                    featuredictionary['model'] = model[0].text.strip()
            extract_product_details(div, featuredictionary)
            extract_seller_details(div, featuredictionary)
            extract_images(div, featuredictionary)
        extract_features(soup, featuredictionary)
        json_data = json.dumps(featuredictionary, indent=2)
        return json_data
    else:
        print("Failed to fetch the webpage")



#amazonscraper
def amazon_scraper(url):
    response = requests.get(url,headers=headers)
    if response.status_code==200:
        soup=BeautifulSoup(response.text,'html.parser')
        #print(soup.prettify())
        d={}
        title= soup.body.find_all('span', id='productTitle')
        d['title']=(title[0].text.strip())
        price = soup.body.find_all('span', class_='a-price')
        d['price']=(price[0].find('span',class_='a-offscreen').text.strip())
        div=soup.body.find_all('div',id='prodDetails')
        dep=div[0].find_all('tr')

        for i in dep:
            d[i.find('th').text.strip().replace(' ','_').replace('&','_').replace(':','_').replace('.','_').replace('±','_').replace('#','_').replace('@','_').replace('-','_').replace('+','_').replace('/','_').replace('(','_').replace(')','_')]=i.find('td').text.strip().replace('\n',' ')
        #print(d)
        json_data = json.dumps(d,indent=2)
        return json_data
        
    else:
        print("Failed to fetch the webpage")
        
#flipkartscraper
# Modify flipkart_scraper function
def flipkart_scraper(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        d = {}
        title = soup.body.find_all('span', class_='B_NuCI')
        d['title'] = (title[0].text.strip())
        price = soup.body.find_all('div', class_='_30jeq3 _16Jk6d')
        d['price'] = (price[0].text.strip())
        div = soup.body.find_all('div', class_='_1UhVsV')

        dep = div[0].find_all('tr')

        for i in dep:
            d[i.find_all('td')[0].text.strip().replace('&', '_').replace(':', '_').replace(' ', '_').replace('.',
                                                                                                             '_').replace(
                '±', '_').replace('#', '_').replace('@', '_').replace('-', '_').replace('+', '_').replace('/',
                                                                                                           '_').replace(
                '(', '_').replace(')', '_')] = i.find_all('td')[1].text.strip().replace('\n', ' ')
        return d
    else:
        print("Failed to fetch the webpage")
        


    
@app.route('/array', methods=['POST'])
def run_script():
    data = request.get_json()  
    ls = data['array'] 
    url1 = ls[0]
    url2 = ls[1]
    url3 = ls[2]
    url4 = ls[3]
    data={}
    if url1:
        data["GEM"] = json.loads(gem_scraper(url1))
    # if url2:
    #     data["AMAZON"] = (amazon_scraper(url2))
    # if url4:
    
    data["Seller_type"]=json.loads(des(url4))
    if url3:
        data["FLIPKART"] = (flipkart_scraper(url3))
    
    
    if data:
        return json.dumps(data)
    
    return "No JSON data available."

if __name__ == '__main__':
    app.run(port='6500') 
