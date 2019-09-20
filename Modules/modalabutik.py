
import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import xlsxwriter
import pandas as pd
from collections import OrderedDict
import csv

main_url="https://www.modaalabutik.com/urunler/tesettur-giyim?ps=1"


def setWebDriver(webdriver,Options):
    chrome_options = Options()
    #chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    chrome = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    return chrome


def openPage(page,chrome):
    chrome.get(page)
    #assert 'Bizi' in chrome.title
    print("Opened ", page)
    sleep(5)
    try:
        cookie=chrome.find_element_by_id('onesignal-popover-cancel-button')
        if cookie:
            cookie.click()
    except:
        pass
    return chrome

def getCards(chrome):
    cards=chrome.find_elements_by_css_selector(".col-md-4.col-sm-6.col-xs-6.col-6.prodItem")
    return cards


def openCards(cards):
    j=0
    sub_url=[]
    for i in cards:
        i.click()
        sleep(2)
        #sub_url=i.find_elements_by_xpath("//a[@href]")
        #sub_url=i.find_element_by_link_text(".product-full-name.a")
        sub_url.append(i.find_element_by_xpath('//*[@id="veri-formu"]/div/div[2]/div[1]/a[2]').get_attribute('href'))
        close=i.find_element_by_xpath('/html/body/div[6]/a')
        close.click()
        j+=1
        print(j)
        sleep(1)

    return sub_url



def getData(sub_urls,webdriver):
    types=[]
    publishes=[]
    featureds=[]
    visCats=[]
    taxes=[]
    stocks=[]
    backorders=[]
    soldInds=[]
    reviews=[]
    #--------------------
    parents=[]
    categories=[]
    names=[]
    prices=[]
    descripts=[]


    type="variable"
    published=1
    featured=0
    vis_cat='visible'
    tax="taxable"
    inStock=1
    backorder=0
    soldInd=0
    review=1

    for i in sub_urls:
        chrome=openPage(i,webdriver)
        """Adding fix values"""
        types.append(type)

        publishes.append(published)

        featureds.append(featured)

        visCats.append(vis_cat)

        taxes.append(tax)

        stocks.append(inStock)

        backorders.append(backorder)

        soldInds.append(soldInd)

        reviews.append(review)

        """Adding parent"""
        parent=chrome.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/span").text
        parents.append(parent)

        """Categories Adding"""
        category=chrome.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/ul/li[2]/a/span").text
        categories.append(category)



        """Names adding"""
        name=chrome.find_element_by_xpath('//*[@id="veri-formu"]/div/div[2]/div[1]/h2').text
        name=name.split("-")[0]
        names.append(name)

        """Sales price adding"""
        price=chrome.find_element_by_xpath('//*[@id="veri-formu"]/div/div[2]/div[2]').text
        price=price.split(' ')[0]
        prices.append(price)

        # parent=chrome.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/span').text
        # parents.append(parent)

        """Description adding"""
        tabs=chrome.find_element_by_css_selector('.product-detail-content')
        descript = [item.text for item in tabs.find_elements_by_xpath(".//*[self::td or self::th]")]
        descripts.append(descript)

        # for table in tabs:
        #     data=[item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
        #     print(data)

    createCSV(sub_urls,types,	publishes,	featureds,	visCats,	taxes,	stocks,	backorders,	soldInds,	reviews,	parents,	categories,	names,	prices,	descripts,
)




def createCSV(subUrls, types,	publishes,	featureds,	visCats,	taxes,	stocks,	backorders,	soldInds,	reviews,	parents,	categories,	names,	prices,	descripts,
):
    dict=OrderedDict()
    dict['Explicit URL'] = sub_urls
    dict['Type'] = types
    dict['Published'] = publishes
    dict['Is featured?'] = featureds
    dict['Visibility in catalog'] = visCats
    dict['Tax status'] = taxes
    dict['In stock?'] = stocks
    dict['Backorders allowed?'] = backorders
    dict['Sold individually?'] = soldInds
    dict['Allow customer reviews?'] = reviews
    dict['Parent'] = parents
    dict['Categories'] = categories
    dict['Name'] = names
    dict['Sale price'] = prices
    dict['Description']=descripts

    # for k,v in dict.items():
    #     print(k,"\n",v)

    df=pd.DataFrame.from_dict(dict)
    df.to_csv("modalabutik_scraped_sample.csv",index=False,encoding='ISO-8859-9')
    # with open('modalabutik_scraped_sample.csv', 'w') as f:
    #     for key in dict.keys():
    #         f.write("%s,%s\n"%(key,dict[key]))

po=openPage(main_url,setWebDriver(webdriver,Options))
cards=getCards(po)
sub_urls=openCards(cards)
getData(sub_urls,setWebDriver(webdriver,Options))



