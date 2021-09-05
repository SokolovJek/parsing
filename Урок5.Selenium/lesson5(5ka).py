from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions as s_exceptions

chrome_options = Options()
chrome_options.add_argument("--start-maximized")


driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.get('https://5ka.ru/special_offers/')

driver.implicitly_wait(10)

city = driver.find_element_by_class_name('location__select-city')
city.click()

city = driver.find_element_by_xpath('//span[text()="г.Санкт-Петербург"]')
city.click()

while True:
    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'special-offers__more-btn')))
        # button = driver.find_element_by_class_name('special-offers__more-btn')
        button.click()
    except s_exceptions.TimeoutException:
        print('раскрытие страниц законченно')
        break

# goods = driver.find_elements_by_class_name('sale-card')
# for good in goods[:-3]:
#     print(good.find_element_by_class_name('sale-card__title').text)