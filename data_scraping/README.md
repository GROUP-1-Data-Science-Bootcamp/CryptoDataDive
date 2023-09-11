# Data Scraping
First step!
### scraping_mainpage.py
The code is a Python script that uses the Selenium WebDriver library to scrape cryptocurrency data (rank, name, symbol, mainlink and historicallink) from the webpage "https://coinmarketcap.com/historical/20230825/" and save it as a CSV file named "top200.csv" using the pandas library. 
### scraping_csv.py
The code automates the download of CSV files from a list of URLs using the Selenium library. It reads the "top200.csv" file and extracts the URLs from the "historicallink" column. The code then navigates to each URL, perform necessary actions, and download the corresponding CSV file for each cryptocurrency.
