from selenium import webdriver
import logging
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import os
import shutil
import pandas as pd
import time
from geopy.geocoders import Nominatim
import requests
import urllib.parse
import re
from bs4 import BeautifulSoup
from itertools import product

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))



def appendProduct(file_path2, data):
    temp_file = 'temp_file.csv'

    # Read existing CSV or create an empty DataFrame
    if os.path.isfile(file_path2):
        df = pd.read_csv(file_path2, index_col='ASIN', encoding='utf-8')
    else:
        df = pd.DataFrame()

    # Update DataFrame with new data
    asin = data["ASIN"]
    state = data["State"]
    available_flag = data["Available"]

    # Check if ASIN already exists in the DataFrame
    if asin in df.index:
        # Update existing row
        df.loc[asin, state] = available_flag
    else:
        # Add new row
        df.loc[asin, state] = available_flag

    try:
        df.to_csv(temp_file, index=True, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred while saving the temporary file: {str(e)}")
        return False

    try:
        os.replace(temp_file, file_path2)
    except Exception as e:
        print(f"An error occurred while replacing the original file: {str(e)}")
        return False

    return True

driver.get("https://www.amazon.com/")
time.sleep(10)

file = open('zip_codes.txt')
zip_codes = [f.strip() for f in file.readlines()]

df = pd.read_excel('ASIN List.xlsx')
asins = df['ASIN'].values

for asin in asins:
    driver.get(f'https://www.amazon.com/dp/{asin}')
    time.sleep(2)
    for zip_code in zip_codes:
        state,zip_code = zip_code.split(',')
        location_button = driver.find_element(By.XPATH,"//a[@id='nav-global-location-popover-link']")
        location_button.click()
        time.sleep(2)
        
        location_input = driver.find_element(By.XPATH,"//input[@aria-label='or enter a US zip code']")
        location_input.send_keys(zip_code)
        time.sleep(1)

        location_apply = driver.find_element(By.XPATH,"//span[.='Apply']/parent::span/input")
        location_apply.click()
        time.sleep(2)

        try:
            additional_button = driver.find_element(By.XPATH,"//span[.='Continue']/parent::span/input")
            additional_button.click()
            time.sleep(4)
        except:
            try:  
                location_submit = driver.find_element(By.XPATH,"//button[.='Done']")
                location_submit.click()
                time.sleep(4)
            except:
                time.sleep(4)
                pass
        
        available_flag = "Yes"
        try:
            available = driver.find_element(By.XPATH,"//div[@id='mir-layout-DELIVERY_BLOCK']/div/span[@class='a-color-error']")
            available_flag = "No"
        except:
            available_flag = "Yes"
        
        data = {
            "ASIN": asin,
            "State": state,
            "Available": available_flag
        }

        print(data)
        appendProduct('output.csv',data)


        

        
