from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import os, sys

PATH = os.path.abspath(os.path.dirname(sys.argv[0]))

USER = 'pattersonkvn@aim.com'
PW = 'GTech19!'


def load_driver():
    options = Options()
    options.add_experimental_option("prefs", {
      "download.default_directory": PATH,
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(options=options)
    return driver


def first(driver):
    driver.get("https://nhpd.preservationdatabase.org/Data")
    inputUser = driver.find_element_by_id("Email")
    inputUser.send_keys(USER)
    inputPw = driver.find_element_by_id("Password")
    inputPw.send_keys(PW)
    time.sleep(1)
    inputPw.send_keys(Keys.ENTER)
    select = Select(driver.find_element_by_id('downloadFileId'))
    select.select_by_visible_text('Active and Inconclusive Properties GA(xlsx)')
    driver.find_element_by_xpath("//input[@value='Download Complete Database']").click()
    time.sleep(10)
    driver.close()



scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', seconds=30)
def refresh():
    driver = load_driver()
    first(driver)


refresh()
scheduler.start()