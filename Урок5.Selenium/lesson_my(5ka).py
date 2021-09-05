from selenium import webdriver  # импорт драйвера который будет воздействовать на ядро браузера
from selenium.webdriver.common.keys import Keys  # метод для имитации клавиатуры
from selenium.webdriver.chrome.options import Options  # метод для управления настройками браузера
from selenium.webdriver.support.ui import WebDriverWait                  #1
from selenium.webdriver.support import expected_conditions as EC         #1   ВСЕ они нужны чтобы сделаьть ЯВНУЮ ЗАДЕРЖКУ
from selenium.webdriver.common.by import By                              #1
import selenium.common.exceptions as s_exceptions
import time

"""цель собрать даные со скидками в городе санкт-петербург'"""

chrome_option = Options()
chrome_option.add_argument('--start-maximised')  # открывает экран на макисум=

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_option)   # указываем путь до скачанного драйвера(под браузер) и передаем настройки браузера(не обязательно)
driver.get('https://5ka.ru/special_offers')    # делаем запрос
driver.implicitly_wait(10) # задержка времени автоматическая с максимумом по выдержке 10 секунд, будет действовать перед всеми запросвми к странице(НЕ ЯВНАЯ ЗАДЕРЖКА)

city = driver.find_element_by_class_name('location__select-city')
city.click()

select_city = driver.find_element_by_xpath('//span[text()="г.Санкт-Петербург"]')
select_city.click()

print()
while True:
    try:
        # wait = WebDriverWait(driver,10)  #создаем обьект класса WebDriverWait и передаем туда атрибуты
        # button = wait.until(EC.element_to_be_clickable((By.NAME,'Больше акций')))     # задаем чего мы ожидаем и задаем в атрибут задачу, а в класс presence_of_element_located передаем картеж с путем
        time.sleep(5)
        button = driver.find_element_by_class_name('special-offers__more-btn')
        button.click()
    except s_exceptions.ElementNotInteractableException:
        print('раскрытие страниц законченно')
        break

goods = driver.find_elements_by_class_name('sale-card')
for good in goods[:-3]:
    print(good.find_element_by_class_name('sale-card__title').text)