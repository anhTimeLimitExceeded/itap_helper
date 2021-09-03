# About
This is a python script that simulates ITAP hours logging\
\
ITAP is a DePauw's program that allows student to work on campus and thus students need to log hours on the school's website. This scripts runs a simulation of that process using Selenium and Chromium Driver

# How to run
## Requirements
Python 3 and Selenium installed. How to install selenium:
```
pip3 install selenium
```
## Running
```
python3 script.py
```
## Customizing the code
### Providing credentials
Locate this code snippet in script.py
```
USERNAME = ''
PASSWORD = ''

driver = webdriver.Chrome('./chromedriver.exe')
wait = WebDriverWait(driver, 20)
...
```
Replace with your credentials. For exmaple:
```
USERNAME = 'anhle_2023'
PASSWORD = 'p@55w0rd'

driver = webdriver.Chrome('./chromedriver.exe')
wait = WebDriverWait(driver, 20)
...
```

### Changing logged hours
Locate this code snippet in script.py
```
def generate_times(start_date, end_date):
    # list of start time (14 days) and list of hours worked (14 days)
    start_times = [
          "9:00 PM",    #day 1
          "11:00 PM",    #day 2
          "8:30 PM",    #day 3
          ...
    ]
    hours = [
        1.5,#day 1
        0,  #day 2
        ...
    ]
```

`start_times` is the array of starting hours (default to be 9:00 PM)\
`hours` is the array of hours worked (default to be 0)\
The two arrays are set to length 14 (14 days or 2 weeks of logging). If the hour is 0 then that day will be ignored. You don't have to delete anything, you only need to change the start time and the hours worked.
