# Data Scraping
You should run the following files in order!
### scraping_mainpage.py
The code is a Python script that uses the Selenium WebDriver library to scrape cryptocurrency data (rank, name, symbol, mainlink and historicallink) from the webpage "https://coinmarketcap.com/historical/20230825/" and save it as a CSV file named "top200.csv" using the pandas library. 
### scraping_csv.py
The code automates the download of CSV files from a list of URLs using the Selenium library. It reads the "top200.csv" file and extracts the URLs from the "historicallink" column. The code then navigates to each URL, perform necessary actions, and download the corresponding CSV file for each cryptocurrency which is saved in CSVs folder.
### basic_data_collector.py
The code takes iterates over all rows in "top200.csv", navigates to the provided mainlink, and extracts the symbol, tags and GitHub link (if available) from the web page. If a valid GitHub link is available, it calls the helper functions to extract the programming languages and contributors for that repository. Finally, it saves the data into the "important-information.csv" file.
### data_preprocessor.py
The code reads data from the "top200.csv" file. Uses the values in the "name" column to find the associated csv file in the csvs folder and then cleans the data to be ready for injecting into the database. It then saves the cleaned data for each file in a separate CSV file with a specific naming convention in the cleaned_csvs folder.
