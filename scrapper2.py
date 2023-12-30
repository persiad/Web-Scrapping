# Web scrapper to extract data from finance.naver.com
# Instead of bs4, this project uses selenium

import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    browser = webdriver.Chrome()
    # browser.maximize_window()

    # 1. Move to the webpage
    url = "https://finance.naver.com/sise/sise_market_sum.naver?&page="
    browser.get(url)

    # 2. Choose the filters (up to 6 items)
    filters = browser.find_elements(By.NAME, "fieldIds")
    # when open the web, some items are checked by default
    # unclick all the boxes and let user choose which items to select
    for filter in filters:
        if filter.is_selected():
            filter.click()

    # 3. Choose the filers that you wish:
    items_to_select = ['거래량', '시가총액', 'PER', '영업이익증가율', 'ROE', '매출액증가율']
    for filter in filters:
        parent_element = filter.find_element(By.XPATH, "..")
        label = parent_element.find_element(By.TAG_NAME, 'label')
        # this is a slow operation: need to reduce it to a constant time
        if label.text in items_to_select:
            filter.click()

    # 4. hit apply
    btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
    btn_apply.click()

    # 5. Extract data (table)
    # each page has 3 tables, we need the second one (which includes the main data)
    for idx in range(1, 50):
        # we need to move to the next page
        browser.get(url + str(idx))

        df = pd.read_html(browser.page_source)[1]
        # break out of the for loop if table is empty <= meaning we've reached the end
        if len(df) == 0:
            break
        df.dropna(axis='index', how='all', inplace=True)
        df.dropna(axis='columns', how='all', inplace=True)

        # 6. save to a file
        file_name = "market_data.csv"
        if os.path.exists(file_name):
            df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
        else:
            df.to_csv(file_name, encoding='utf-8-sig', index=False)
        print(f'{idx} page done')
    browser.quit()


main()
