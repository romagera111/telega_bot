import datetime
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By

class Parser:

    def __init__(self):
        self.urls = ['https://www.avito.ru/moskva/avtomobili/vaz_lada-ASgBAgICAUTgtg3GmSg?cd=1&f=ASgBAQECAkTyCrCKAeC2DcaZKAFA4rYNNMyaKMaaKMKaKAJFxpoMGnsiZnJvbSI6NjAwMDAsInRvIjoxNzAwMDB9~owUF3siZnJvbSI6MTk3MCwidG8iOjIwMDB9&radius=500&s=104&searchRadius=500',
                     'https://www.avito.ru/staryy_oskol/avtomobili/vaz_lada-ASgBAgICAUTgtg3GmSg?cd=1&f=ASgBAQECAUTgtg3GmSgBQOK2DUTEmijCmijGmijMmigCRcaaDBp7ImZyb20iOjUwMDAwLCJ0byI6MjAwMDAwffqMFBd7ImZyb20iOjE5NzAsInRvIjoxOTk5fQ&radius=200&searchRadius=200']
    
    def parse(self):

        links_total = list()

        for url in self.urls:

            driver = webdriver.Firefox()

            driver.get(url)

            links = driver.find_elements(By.XPATH, "//a[@itemprop='url' and contains(@class, 'styles-module-root-iSkj3') and not(@rel='noopener noreferrer')]")

            cars = [link.get_attribute("href") for link in links]

            links_total += cars

            driver.close()

        connection = sqlite3.connect('cars.db')
        cursor = connection.cursor()

        links_not_in_pool = list()

        for link in links_total:
            cursor.execute("SELECT 1 FROM main_table WHERE link = ?", (link,))

            if not cursor.fetchone():
                links_not_in_pool.append(link)
                time_str = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                cursor.execute("INSERT INTO main_table VALUES (?,?)", (link, time_str))
                connection.commit()
        
        connection.close()

        if links_not_in_pool:
            return links_not_in_pool
        
        return []