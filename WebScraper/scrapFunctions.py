from packageManager import *

def get_link(driver):
    # this block contains image link and description
    img_elements = driver.find_elements_by_xpath("//img[@class='_6uf91T z-oVg8 u-6V88 ka2E9k uMhVZi FxZV-M _2Pvyxl JT3_zV EKabf7 mo6ZnF _1RurXL mo6ZnF PZ5eVw']")
    # linkList is to store image link and alternative description
    linkList:list = []
    # save info to the list
    for element in img_elements:
        link = element.get_attribute("src")
        description = element.get_attribute("alt")
        # add new record to list [link, description]
        linkList.append([link, description])
    driver.implicitly_wait(1)
    return linkList

def get_brand(driver):
    # this block contains brand and description (should be identical of the last block
    tag_elements = driver.find_elements_by_class_name('hPWzFB')
    # detailList is to store brand and description information
    brandList:list = []
    # save info to the list
    for element in tag_elements:
        brand = element.find_element_by_tag_name('span').text
        description = element.find_element_by_tag_name('h3').text
        brandList.append([brand, description])
    driver.implicitly_wait(1)
    return brandList