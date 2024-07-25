from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from .randomIP import RandomIPServer

# Initialize the Chrome browser

def fetchAmazon(product_name, browser):
    try:
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
        return products[0:5]
    except Exception as e:
        print(f"An error occurred while fetching Amazon products: {e}")
        return []

def fetchFlipkart(product_name, browser):
    try:
        browser.get(f'https://www.flipkart.com/search?q={product_name}')
        time.sleep(5)
        page_source = browser.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        products = []

        product_titles = soup.find_all('div', class_='KzDlHZ')
        for title in product_titles:
            product_details = {}
            product_details["Title"] = title.text
            products.append(product_details)
        if len(products) == 0:
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
                products[i]["URL"] = "https://flipkart.com" + url['href']
                
        for i in range(len(products)):
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
        return products[0:5]
    except Exception as e:
        print(f"An error occurred while fetching Flipkart products: {e}")
        return []

def fetch_products(product_name):
    try:
        PROXY = RandomIPServer()
        options = Options()
        options.add_argument(f'--proxy-server={PROXY}')
        browser = webdriver.Chrome(options=options)
        products = []
        products.extend(fetchAmazon(product_name, browser))
        products.extend(fetchFlipkart(product_name, browser))
        browser.quit()
        return products
    except Exception as e:
        print(f"An error occurred while fetching products: {e}")
        return []

# print(fetch_products("laptop"))
