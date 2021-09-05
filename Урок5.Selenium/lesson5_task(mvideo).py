from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


chrome_option = Options()
chrome_option.add_argument('--window-size=1700,1000')


driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_option)
driver.get('https://www.mvideo.ru/')
driver.implicitly_wait(10)
actions = ActionChains(driver)

product = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[7]//li')

actions.move_to_element(product)
actions.perform()
link = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[7]/div/div[2]/div/div[1]/a[contains(@class,"i-icon-fl-arrow-right")]')

new_set = set()
for i in range(5):
    descriptions = driver.find_elements_by_xpath(
        '/html/body/div[2]/div/div[3]/div/div[7]//li/'
        '/a[@class="fl-product-tile-title__link sel-product-tile-title"]')
    for description in descriptions:
        new_set.add(description.text)
    link.click()
new_list=[]
for i in new_set:
    new_list.append(i)

client = MongoClient('localhost', 27017)
db = client['lesson5']
my = db.my

my_dict = {'новинки':new_list}
my.insert_one(my_dict)