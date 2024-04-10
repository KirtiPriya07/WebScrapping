from selenium import webdriver
import pyautogui
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

filename = "data"
link = "https://www.google.com/maps/search/busniess+in+chandigarh/@30.7500649,76.7451944,13z/data=!3m1!4b1?entry=ttu"

browser = webdriver.Chrome()
record = []
e = []
le = 0

def Selenium_extractor():

    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

    while len(a) < 1000:
        print(len(a))
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(scroll_origin, 0, 1000).perform()
        time.sleep(2)
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

        if len(a) == var:
            le+=1
            if le > 20:
                break
        else:
            le = 0

    for i in range(len(a)):
        scroll_origin = ScrollOrigin.from_element(a[i])
        action.scroll_from_origin(scroll_origin, 0, 100).perform()
        action.move_to_element(a[i]).perform()
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try: 
            
            Name_Html = soup.findAll('div', {"class": "qBF1Pd fontHeadlineSmall"})

            name = Name_Html[0].text
            print( "try B", name)
            if name not in e:
                e.append(name)
                divs = soup.findAll('span', {"class": "UsdlK"})
                for j in range(len(divs)):
                    if str(divs[j].text)[0] == "+":
                        phone = divs[j].text

                 #for div in soup.findAll('div', {"class":"W4Efsd"}):
                  #  if div.children == 'span':
                  #      address= div.children.text
                #address_divs = soup.findAll('div', {"class":"W4Efsd"})
                #print("find", address_divs)
                # Address_Html= address_divs[0]
                # address=Address_Html.text
                address = "temprorary"
                
                website_a = soup.findAll('a', {"class" :"lcr4fd S9kvJb "})
                print("find web", website_a)
                try:
                    for z in range(len(website_a)):
                        if str(website_a[z].text)[-4] == "." or str(website_a[z].text)[-3] == ".":
                            website = website_a[z].text
                except:
                    website="Not available"
                print([name,phone,address,website])
                record.append((name,phone,address,website))
                df=pd.DataFrame(record,columns=['Name','Phone number','Address','Website'])  # writing data to the file
                df.to_csv(filename + '.csv',index=False,encoding='utf-8')
        except:
            print("error")
            continue

browser.get(str(link))
time.sleep(10)
Selenium_extractor()