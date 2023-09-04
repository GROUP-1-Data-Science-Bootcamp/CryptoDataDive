import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

top200_path = os.path.join(".", "top200.csv")
df = pd.read_csv(top200_path)

links_to_download = df["historicallink"].tolist()


def download_csv(driver, url):
    driver.get(url)
    time.sleep(2)
    date_range_div = driver.find_element(
        By.CLASS_NAME,
        "sc-16891c57-0.dalfmx.BaseButton_base__aMbeB.BaseButton_v-primary__zw8Vo.BaseButton_t-default__fZuC3.BaseButton_size-md__jbSJR.BaseButton_vd__2Cn0v")
    date_range_div.click()
    time.sleep(4)
    last_365_days_li = driver.find_element(
        By.CSS_SELECTOR, "li:nth-child(5)")
    last_365_days_li.click()
    time.sleep(2)

    continue_button = driver.find_elements(By.CLASS_NAME, "bcCCXI")[1]
    continue_button.click()
    time.sleep(7)

    download_button = driver.find_element(
        By.CLASS_NAME, "BaseButton_vd__2Cn0v+.BaseButton_size-md__jbSJR")
    download_button.click()
    time.sleep(2)


driver = webdriver.Firefox()
driver.maximize_window()

while links_to_download:
    link = links_to_download[0]
    try:
        download_csv(driver, link)
        print(f"Downloaded: {link}")
        links_to_download.pop(0)
        print(f"Remaining Links: {len(links_to_download)}")
    except Exception as e:
        print(f"Error downloading {link}: {e}")
        print("Retrying...")
        time.sleep(5)

    if len(links_to_download) == 0:
        print("Downloaded all files. Stopping.")
        break

driver.quit()
