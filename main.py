from selenium import webdriver
from selenium.common import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from bs4 import BeautifulSoup
import requests

GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLScFg0dYkr2cZ1xDRm6iVdup856tH8AZmcmDzaBkCtfLW5wa6A/viewform?usp=dialog"
ZILLOW_LINK = "https://appbrewery.github.io/Zillow-Clone"

response = requests.get(ZILLOW_LINK)
zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page,"html.parser")

listing_links = soup.find_all(name="a",class_="property-card-link")
listing_link_list = []
for link in listing_links:
    # print(link.get("href"))
    listing_link_list.append(link.get("href"))

prices = soup.find_all(name="span",class_="PropertyCardWrapper__StyledPriceLine")
prices_list = []
for price in prices:
    price_text = price.getText()
    cleaned_price = price_text.replace(',', '').replace('+', '').replace('/mo', '').split()[0]
    prices_list.append(cleaned_price)


addresses = soup.find_all(name="address")
address_list = []
for address in addresses:
    cleaned_address_text = " ".join(address.getText().replace("|","").strip().split())
    address_list.append(cleaned_address_text)

print(listing_link_list)
print(prices_list)
print(address_list)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(chrome_options)
driver.get(GOOGLE_FORM_LINK)


for i in range(len(listing_link_list)):
    address_input = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(address_list[i])

    price_input = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(prices_list[i])

    link_input = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(listing_link_list[i])

    submit_button = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    # time.sleep(1)

    next_answer = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_answer.click()
    # time.sleep(1)




