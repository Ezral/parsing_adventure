import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import pandas as pd

'''IDI online member list scraping steps:
1. Start webdriver
2. Open URL
3. Preparing selection
    Input 'a' into "Nama Lengkap" filter
    Select 200 for pagination filter
    Click "Search" button
4. Scraping values
    Run for loop in all pages:
       Run for loop in 200 rows:
           Iter through all the xpaths
           Append to respective lists
       Click Next page
5. Importing dataframe to csv'''

'''1. STARTING WEBDRIVER'''
# Starting time
start = time.time()
# Set the headless option to True/False for webdriver
options = Options()
options.headless = False
# Executable path for webdriver
webdriver_path = '/Users/medicalagent3/chromedriver'
# Running the webdriver
driver = webdriver.Chrome(options=options, executable_path = webdriver_path)

'''2. OPENING URL'''
# URL for website
url = "http://www.idionline.org/about/direktori-anggota/"
driver.get(url)
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
time.sleep(5)
# xpath for name filter
name = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td/table/thead/tr[2]/td[3]/input")
# xpath for pagination filter
select = driver.find_element_by_id("filter_pagination")
# xpath for search button
search_btn = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[1]/td/span[2]/input[1]")

'''3. PREPARING SELECTION
(comment out this section to start at page 1)'''
# Input 'a' into "Nama Lengkap" filter
name.send_keys("%")
# Select 200 for pagination filter
Select(select).select_by_value("200")
# Page selection (comment out this section to start at page 1)
driver.find_element_by_link_text("788").click()
# 3s sleep to allow page to load
time.sleep(3)

'''4. SCRAPING VALUES'''
nama = []
gelar_dpn = []
gelar_blkg = []
npa = []
wilayah = []
cabang = []

for p in range(1,395):
    # iter starts
    iter_start = time.time()
    # xpath for prev button
    prev_btn = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[1]/td/span[1]/span[1]/a")
    # xpath for next button
    # next_btn = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td/span[1]/span[14]/a")
    for i in range(1,201):
        name = "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{}]/td[3]".format(i)
        pref = "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{}]/td[4]".format(i)
        suf = "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{}]/td[5]".format(i)
        id = "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{}]/td[6]".format(i)
        prov = "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{}]/td[7]".format(i)
        branch = "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{}]/td[8]".format(i)
        nama.append(driver.find_element_by_xpath(name).text)
        gelar_dpn.append(driver.find_element_by_xpath(pref).text)
        gelar_blkg.append(driver.find_element_by_xpath(suf).text)
        npa.append(driver.find_element_by_xpath(id).text)
        wilayah.append(driver.find_element_by_xpath(prov).text)
        cabang.append(driver.find_element_by_xpath(branch).text)
    iter_time = time.time() - iter_start
    print("Iteration #{x} completed in {y} sec.".format(x=p,y=str(iter_time)))
    prev_btn.click()
    # next_btn.click()
    time.sleep(3)

'''5. IMPORTING DATAFRAME TO CSV'''
# create data file
df = pd.DataFrame({'name':nama,'prefix':gelar_dpn,'suffix':gelar_blkg,'id_number':npa,'province':wilayah,'area':cabang})
# Define time str format
now = datetime.now().strftime("%Y%m%d-%H%M")
# write to csv
df.to_csv('/Users/medicalagent3/idi_member_part2_{}.csv'.format(now))
# Printing process time
proc_time = time.time() - start
print("/Users/medicalagent3/idi_member_part2_{}.csv saved in /Users/medicalagent3/".format(now))
print("Total time elapsed: {} sec.".format(str(proc_time)))
