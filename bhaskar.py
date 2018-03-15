import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import traceback
import json
import re

stateNameList = []
superCityState = [[]]
citiesFromSupercity = {}
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(desired_capabilities=capa)
wait = WebDriverWait(driver, 20)
driver.get("http://epaper.bhaskar.com/")
dataEpaper = {}
dataEpaper['state'] = []
wait.until(EC.visibility_of_element_located((By.ID, 'DFP_728_90_ATF_2')))
stateWebElement = driver.find_elements_by_xpath("//div[@class='epaper']/ul/li/a")
i = 1
for stateWeb in stateWebElement:
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='epaper']/ul/li[%d]/a" % i)))
        eachStateWebElement = driver.find_element_by_xpath("//div[@class='epaper']/ul/li[%d]/a" % i)
        urlElement = eachStateWebElement.get_attribute("href")
        matchObj = re.match(r'http://.+.bhaskar.com/(\w+)', urlElement, re.M | re.I)
        stateName = matchObj.group(1)
        print(stateName)
        epaperLinkList = []
        dataEpaper['state'].append({
            'name': stateName,
            'city': epaperLinkList
        })
        stateNameList.append(stateName)
        i = i + 1
        eachStateWebElement.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'DFP_728_90_ATF_2')))
        cityWebElement = driver.find_elements_by_xpath("//div[@class='epaper']/ul/li/a")
        x = 1
        for cityElement in cityWebElement:
            try:
                cityObject = {}
                cityCode = ""
                wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='epaper']/ul/li[%d]/a" % x)))
                eachCityWebElement = driver.find_element_by_xpath("//div[@class='epaper']/ul/li[%d]/a" % x)
                urlcityElement = eachCityWebElement.get_attribute("href")
                matchObj = re.match(r'http://.+.bhaskar.com/(\w+)', urlcityElement, re.M | re.I)
                # http://epaper.bhaskar.com/jaipur/14/14032018/0/1/
                cityName = matchObj.group(1)
                print(cityName)
                x = x + 1
                eachCityWebElement.click()
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'pdf')))
                driver.find_element_by_class_name("pdf").click()
                time.sleep(2)
                windowTab = driver.window_handles
                for tab in windowTab:
                    if tab != windowTab[0]:
                        driver.switch_to.window(tab)
                        codeUrl = driver.current_url
                        print(codeUrl)
                        try:
                            matchObj = re.match(r'http://digitalimages.bhaskar.com(.+)?/epaperpdf/\d+/\d\d(.+)-PG.+',
                                                codeUrl,
                                                re.M | re.I)
                            #                     http://digitalimages.bhaskar.com/epaperpdf/14032018/13JAIPURCITY-PG12-0.PDF
                            #                     http://digitalimages.bhaskar.com/cph/epaperpdf/14032018/13JALANDHAR%20CITY-PG1-0.PDF
                            cityCode = matchObj.group(2)
                            otherCode = matchObj.group(1)
                            if otherCode is None:
                                otherCode = ""
                            cityObject["extraParam"] = otherCode
                            newcitycode = cityCode.replace('%20', ' ')
                            cityObject[cityName] = newcitycode
                            epaperLinkList.append(cityObject)
                            driver.close()
                            time.sleep(2)
                        except Exception as e:
                            traceback.print_exc()
                            cityObject[cityName] = "Error"
                            epaperLinkList.append(cityObject)
                            driver.close()
                            time.sleep(2)
                # cityObject[city] = cityCode
                # epaperLinkList.append(cityObject)
                driver.switch_to.window(windowTab[0])
                json_data = json.dumps(dataEpaper)
                print(json_data)
                driver.back()
                time.sleep(2)
            except Exception as e:
                traceback.print_exc()
        driver.back()
        time.sleep(2)
    except Exception as e:
        traceback.print_exc()