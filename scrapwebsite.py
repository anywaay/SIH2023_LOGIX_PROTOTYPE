pip install Workbook
import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from bs4 import BeautifulSoup


def pagescrap(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return soup
    else:
        print("Failed to fetch the webpage")
def getinfoofpage(soup,output,search):
    np=''
    nextpage=soup.body.find_all('div',class_='pagination')
    variant_desc_divs = soup.body.find_all('div', class_='variant-wrapper')
    for div  in nextpage:
        link = div.find_all('a', attrs={'rel': 'next'})
        for li in link:
            href=li.get('href')
            print("https://mkp.gem.gov.in"+href)
            np="https://mkp.gem.gov.in"+href
            break
    for div in variant_desc_divs:
        k = [search]
        #title
        variant_titles = div.find_all('span', class_='variant-title')
        k.append(variant_titles[0].text.strip())
        #reseller or oem
        typeofseller=div.find_all('span',class_='sold_as_summary')
        k.append(typeofseller[0].text.strip())
        #link of next and sellers
        links=div.find_all('a')
        #rating
        rating=div.find_all('span',class_='badge')
        #money
        price=div.find_all('span',class_='m-w')
        k.append(price[0].text.strip())
        #brand
        brand=div.find_all('div',class_='variant-brand')
        #quantity
        quantity=div.find_all('div',class_='variant-moq')
        k.append(quantity[0].text.strip())
        #image
        image= div.find_all('span', {'data-src': True})
        if variant_titles:
            k.append(brand[0].text.strip())
            if rating:
                k.append(rating[0].text.strip())
            else:
                k.append('0')
            for l in image:
                h = l.get('data-src')
                k.append(h)
                print(h)
            if rating:
                print(rating[0].text)
            else:
                print(0)
            for link in links:
                href = link.get('href')
                if href:
                    k.append("https://mkp.gem.gov.in"+href)
        output.append(k)
    if np:
        return np
def storeinxl2():
    w=Workbook()
    sheet=w.add_sheet('data')
    for item in range(0,len(output)):
        li=output[item]
        for p in range(0,len(li)):
            sheet.write(item+1,item,li[p])
    w.save('datascrap.xls')
def storeinxl(output):
    w = Workbook()
    sheet = w.add_sheet('data')

    # Loop through the data and write it to the Excel sheet
    for row_index, row_data in enumerate(output, start=1):
        for col_index, value in enumerate(row_data):
            sheet.write(row_index, col_index, value)
            print (value)

    w.save('datascrap.xls')
if __name__ == '__main__':
    dic={
     "Desktop Computers":"computers-desktop-computer",
     "Laptop Notebooks":"computers-0806nb",
     "Computer Printers":"computer-printer-0901print",
     "Tablet Computers":"computers-0912tc",
     "Buses":"buses",
     "Tractors":"tractors",
     "Cars":"25101500-cars-version-2-",
     "Utility Vehicles":"25101500-utility-vehicles-version-2-",
     "Class Room Desking":"general-classroom-furnishing-class-room-desking-and-seating91",
     "Executive Table":"-furniture-and-furnishings-accommodation-furnitureold-freestanding-furniture-executive-table-version-2-",
     "Revolving Chair":"-furniture-and-furnishingsold-accommodation-furniture-office-furniture-revolving-chair-version-2-",
     "Movable File Storage System":"movable-file-storage-system",
     "Alcohol Based Hand Sanitizer":"drugs-and-pharmaceutical-products-anti-infective-drugsold-antiseptics-alcohol-based-hand-rub-hand-sanitizer",
     "Surgical Gloves as per IS 4148":"surgical-gloves",
     "Disposable Syringes as per IS 10258":"syringes-and-accessories-disposable-syringes52",
     "Diaries Printed Plain Register":"diaries-printed-plain--register-",
     "Gel Pen":"drawing-tools-and-supplies-and-accessories-gel-pen-rev-",
     "Maplitho Paper":"maplitho-paper",
     "Led Luminaire":"exterior-lighting-fixtures-and-accessories-led-luminaire-for-road-and-street-lights-",
     "Molded Case Circuit Breakers (MCCB)":"circuit-protection-devices-and-accessories-molded-case-circuit-breakers-mccb-",
     "Telecommunication Cable":"telecommunication-cable",
     "Television TV":"domestic-appliances-and-supplies-and-consumer-electronic-products-consumer-electronics-audio-and-visual-equipmentold-28051-tv",
     "Domestic Refrigerators":"domestic-refrigerators",
     "Handloom Cotton Bed Sheets":"bedclothes-handloom-cotton-bed-sheets-as-per-is-745-version-2-",
     "Cotton Towels as per IS 7056":"cotton-towels",
     "Steel Tubes, Tubulars And Fittings":"commercial-pipe-and-piping-steel-pipes-fitting",
     "Commercial CPCV Pipe Fittings":"commercial-pipe-and-piping-commercial-cpvc-pipe-fittings"
    }
    output=[]
    for search in dic:
        url="https://mkp.gem.gov.in/"+dic[search]+"/search?"
      
        soup=pagescrap(u)
        while url:
            soup = pagescrap(url)
            if soup:
                url = getinfoofpage(soup, output, search)
            else:
                break

    print(output)    
    storeinxl(output)
