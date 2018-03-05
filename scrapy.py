# import libraries

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

# specify the url
paperPage = "https://www.jagran.com"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(paperPage, headers=hdr)
page = urllib2.urlopen(req)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, "html.parser")
# Take out the <div> of name and get its value
paperLink = soup.find('a', text="Epaper")
epaperLink = paperLink.get('href')

req = urllib2.Request(epaperLink, headers=hdr)
page = urllib2.urlopen(req)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, "html.parser")

stateNameList = []
superCityState = [[]]
citiesFromSupercity = {}
paperLink = soup.find('ul', id="navbar").find_all(recursive=False)
for name in paperLink:
    findStateName = name.find('a', href="#")
    if findStateName is not None:
        stateName = findStateName.text.strip(";")
        stateNameList.append(stateName)



#capa = DesiredCapabilities.CHROME
#capa["pageLoadStrategy"] = "none"
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("http://epaper.jagran.com/homepage.aspx")
dataEpaper = {}
dataEpaper['state'] = []
for stateVar in stateNameList:
    # select first state
    print("+++++++++++++++++++++++++")
    print(stateVar)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #if (stateVar=="Delhi") | (stateVar=="UP") | (stateVar=="Haryana") | (stateVar=="Uttarakhand") | (stateVar=="Bihar") :
        #continue
    epaperLinkList = []
    dataEpaper['state'].append({
        'name':stateVar,
        'city':epaperLinkList
    })
    stateWebElement = driver.find_element_by_xpath('//ul[@id="navbar"]//a[text()="%s" and @href="#"]' %stateVar)
    hoverOverOnState = ActionChains(driver).move_to_element(stateWebElement).perform()
    superCityWebElement = stateWebElement.find_elements_by_xpath('./..//section/ul/li/a[@href="#" or text()="%s"]' %stateVar)

    print(len(superCityWebElement))
    superCityList = []
    for superCityWeb in superCityWebElement:
        print(superCityWeb)
        superCityList.append(superCityWeb.text)
        print(superCityWeb.text)
    print("-----------")
    for superCity in superCityList:
        #if (superCity == "Dhanbad") | (superCity == "Jamshedpur") : #| (superCity == "Allahabad") | (superCity == "Bareilly") | (superCity == "Gorakhpur") | (superCity == "Kanpur") | (superCity == "Jhansi") :
            #continue
        stateWebElementFirst = driver.find_element_by_xpath(
            '//ul[@id="navbar"]//a[text()="%s" and @href="#"]' % stateVar)
        superCityWebElementFirst = stateWebElementFirst.find_element_by_xpath(
            './..//section/ul/li/a[text()="%s"]' %superCity)
        hoverOverOnStateFirst = ActionChains(driver).move_to_element(stateWebElementFirst)
        hoverOverOnSuperCityFirst = hoverOverOnStateFirst.move_to_element(superCityWebElementFirst)
        hoverOverOnSuperCityFirst.perform()

        superCityName = superCity
        print("#################")
        print(superCity)
        print("#################")
        citiWebElement = superCityWebElementFirst.find_elements_by_xpath('./../ul//li')
        cityList = []
        for cityWeb in citiWebElement:
            cityList.append(cityWeb.text)
            print(cityWeb.text)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        for city in cityList:
            cityObject = {}
            cityCode = ""
            staleElement = True
            while (staleElement):
                try:
                    wait.until(EC.visibility_of_element_located((By.ID, 'navbar')))
                    #driver.execute_script("window.stop();")
                    stateWebElementAgain = driver.find_element_by_xpath(
                        '//ul[@id="navbar"]//a[text()="%s" and @href="#"]' % stateVar)
                    superCityWebElementAgain = stateWebElementAgain.find_element_by_xpath(
                        './..//section/ul/li/a[text()="%s"]' % superCityName)
                    hoverOverOnStateAgain = ActionChains(driver).move_to_element(stateWebElementAgain)
                    hoverOverOnSuperCityAgain = hoverOverOnStateAgain.move_to_element(superCityWebElementAgain)
                    hoverOverOnSuperCityAgain.perform()
                    #cityName = city.text
                    print("#################")
                    print(city)
                    print("#################")
                    cityXPath = superCityWebElementAgain.find_element_by_xpath(
                        './..//li/a[text()="%s"]' % city)
                    #myxpath = ('//li/a[text()="%s"]' % city)
                    #element = wait.until(
                        #EC.element_to_be_clickable((By.XPATH, cityXPath)))
                    #time.sleep(1)
                    cityXPath.click()
                    #time.sleep(1)
                    wait.until(EC.visibility_of_element_located((By.ID, 'navbar')))
                    print("&&&&&&&&&&&&&&&&&&&&&&found &&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    driver.execute_script("window.stop();")
                    elementPdfLink = wait.until(
                        EC.element_to_be_clickable((By.XPATH, '//a[@href="#" and @class="pdf"]')))
                    driver.find_element_by_xpath('//a[@href="#" and @class="pdf"]').send_keys(Keys.ESCAPE)#findElement((By.XPATH, '//a[@href="#" and @class="pdf"]')).sendKeys("Keys.ESCAPE");
                    elementPdfLink.click()
                    #time.sleep(1)
                    windowTab = driver.window_handles
                    for tab in windowTab:
                        if tab != windowTab[0]:
                            driver.switch_to.window(tab)
                            codeUrl = driver.current_url
                            print(codeUrl)
                            matchObj = re.match(r'http://epaper.jagran.com/epaperimages/\d+/.+/\d\d(.+)-pg.+', codeUrl, re.M | re.I)
                            cityCode = matchObj.group(1)
                            driver.close()
                    cityObject[city] = cityCode
                    epaperLinkList.append(cityObject)
                    driver.switch_to.window(windowTab[0])
                    print("coming till here")
                    json_data = json.dumps(dataEpaper)
                    print(json_data)
                    staleElement = False
                except Exception as e:
                    print("it is stale")
                    print(e)
                    cityObject[city] = "NOT Found"
                    for window in driver.window_handles:
                        driver.switch_to.window(window)
                        try:
                            driver.switch_to.alert.accept()
                        except NoAlertPresentException:
                            pass
                    windowTab = driver.window_handles
                    for tab in windowTab:
                        if tab != windowTab[0]:
                            driver.switch_to.window(tab)
                            codeUrl = driver.current_url
                            print(codeUrl)
                            driver.close()
                    driver.switch_to.window(windowTab[0])
                    traceback.print_exc()
                    staleElement = False



assert "No results found." not in driver.page_source
driver.close()

json_data = json.dumps(dataEpaper)
print(json_data)


