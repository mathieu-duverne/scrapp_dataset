from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import csv
import re

def remove_escape_and_comma(string):
  """Removes all escape and commas from a string.

  Args:
    string: The string to remove the escape and commas from.

  Returns:
    A string without the escape and commas.
  """

  pattern = re.compile(r"([\\,\n])")
  return pattern.sub("", string)

def read_csv(filename):
  """Reads and extracts data from a CSV file.

  Args:
    filename: The path to the CSV file.

  Returns:
    A list of lists, where each inner list contains the data from a single row of the CSV file.
  """

  with open(filename, "r", encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    data = []
    for row in reader:
      print(row[3])
      data.append(row[3])

  return data


def split_string(string):
  """Splits the string and returns the last string after the last "/"."""
  parts = string.split("/")
  last_part = parts[-1]
  return last_part


def append_value_to_dataframe(dataframe, title, about, usuability, href):
  """Appends a value to the DataFrame."""
  new_data = pd.DataFrame({"Title": [title], "About": [about], "Usuability": [usuability], "Link" : [href]})
  dataframe = pd.concat([dataframe, new_data], ignore_index=True)
  return dataframe


def scrapp_kaggle_datasets(url, data):
  """Scrapp specific datasets from the Kaggle website."""

  driver.get(url)
  
  # this is just to ensure that the page is loaded -- For dynamic web page -- 
  time.sleep(3) 
  
  html = driver.page_source
  
  # --- BeautifulSoup --- #
  soup = BeautifulSoup(html, "html.parser")
  ul_datasets_per_page = soup.find("ul", class_="km-list--three-line")
  # --- BeautifulSoup --- #

  count=0
  urls_usuability = [] 

  # --- BeautifulSoup : Iteration on all intersting li --- #
  for row in ul_datasets_per_page.find_all("li", class_="sc-jFJHMl eIZuMY"):

    # get a link
    href = row.a["href"]
    url = "https://www.kaggle.com" + row.a["href"]
    
    # if my csv file contains this link let's see other link
    if url in data:
      continue

    driver.get(url)
    
    # this is just to ensure that the page is loaded -- For dynamic web page -- 
    time.sleep(3) 
    
    html = driver.page_source
    dataframe = pd.DataFrame(columns=["Title", "About", "Usuability", "Link"])
    
    soup = BeautifulSoup(html, "html.parser")
    
    # Find specific div with attribute 
    about_dataset = soup.find("div", attrs = {'style':'min-height: 80px;'})
    about = ""
    for p in about_dataset.find_all("p"):
      about += p.text
    
    good_about = remove_escape_and_comma(about)
    
    # Find specific p with attribute 
    usuability = soup.find("p", attrs= {'style':'margin-top: 4px;'}).span.text

    title = split_string(href)
   
    urls_usuability.append((url, usuability))
    dataframe = append_value_to_dataframe(dataframe, title, good_about, usuability, url)
    
    # write data in csv file 
    dataframe.to_csv('kaggle_dataset.csv', mode='a', index=False, header=False)
    count += 1
  
  if count == 0 : data_to_send = "No dataset added"
  else:
    data_to_send = "Here is the number of datasets added to your data : " + str(count) + "\n" + "Below are the titles of the datasets added during the last run : \n "
    
    for url, usuability in urls_usuability:
        data_to_send += url + " : " + usuability
    
    d = data_to_send.encode(encoding = 'UTF-8')
    
    # To send a notification on my mobile  
    requests.post('https://notify.run/bVZoarEcz4hgatgCFl5p', data=d)
  


if __name__ == "__main__":
  
#   ------- Selenium for dynamic web app ------- # 
  driver_location = "chromedriver"
  binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome"
  
  option = webdriver.ChromeOptions()
  option.binary_location = binary_location
  driver = webdriver.Chrome(executable_path=driver_location) 
#   ------- Selenium for dynamic web app ------- # 
  
  # We don't want duplicates
  data = read_csv("kaggle_dataset.csv")
  
  # topic trendingDataset 
  url = "https://www.kaggle.com/datasets?topic=trendingDataset"
  
  scrapp_kaggle_datasets(url, data)
