from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Initialize the Chrome browser


def fetchAmazon(product_name,browser):
    browser.get(f'https://www.amazon.in/s?k={product_name}')
    time.sleep(5)
    page_source = browser.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    products = []

    product_titles = soup.find_all('span', class_='a-size-medium a-color-base a-text-normal')
    for title in product_titles:
        product_details = {}
        product_details["Title"] = title.text
        products.append(product_details)
    if len(products) == 0:
        return []
    
    product_prices = soup.find_all('span', class_='a-price-whole')
    for i, price in enumerate(product_prices):
        if i < len(products):
            products[i]["Price"] = price.text

    rating_tags = soup.find_all('span', class_='a-icon-alt')
    for i, rating in enumerate(rating_tags):
        if i < len(products):
            products[i]["Rating"] = rating.text.split()[0]

    image_tags = soup.find_all('img', class_='s-image')
    for i, image in enumerate(image_tags):
        if i < len(products):
            products[i]["Image"] = image['src']
            
    url_tags = soup.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    for i, url in enumerate(url_tags):
        if i < len(products):
            products[i]["URL"] = "https://amazon.in" + url['href']
            
    for i in range(len(products)):
        products[i]["Platform"] = "Amazon"
    # s-image->image class
    # a-size-medium a-color-base a-text-normal->title
    # a-icon-alt->rating
    # a-price-whole->price
    return products

def fetchFlipkart(product_name,browser):
    browser.get(f'https://www.flipkart.com/search?q={product_name}')
    time.sleep(5)
    page_source = browser.page_source

    browser.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    products = []

    product_titles = soup.find_all('div', class_='KzDlHZ')
    for title in product_titles:
        product_details = {}
        product_details["Title"] = title.text
        products.append(product_details)
    if(len(products)==0):
        return []
    product_prices = soup.find_all('div', class_='Nx9bqj _4b5DiR')
    for i, price in enumerate(product_prices):
        if i < len(products):
            products[i]["Price"] = price.text

    rating_tags = soup.find_all('div', class_='XQDdHH')
    for i, rating in enumerate(rating_tags):
        if i < len(products):
            products[i]["Rating"] = rating.text

    image_tags = soup.find_all('img', class_='DByuf4')
    for i, image in enumerate(image_tags):
        if i < len(products):
            products[i]["Image"] = image['src']
            
    url_tags = soup.find_all('a', class_='CGtC98')
    for i, url in enumerate(url_tags):
        if i < len(products):
            products[i]["URL"] = "https://flipkart.com"+url['href']
            
    for i in range(0,len(products)):
        products[i]["Platform"] = "FlipKart"

    # feature_tags = soup.find_all('ul', class_='G4BRas')
    # for i, feature in enumerate(feature_tags):
    #     if i < len(products):
    #         products[i]["Features"] = feature.text

    # for product in products:
    #     print(product["Title"])
    #     print(product["Price"])
    #     print(product["Rating"])
    #     print(product["Image"])
    #     print(product["URL"])
    #     print(product["Platform"])
    #     # print(product["Features"])
    #     print()
    #     print("\n\n")
    return products
    # KzDlHZ->title
    # Nx9bqj _4b5DiR->prices
    # XQDdHH->rating
    # <img loading="eager" class="DByuf4" alt="CHUWI Intel Celeron Dual Core 10th Gen N4020 - (4 GB/128 GB SSD/Windows 11 Home) HeroBook Air Laptop" src="https://rukminim2.flixcart.com/image/312/312/xif0q/computer/o/3/m/-original-imagtdqhggabrmft.jpeg?q=70">
    # <ul class="G4BRas"><li class="J+igdf">Fan-less Design
    # (Low Power Consumption)</li><li class="J+igdf">4x faster than eMMC</li><li class="J+igdf">M.2 port for easy DIY upgrades</li><li class="J+igdf">LPDDR4 4GB RAM</li><li class="J+igdf">Intel 9th generation UHD Graphics</li><li class="J+igdf">Support 4K/60 Frames HD</li><li class="J+igdf">Intel Celeron Dual Core Processor (10th Gen)</li><li class="J+igdf">4 GB LPDDR4 RAM</li><li class="J+igdf">64 bit Windows 11 Operating System</li><li class="J+igdf">128 GB SSD</li><li class="J+igdf">29.46 cm (11.6 inch) Display</li><li class="J+igdf">Operating System Software</li><li class="J+igdf">1 Year Onsite Warranty</li></ul>


def fetch_products(product_name):
    browser = webdriver.Chrome()
    products = []
    products.extend(fetchAmazon(product_name,browser))
    products.extend(fetchFlipkart(product_name,browser))
    browser.quit()
    return products

# print(fetch_products("laptop"))

# Close the browser after all operations are complete


