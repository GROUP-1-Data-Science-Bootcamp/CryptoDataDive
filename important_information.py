import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

top200_path = os.path.join(".", "top200.csv")
df = pd.read_csv(top200_path)
links_to_scrap = df["mainlink"].to_list()
results_df = pd.DataFrame(columns=["symbol", "github", "tags"])


def get_info(driver, link):
    driver.get(link)

    symbol = driver.find_element(By.CLASS_NAME, "cjeUNx").text

    about_button = driver.find_element(By.XPATH,
                                       "//span[@class='sc-16891c57-0 dlPAsd base-text' and contains(text(), 'About')]")
    about_button.click()
    time.sleep(0.5)

    href = "unknown"
    try:
        github_link = driver.find_element(By.XPATH, "//a[contains(text(), 'GitHub')]")
        href = github_link.get_attribute("href")
    except:
        pass

    tags = driver.find_elements(By.CSS_SELECTOR, "#section-coin-about .cmc-link")
    tags_name = [tag.text for tag in tags]

    return symbol, href, tags_name


driver = webdriver.Firefox()

while links_to_scrap:
    link = links_to_scrap[0]
    try:
        symbol, github, tags = get_info(driver, link)
        print(f"Downloaded: {symbol} info")

        row_symbol = symbol if symbol else "unknown"
        new_row = pd.DataFrame({
            "symbol": [row_symbol],
            "github": [github],
            "tags": [", ".join(tags)]
        })
        results_df = pd.concat([results_df, new_row], ignore_index=True)
        links_to_scrap.pop(0)
        print(f"Remaining Links: {len(links_to_scrap)}")
    except Exception as e:
        print(f"Error downloading {link}: {e}")
        print(f"Retrying ...")
        time.sleep(5)

    if len(links_to_scrap) == 0:
        print("Downloaded all files. Stopping.")
        break

driver.quit()
results_df.to_csv("important-information.csv", index=False)
