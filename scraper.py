from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import re
import numpy as np
import config

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--lang=en-US')
options.binary_location = config.CHROME_BINARY_LOCATION
options.chrome_driver_binary = config.CHROMEDRIVER_BINARY_LOCATION

driver = webdriver.Chrome(options=options)
busy_times = {'5': 0,
              '6': 0,
              '7': 0,
              '8': 0,
              '9': 0,
              '10': 0,
              '11': 0,
              '12': 0,
              '13': 0,
              '14': 0,
              '15': 0,
              '16': 0,
              '17': 0,
              '18': 0,
              '19': 0,
              '20': 0,
              '21': 0,
              '22': 0,
              '23': 0,
              '0': 0,
              '1': 0,
              '2': 0,
              '3': 0,
              '4': 0
              }


class Scrap():

    def __init__(self, url) -> None:
        self.url = url

    def get_page_source(self, class_name):
        '''
        class_name= HTML tags find with class name
        '''

        driver.get(self.url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        return driver.page_source

    def get_information(self, html_page):
        soup = BeautifulSoup(html_page, features='html.parser')
        information = soup.find_all('div', {'class': 'dpoVLd'})
        return information

    def normalize_dict_values(self, input_dict):
        # Extract values from the dictionary
        values = np.array(list(input_dict.values()))

        # Normalize the values between 0 and 1
        normalized_values = (values - np.min(values)) / \
            (np.max(values) - np.min(values))

        # Scale the normalized values to be between 0 and 100
        normalized_values_0_to_100 = normalized_values * 100

        # Create a new dictionary with the same keys and the normalized values
        normalized_dict = {key: value for key, value in zip(
            input_dict.keys(), normalized_values_0_to_100)}

        return normalized_dict

    def get_place_name(self, html_page):
        soup = BeautifulSoup(html_page, features='html.parser')
        place_name = soup.find('h1', {'class': 'DUwDvf lfPIob'})
        return place_name.text

    import re

    def parse_busy_string(self, data_label):
        # Regular expression to extract percentage and time
        pattern = re.compile(r'(\d+)% busy at (\d+)\s*([APMapm]{2})\.')

        match = pattern.match(data_label)

        if match:
            percentage = int(match.group(1))
            hour = int(match.group(2))
            period = match.group(3).upper()

            # Convert to 24-hour format
            if period == 'PM' and hour != 12:
                hour += 12
            elif period == 'AM' and hour == 12:
                hour = 0

            return percentage, hour
        else:
            return None

    def save_information(self, html_page):
        information = self.get_information(html_page)
        place_name = self.get_place_name(html_page)

        for info in information:
            data_label = info['aria-label']
            with open(f'{place_name}.txt', 'a') as textfile:
                textfile.writelines(data_label+'\n')
        print(f'{place_name}.txt is created successfully !')

    def save_plot(self, html_page):
        information = self.get_information(html_page)
        for info in information:
            data_label = info['aria-label']
            percent, hour_24_format = self.parse_busy_string(data_label)
            key_busy_times = str(hour_24_format)
            busy_times[key_busy_times] += int(percent)

        normal_busy_times = self.normalize_dict_values(busy_times)

        hours = normal_busy_times.keys()
        values = normal_busy_times.values()
        place_name = self.get_place_name(html_page)
        print(values)
        plt.bar(hours, values)
        plt.xlabel('Hours')
        plt.ylabel('A week')
        plt.title(f'plotted popular times of {place_name}')
        plt.savefig(f'{place_name}.png')
        plt.show()
        plt.close()

    def run(self):
        html = self.get_page_source('UmE4Qe')
        self.save_information(html_page=html)
        self.save_plot(html)
        return True
