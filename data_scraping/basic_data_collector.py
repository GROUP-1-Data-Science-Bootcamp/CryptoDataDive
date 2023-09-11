import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

top200_path = os.path.join(".", "data_collections/top200.csv")
df = pd.read_csv(top200_path)
links_to_scrap = df["mainlink"].to_list()
results_df = pd.DataFrame(columns=["symbol", "github", "langs", "contributors", "tags"])


def get_info(driver, link):
    driver.get(link)
    time.sleep(5)

    symbol = driver.find_element(By.CLASS_NAME, "cjeUNx").text

    tags = list()
    try:
        tags_show_all_button = driver.find_element(
            By.XPATH,
            "//span[@class='sc-16891c57-0 sc-9ee74f67-1 ixMiII' and contains(text(), 'Show all')]",
        )
        tags_show_all_button.click()

        tags_categories = driver.find_element(
            By.XPATH, "//div[@class='sc-16891c57-0 ddQhJW']"
        )
        tags_categories = tags_categories.find_elements(
            By.XPATH, ".//div[@class='sc-16891c57-0 gPFIPZ']"
        )

        for tag_category in tags_categories:
            category_tags = tag_category.find_element(By.XPATH, ".//div")
            found_tags = category_tags.find_elements(
                By.XPATH, ".//span[@class='sc-16891c57-0 sc-9ee74f67-1 dWtIZr']"
            )
            for tag in found_tags:
                tags.append(tag.text)
    except:
        tags_elements = driver.find_elements(
            By.CSS_SELECTOR, "#section-coin-about .cmc-link"
        )
        tags = [tag.text for tag in tags_elements]

    href = "unknown"
    try:
        github_link = driver.find_element(By.XPATH, "//a[contains(text(), 'GitHub')]")
        href = github_link.get_attribute("href")
    except:
        pass

    return symbol, href, tags


def get_github_info_languages(driver, link):
    github_repository_pattern = r"^https?://github\.com/[\w\-]+/[\w\-]+$"
    if re.match(github_repository_pattern, link) is None:
        return []
    used_languages_names = list()
    try:
        driver.get(link)
        time.sleep(10)
        used_languages_box = driver.find_elements(
            By.XPATH, "//ul[@class='list-style-none']"
        )[1]
        used_languages = used_languages_box.find_elements(
            By.XPATH, ".//span[@class='color-fg-default text-bold mr-1']"
        )

        for language in used_languages:
            language_name = language.get_attribute("innerHTML")
            if language_name != "Other":
                used_languages_names.append(language_name)
    except:
        pass
    return used_languages_names


def get_github_info_contributors(driver, link):
    github_repository_pattern = r"^https?://github\.com/[\w\-]+/[\w\-]+/graphs/contributors"
    if re.match(github_repository_pattern, link) is None:
        return []
    contributor_link_list = list()
    try:
        driver.get(link)
        time.sleep(10)
        contributors_full_list = driver.find_element(
            By.XPATH, "//ol[@class='contrib-data list-style-none']"
        )
        contributors_list = contributors_full_list.find_elements(
            By.XPATH, ".//li[@class='contrib-person float-left col-6 my-2 pl-2']"
        ) + contributors_full_list.find_elements(
            By.XPATH, ".//li[@class='contrib-person float-left col-6 my-2 pr-2']"
        )

        for contributor in contributors_list:
            contributor_link = (
                (
                    contributor.find_element(
                        By.XPATH, ".//span[@class='d-block Box']"
                    ).find_element(
                        By.XPATH, ".//h3[@class='border-bottom p-2 lh-condensed']"
                    )
                )
                .find_element(By.XPATH, ".//a[@class='text-normal']")
                .get_attribute("href")
            )
            contributor_link_list.append(contributor_link)
    except:
        pass

    return contributor_link_list


driver = webdriver.Firefox()
driver.minimize_window()

while links_to_scrap:
    link = links_to_scrap[0]
    try:
        symbol, github, tags = get_info(driver, link)
        print(f"Downloaded: {symbol} info")

        langs = list()
        contributors = list()
        if github != "unknown":
            langs = get_github_info_languages(driver, github)
            contributors = get_github_info_contributors(
                driver, github + "/graphs/contributors"
            )

        print(f"Downloaded: {symbol} github info")

        row_symbol = symbol if symbol else "unknown"
        new_row = pd.DataFrame(
            {
                "symbol": [row_symbol],
                "github": [github],
                "langs": [", ".join(langs)],
                "contributors": [", ".join(contributors)],
                "tags": [", ".join(tags)],
            }
        )
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
results_df.to_csv("data_collections/important-information.csv", index=False)

#%%
