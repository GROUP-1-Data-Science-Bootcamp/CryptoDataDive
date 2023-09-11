from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Firefox()
driver.get("https://coinmarketcap.com/historical/20230825/")
driver.maximize_window()

collected_currencies = []
total_height = int(driver.execute_script("return document.body.scrollHeight"))

for i in range(1, total_height, 800):
    driver.execute_script(f"window.scrollTo(0, {i});")

main_element = driver.find_elements(
    By.CLASS_NAME, "cmc-table__column-name--name")

symbol = driver.find_elements(
    By.CLASS_NAME, "cmc-table__cell--sort-by__symbol div")

if main_element:
    for index, element in enumerate(main_element):
        cryptocurrencies = dict()
        cryptocurrencies["rank"] = index + 1
        cryptocurrencies["name"] = element.text
        cryptocurrencies["symbol"] = symbol[index].text
        cryptocurrencies["mainlink"] = element.get_attribute("href")
        cryptocurrencies["historicallink"] = (
                element.get_attribute("href") + "historical-data/"
        )
        collected_currencies.append(cryptocurrencies)
else:
    print("No name links found")

driver.quit()

df = pd.DataFrame(collected_currencies)
df.to_csv("top200.csv", index=False)
