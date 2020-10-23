import numpy as np
import pandas as pd
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as Soup
from datetime import datetime


warnings.filterwarnings('ignore')
current_month = int(datetime.now().month)
current_year = int(datetime.now().year)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

data = []
for i in range(current_year, 1929, -1):
    for j in range(1, 13):
        if i == current_year and j>current_month:
            continue
        else:
            url = f'https://www.wunderground.com/history/monthly/mk/ilinden/LWSK/date/{i}-{j}'
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(10)
            driver.get(url)
            try:
                extracted_dates = driver.find_element_by_css_selector('#inner-content > div.region-content-main > div.row > div:nth-child(5) > div:nth-child(1) > div > lib-city-history-observation > div > div.observation-table.ng-star-inserted > table > tbody > tr > td:nth-child(1) > table')
                extracted_temperatures = driver.find_element_by_css_selector('#inner-content > div.region-content-main > div.row > div:nth-child(5) > div:nth-child(1) > div > lib-city-history-observation > div > div.observation-table.ng-star-inserted > table > tbody > tr > td:nth-child(2) > table')
                extracted_dew_points = driver.find_element_by_css_selector('#inner-content > div.region-content-main > div.row > div:nth-child(5) > div:nth-child(1) > div > lib-city-history-observation > div > div.observation-table.ng-star-inserted > table > tbody > tr > td:nth-child(3) > table')
                extracted_humidity = driver.find_element_by_css_selector('#inner-content > div.region-content-main > div.row > div:nth-child(5) > div:nth-child(1) > div > lib-city-history-observation > div > div.observation-table.ng-star-inserted > table > tbody > tr > td:nth-child(4) > table')
                extracted_wind_speed = driver.find_element_by_css_selector('#inner-content > div.region-content-main > div.row > div:nth-child(5) > div:nth-child(1) > div > lib-city-history-observation > div > div.observation-table.ng-star-inserted > table > tbody > tr > td:nth-child(5) > table')
                extracted_pressure = driver.find_element_by_css_selector('#inner-content > div.region-content-main > div.row > div:nth-child(5) > div:nth-child(1) > div > lib-city-history-observation > div > div.observation-table.ng-star-inserted > table > tbody > tr > td:nth-child(6) > table')
                dates = [str(d) + str(j) + str(i) for d in extracted_dates.text.split('\n')]
                temperatures = list(extracted_temperatures.text.split('\n'))
                dew_points = list(extracted_dew_points.text.split('\n'))
                humidity = list(extracted_humidity.text.split('\n'))
                wind_speed = list(extracted_wind_speed.text.split('\n'))
                pressure = list(extracted_pressure.text.split('\n'))
                for k in range(1, len(dates)):
                    data.append([int(dates[k]), temperatures[k], dew_points[k], humidity[k], wind_speed[k], pressure[k]])

                print(f'Finished month {j} year {i}')
            
            except:
                print(f'Couldn\'t locate object year {i} month {j}')
                    
            finally:
                driver.quit()
                df = pd.DataFrame(np.array(data), columns = ['Date', 'Temperatures', 'Dew-Points', 'Humidity', 'Wind-Speed', 'Pressure'])        
                df.to_csv('weather_forecast_data_Skopje')       
