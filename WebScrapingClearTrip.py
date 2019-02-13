#importing lib
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

#cleartrip Url country  and city
url = "https://me.cleartrip.com/hotels/results?city=Miami&country=US&state=&dest_code=&area=&poi=&hotelId=&hotelName=&chk_in=13/02/2019&chk_out=14/02/2019&org=&num_rooms=1&adults1=2&children1=0&utm_source=google&utm_medium=organic&utm_campaign=Redirection"
#borwser driver
browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
browser.get(url)
content = browser.page_source
browser.quit()

soup = BeautifulSoup(content,"lxml")
#Find all link f hotel
hotelNames = soup.find_all('a',class_="hotelDetails")

hotelLink1  =  [name.get('href') for name in hotelNames]

#Removing all dumplicate links
list1=[]
for x in hotelLink1:
  result = x[:x.find("#") + 1]
  list1.append(result)

hotelLink=[]
for i in list1:
    if i not in hotelLink:
        hotelLink.append(i)

##

clearTripUrl="https://me.cleartrip.com/"

#create finalResult json variables
finalResult={}
for link in hotelLink:
    finalResult["link"]=[]
    finalResult["name"]=[]
    finalResult["location"]=[]

    hotel=(clearTripUrl+link)
    html = urlopen(hotel)
    bsObj = BeautifulSoup(html, "html.parser")


    hoteldetail=bsObj.find('div',{'class':'colZero col24'})
    #Remove \n \t
    name=hoteldetail.div.h1.text.replace("\n","")
    name=name.replace("\t","")

    #Remove \n \t
    location=hoteldetail.div.h1.small.text.replace("\n","")
    location=location.replace("\t","")

    finalResult["name"].append(name)
    finalResult["location"].append(location)
    finalResult["link"].append(hotel)

    #Getting Hotel Details
    container=bsObj.findAll('div',{'class':'col col16 amenitiesDescription'})
    container=container[0]
    amenitiesCategory=container.findAll('div',{'class':'amenitiesCategory'})


    for x in range(1,len(amenitiesCategory)-1):
        if(x==1):
            listt=amenitiesCategory[x].findAll('li')
            for y in range(0,len(listt)):
                finalResult[listt[y].small.text]=[]
                finalResult[listt[y].small.text].append(listt[y].span.text)
        else:

            listt=amenitiesCategory[x].findAll('li')
            finalResult[amenitiesCategory[x].strong.text]=[]
            for y in range(0,len(listt)):

                finalResult[amenitiesCategory[x].strong.text].append(listt[y].text)
    print(finalResult)
