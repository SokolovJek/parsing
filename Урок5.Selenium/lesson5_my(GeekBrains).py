from selenium import webdriver  # импорт драйвера который будет воздействовать на ядро браузера
from selenium.webdriver.common.keys import Keys  # метод для имитации клавиатуры
from selenium.webdriver.chrome.options import Options  # метод для управления настройками браузера
import time
"""цель занятия c помощью SELENIUM зайти на сайт geekBrains авторизоватся, и дойти до пункта 'редактирования профиля'"""

chrome_option = Options()
# chrome_option.add_argument('--start-maximised')  # открывает экран на макисум
chrome_option.add_argument("--window-size=760,1248")  # открывает экран на макисум(не обязательно)

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_option)   # указываем путь до скачанного драйвера(под браузер) и передаем настройки браузера(не обязательно)
driver.get('https://gb.ru/login')    # делаем запрос


elem = driver.find_element_by_id('user_email')   # узнаем в HTML  коде id поля для вода(можно и подругому)
elem.send_keys('study.ai_172@mail.ru')    # вводим логин

elem = driver.find_element_by_id('user_password')
elem.send_keys('Password172')
elem.send_keys(Keys.ENTER)   #имитациия нажатия ENTER

time.sleep(0.50)
menu = driver.find_element_by_xpath('//span[text()="меню"]')
menu.click()  #метод имитация нажатия левой кнопки миши(клик)

menu = driver.find_element_by_xpath('//button[@data-test-id="user_dropdown_menu"]') #переходим дальше
menu.click()

link = driver.find_element_by_xpath('//li/a[contains(@href,"/users/")]')
# link.click()   # можно так(но предлагают так)
driver.get(link.get_attribute('href'))
print()