import requests
from bs4 import BeautifulSoup
import csv
from flask import Flask, request
import json
import pandas as pd

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

@app.route('/selller', methods=['POST'])
def run_script():
    try:
        data = request.get_json()
        ls = data['array']
        url = ls[0]
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
    
            table = soup.body.find_all('div', id="sellers-table-wrap")
    
            heading = table[0].find_all('th')
            header = [h.text.strip() for h in heading]
    
            tb = table[0].find_all('tbody')
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
                csv_writer.writerow(header)  # Write header row
    
                for i in range(0, len(n)):
                    if q[i].text == "\n":
                        q_value = "N/A"
                    else:
                        q_value = q[i].text.strip()
    
                    data = [
                        n[i].text.strip().replace('\n', ' '),
                        p[i].text.strip()[1:],
                        d[i].text.strip(),
                        q_value,
                        qa[i].text.strip(),
                        minq[i].text.strip(),
                        ofp[i].text.strip(),
                        ori[i].text.strip()
                    ]
                    csv_writer.writerow(data)
                    data1.append(data)
    
            # Move the reading part outside the with block
            excel_file = 'seller_data.xlsx'
            df = pd.read_csv("seller_data.csv")
    
            # Convert 'price' column to numeric for sorting
           # ...
    # Convert 'Offer Price' column to numeric for sorting
            for i in range (0,len(df['Offer Price'])):
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
            
            result = {
                "First_Reseller": reseller_row,
                "First_OEM": oem_row
            }
    
            return result
        else:
            return "ERROR"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(port=6000)