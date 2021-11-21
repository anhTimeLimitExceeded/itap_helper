from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, time, timedelta
import re
import json

def read_cookies():
    return json.load(open('cookie.json'))["cookies"]
    
def simulate():
    WORK_STUDY_URL          = "https://my.depauw.edu/e/student/employment/"
    DUMMY_URL               = "https://my.depauw.edu/a"
    LOGIN_USERNAME_XPATH    = "//*[@id='username']"
    LOGIN_PASSWORD_XPATH    = "//*[@id='pin']"
    LOGIN_BUTTON_XPATH      = "/html/body/div[2]/div/div/div/div/form/input[4]"
    OPEN_TIME_CARD_XPATH    = "/html/body/div/table[2]/tbody/tr/td[2]/p[1]"
    ADD_TIME_TEXT           = "Add Time"
    CLEAR_DATETIME_IN       = "/html/body/div/table[2]/tbody/tr/td/form/table/tbody/tr[4]/td[2]/a[2]"
    CLEAR_DATETIME_OUT      = "/html/body/div/table[2]/tbody/tr/td/form/table/tbody/tr[5]/td[2]/a[2]"
    DATETIME_IN_XPATH       = "//*[@id='DATETIME_IN']"
    DATETIME_OUT_XPATH      = "//*[@id='DATETIME_OUT']"
    ADD_RECORD_XPATH        = "//*[@id='submit']"

    USERNAME = ''
    PASSWORD = ''

    driver = webdriver.Chrome('../selenium-drivers/chromedriver.exe')
    wait = WebDriverWait(driver, 20)

    driver.get(WORK_STUDY_URL)

    #login
    driver.find_element_by_xpath(LOGIN_USERNAME_XPATH).send_keys(USERNAME)
    driver.find_element_by_xpath(LOGIN_PASSWORD_XPATH).send_keys(PASSWORD)
    driver.find_element_by_xpath(LOGIN_BUTTON_XPATH).click()


    # generate times
    wait.until(EC.presence_of_element_located((By.XPATH, OPEN_TIME_CARD_XPATH)))
    timecard_string = driver.find_element_by_xpath(OPEN_TIME_CARD_XPATH).text
    dates = re.compile("Current pay period is (.*) - (.*).").findall(timecard_string)[0]
    times = generate_times(dates[0], dates[1])
    print(f'times generated {times}')

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
          ("7:30 PM", 2.5),   #day 1      Sunday
          ("8:00 PM", 2),   #day 2      Monday
          ("8:00 PM", 0),   #day 3      Tuesday
          ("8:00 PM", 0),   #day 4      Wednesday
          ("8:00 PM", 2),   #day 5      Thursday
          ("10:00 AM", 3),  #day 6      Friday
          ("8:00 PM", 1),   #day 7      Saturday
          ("8:00 PM", 0),   #day 8      Sunday
          ("8:00 PM", 0),   #day 9      Monday
          ("8:00 PM", 2.5),   #day 10     Tuesday
          ("8:00 PM", 1.5),   #day 11     Wednesday
          ("8:00 PM", 1),   #day 12     Thursday
          ("10:00 AM", 0.5),  #day 13     Friday
          ("8:00 PM", 0)   #day 14     Saturday
    ]

    format_datetime = '%m/%d/%Y %I:%M %p'
    format_date     = "%m/%d/%Y"
    format_calendar = "%B %d"
    format_time     = "%I:%M %p"
    start_date = datetime.strptime(start_date, format_calendar).replace(year=datetime.now().year)
    end_date = datetime.strptime(end_date, format_calendar).replace(year=datetime.now().year) 
    times = []
    for index in range(0, len(start_times)):
        (start_time, hour) = start_times[index]
        if hour == 0:
            continue    

        current_date = start_date + timedelta(days=index)
        if current_date > end_date:
            break

        begin_datetime  = datetime.strptime(current_date.strftime(format_date) + " " + start_time, format_datetime)
        end_datetime    = begin_datetime + timedelta(hours=hour)

        begin_time = begin_datetime.strftime(format_datetime)
        end_time = end_datetime.strftime(format_datetime)
        
        times.append((begin_time,end_time))

    return times

simulate()
