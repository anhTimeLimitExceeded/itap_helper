from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
import re

def simulate():
    WORK_STUDY_URL          = "https://my.depauw.edu/e/student/employment/"
    LOGIN_USERNAME_XPATH    = "//*[@id='username']"
    LOGIN_PASSWORD_XPATH    = "//*[@id='pin']"
    LOGIN_BUTTON_XPATH      = "/html/body/div[2]/div/div/div/div/form/input[4]"
    OPEN_TIME_CARD_XPATH    = "/html/body/div/table[2]/tbody/tr/td[2]/table[1]/tbody/tr[1]/td/b"
    ADD_TIME_TEXT           = "Add Time"
    CLEAR_DATETIME_IN       = "/html/body/div/table[2]/tbody/tr/td/form/table/tbody/tr[4]/td[2]/a[2]"
    CLEAR_DATETIME_OUT      = "/html/body/div/table[2]/tbody/tr/td/form/table/tbody/tr[5]/td[2]/a[2]"
    DATETIME_IN_XPATH       = "//*[@id='DATETIME_IN']"
    DATETIME_OUT_XPATH      = "//*[@id='DATETIME_OUT']"
    ADD_RECORD_XPATH        = "//*[@id='submit']"

    USERNAME = ''
    PASSWORD = ''

    driver = webdriver.Chrome('./chromedriver.exe')
    wait = WebDriverWait(driver, 20)

    driver.get(WORK_STUDY_URL)
    #login
    driver.find_element_by_xpath(LOGIN_USERNAME_XPATH).send_keys(USERNAME)
    driver.find_element_by_xpath(LOGIN_PASSWORD_XPATH).send_keys(PASSWORD)
    driver.find_element_by_xpath(LOGIN_BUTTON_XPATH).click()

    #generate times
    wait.until(EC.presence_of_element_located((By.XPATH, OPEN_TIME_CARD_XPATH)))
    timecard_string = driver.find_element_by_xpath(OPEN_TIME_CARD_XPATH).text
    dates = re.findall("([0-9]{2}/[0-9]{2}/[0-9]{4})", timecard_string)
    
    times = generate_times(dates[0], dates[1])

    #fill hours
    for time in times:
        time_start = time[0]
        time_end = time[1]
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, ADD_TIME_TEXT)))
        driver.find_element_by_link_text(ADD_TIME_TEXT).click()
        wait.until(EC.presence_of_element_located((By.XPATH, DATETIME_IN_XPATH)))
        driver.find_element_by_xpath(CLEAR_DATETIME_IN).click()
        driver.find_element_by_xpath(DATETIME_IN_XPATH).send_keys(time_start)
        driver.find_element_by_xpath(CLEAR_DATETIME_OUT).click()
        driver.find_element_by_xpath(DATETIME_OUT_XPATH).send_keys(time_end)
        driver.find_element_by_xpath(ADD_RECORD_XPATH).click()

def generate_times(start_date, end_date):
    # list of start time (14 days) and list of hours worked (14 days)
    start_times = [
          "9:00 AM",    #day 1
          "9:00 PM",    #day 2
          "9:00 PM",    #day 3
          "9:00 PM",    #day 4
          "9:00 PM",    #day 5
          "9:00 PM",    #day 6
          "9:00 PM",    #day 7
          "9:00 PM",    #day 8
          "9:00 PM",    #day 9
          "9:00 PM",    #day 10
          "9:00 PM",    #day 11
          "9:00 PM",    #day 12
          "9:00 PM",    #day 13
          "9:00 PM",    #day 14
    ]
    hours = [
        1.5,#day 1
        0,  #day 2
        0,  #day 3
        0,  #day 4
        0,  #day 5
        0,  #day 6
        0,  #day 7
        0,  #day 8
        0,  #day 9
        2,  #day 10
        0,  #day 11
        0,  #day 12
        0,  #day 13
        1,  #day 14
    ]
    format_datetime = '%m/%d/%Y %I:%M %p'
    format_date     = "%m/%d/%Y"
    format_time     = "%I:%M %p"
    start_date = datetime.strptime(start_date, format_date) 
    end_date = datetime.strptime(end_date, format_date) 
    times = []
    for idx, val in enumerate(start_times):
        if hours[idx] == 0:
            continue    

        start_date = start_date + timedelta(days=idx)
        if start_date > end_date:
            break

        begin_datetime  = datetime.strptime(start_date.strftime(format_date) + " " + start_times[idx], format_datetime)
        end_datetime    = begin_datetime + timedelta(hours=hours[idx])

        begin_time = begin_datetime.strftime(format_datetime)
        end_time = end_datetime.strftime(format_datetime)
        
        times.append((begin_time,end_time))

    return times

simulate()
