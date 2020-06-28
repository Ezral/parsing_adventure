# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# Starting time
start = time.time()

# Headless option
options = Options()
options.headless = True

# run Chrome webdriver from executable path of your choice
driver = webdriver.Chrome(options=options, executable_path = '/Users/medicalagent3/chromedriver')

# list of categories
category = ['sayuran','buah','karbohidrat','terbaru','organik','grosir','snack','rempah','daging dan makanan laut','susu telur']

# specify the url
urlpage = [
'https://www.sayurbox.com/products/c/Vegetables',
'https://www.sayurbox.com/products/c/Fruits',
'https://www.sayurbox.com/products/c/Carbs,%20Grains,%20Nuts',
'https://www.sayurbox.com/products/c/Newest%20Items',
'https://www.sayurbox.com/products/c/Organic',
'https://www.sayurbox.com/products/c/Wholesaler',
'https://www.sayurbox.com/products/c/Snacks%20&%20Nibbles',
'https://www.sayurbox.com/products/c/Herbs%20&%20Spices',
'https://www.sayurbox.com/products/c/Daging%20&%20Makanan%20Laut',
'https://www.sayurbox.com/products/c/Olahan%20Susu%20dan%20Telur'
]

# empty dictionary to store all the dataframes
sb_df = {}

# for loop to scrape data and create dataframe 
for n in range(0,len(urlpage)):
    print("Start scraping from {}".format(urlpage[n]))

    # get web page
    driver.get(urlpage[n])
    # execute script to scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # sleep for 30s
    time.sleep(30)

    # find elements by xpath
    # results = driver.find_elements_by_xpath('//*[@id="__next"]//*[contains(@id,"ProductItem__container__name")]//*[@class="ProductItem__container__shortDesc"]//*[@class="Product__container__priceWrapper__price"]//*[@class="Product__container__priceWrapper__packDesc"]')
    name = driver.find_elements_by_xpath('//*[@class="ProductItem__container__name"]')
    description = driver.find_elements_by_xpath('//*[@class="ProductItem__container__shortDesc"]')
    price = driver.find_elements_by_xpath('//*[@class="Product__container__priceWrapper__price"]')
    unit = driver.find_elements_by_xpath('//*[@class="Product__container__priceWrapper__packDesc"]')

    # Return the number of result found
    print('Number of results', len(name))

    # create empty arrays to store data for name, price and unit respectively
    item_name = []
    item_description = []
    item_price = []
    item_unit = []

    # loop over results to store name, price and unit on their own lists separately.
    for result in name:
        product_name = result.text
        item_name.append(product_name)

    for result in description:
        product_name = result.text
        item_description.append(product_name)

    for result in price:
        product_name = result.text
        item_price.append(product_name)

    for result in unit:
        product_name = result.text
        item_unit.append(product_name)

    # create data file
    df = pd.DataFrame({'product':item_name,'desc':item_description,'price':item_price,'unit':item_unit})

    # create data file
    df['link'] = 'https://www.sayurbox.com/p/' + df['product'].str.replace(' ','%20').str.replace('(','').str.replace(')','')

    # write to csv
    sb_df[n] = df
    

# close webdriver after loop is completed
driver.quit()

# reading all the datasets into dataframes
sb = [sb_df[0],sb_df[1],sb_df[2],sb_df[3],sb_df[4],sb_df[5],sb_df[6],sb_df[7],sb_df[8],sb_df[9]]

# adding category column to all dataframe
for n in range(0,len(category)):
    sb[n]['category'] = category[n]

# merging all the dataframes
sayurbox_merged = pd.concat(sb,ignore_index=True)

# cleaning and converting price column into integer
sayurbox_merged['price'] = sayurbox_merged['price'].str.replace('Rp. ','').str.replace('.','').astype(int)

# write to csv
sayurbox_merged.to_csv('sayurbox_merged.csv')

# Printing elapsed time
proc_time = time.time() - start
print("Scraping completed in: {} sec.".format(str(proc_time)))
