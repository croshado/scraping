from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
import csv
# Provide the URL of the Amazon product page
dict={'title':[],'price in ₹':[],'rating':[],'manufacturer':[],'ASIN':[],'description':[]}
global soup,driver,links
def scrap(i):
    global soup,driver,links
    url = f"https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1692713312&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    path="C://Program Files//Google//Chrome//Application//chromedriver.exe"
# Initialize the Selenium webdriver
    service = Service(executable_path=path)

    driver = webdriver.Chrome(service=service)
    driver.get(url)
# Provide the path to chromedriver.exe
    pagesource=driver.page_source

    soup=BeautifulSoup(pagesource,'html.parser')
    links=soup.find_all('a',attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    scrap2()
def scrap2():
   for t in range(len(links)):
        full=links[t].get('href')
        product='https://amazon.in'+full
        driver.get(product)
        pagesource1=driver.page_source
        soup1=BeautifulSoup(pagesource1,'html.parser')
        title=soup1.find('span',attrs={"id":'productTitle'}).text.strip()
        dict['title'].append(title)
        price=soup1.find('span',attrs={"class":'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span",attrs={"class":'a-offscreen'}).text.strip()
        price1=price.strip('₹')
        dict['price in ₹'].append(price1)
        Rating=soup1.find('span',attrs={"id":'acrCustomerReviewText'}).text
        dict['rating'].append(Rating)
        productdescription=soup1.find('div',attrs={"id":'productDescription'})
        so=soup1.find('ul',attrs={"class":'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'})
        if so != None:
          for i in so.find_all('li'):
               if(i.find('span').find('span').text.split()[0])=="Manufacturer":
                   manufacture=i.find('span').find('span').find_next('span').text.strip()
                   dict['manufacturer'].append(manufacture)
           
    
          for x in so.find_all('li'):
                if(x.find('span').find('span').text.split()[0])=="ASIN":
                  ASIN=x.find('span').find('span').find_next('span').text.strip()
                  dict['ASIN'].append(ASIN)
        if productdescription != None:
            try:
                description=soup1.find('div',attrs={"id":'productDescription'}).find("p").find('span').text.strip()
                dict['description'].append(description)
            except:
                description="no description"
                dict['description'].append(description)



name=input('enter file name -')
page=int(input("enter page -"))
a=1
for i in range(page):
    scrap(a)
    a=a+1

with open(f"E://{name}.csv",'w',encoding="utf-8") as outfile:
    writer=csv.writer(outfile)
    keylist=list(dict.keys())
    limit=len(keylist)
    writer.writerow(dict.keys())
    writer.writerows(zip(*dict.values()))

