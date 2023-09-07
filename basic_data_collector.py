import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

top200_path = os.path.join(".", "top200.csv")
df = pd.read_csv(top200_path)
links_to_scrap = df["mainlink"].to_list()
results_df = pd.DataFrame(columns=["symbol", "github", "langs", "contributors", "tags"])


def get_info(driver, link):
    driver.get(link)
    time.sleep(10)

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


def get_github_info_languages(driver, link):
    driver.get(link)
    used_languages_box = driver.find_elements(By.XPATH, "//ul[@class='list-style-none']")[1]
    used_languages = used_languages_box.find_elements(By.XPATH, ".//span[@class='color-fg-default text-bold mr-1']")

    used_languages_names = list()
    for language in used_languages:
        language_name = language.get_attribute("innerHTML")
        if language_name != "Other":
            used_languages_names.append(language_name)
    return used_languages_names


def get_github_info_contributors(driver, link):
    driver.get(link)
    time.sleep(5)
    contributors_full_list = driver.find_element(By.XPATH,
                                                 "//ol[@class='contrib-data list-style-none']")
    contributors_list = (contributors_full_list.find_elements(By.XPATH,
                                                              ".//li[@class='contrib-person float-left col-6 my-2 pl-2']") +
                         contributors_full_list.find_elements(By.XPATH,
                                                              ".//li[@class='contrib-person float-left col-6 my-2 pr-2']"))

    contributor_link_list = list()
    for contributor in contributors_list:
        contributor_link = ((contributor.find_element(By.XPATH, ".//span[@class='d-block Box']").
                             find_element(By.XPATH, ".//h3[@class='border-bottom p-2 lh-condensed']")).
                            find_element(By.XPATH, ".//a[@class='text-normal']").
                            get_attribute("href"))
        contributor_link_list.append(contributor_link)

    return contributor_link_list


driver = webdriver.Firefox()
driver.minimize_window()

while links_to_scrap:
    link = links_to_scrap[0]
    try:
        symbol, github, tags = get_info(driver, link)
        print(f"Downloaded: {symbol} info")

        langs = get_github_info_languages(driver, github)

        contributors = get_github_info_contributors(driver, github + "/graphs/contributors")
        print(contributors)

        print(f"Downloaded: {symbol} github info")

        row_symbol = symbol if symbol else "unknown"
        new_row = pd.DataFrame({
            "symbol": [row_symbol],
            "github": [github],
            "langs": [", ".join(langs)],
            "contrributors": [", ".join(contributors)],
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

#%%