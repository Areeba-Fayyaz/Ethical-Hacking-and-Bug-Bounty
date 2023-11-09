
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

while True:
    def five_seconds():
        time.sleep(5)
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.get('https://pk.khaadi.com/fabrics/2-piece-fabrics/embroidered-top-bottoms/')

        # Find the element with the class 'product-title'
        product_title_element = driver.find_element(By.CLASS_NAME, 'product-tile')

        # Navigate to the nested div with class 'price'
        price_element = product_title_element.find_element(By.CLASS_NAME, 'price')

        # Get and print the text content of the price element
        price_text = price_element.text
        print(price_text)
    five_seconds()
# driver.close() 
# while(True):
#     pass