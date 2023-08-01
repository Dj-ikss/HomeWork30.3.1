import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   pytest.driver.maximize_window()
   yield

   pytest.driver.quit()


def test_show_my_pets():
   pytest.driver.find_element(By.ID, 'email').send_keys('Ваш аккаунт')
   pytest.driver.find_element(By.ID, 'pass').send_keys('ваш аккаунт')
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
   time.sleep(2)

   my_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   num_pet = pytest.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]')
   num_pets = int(num_pet.text[15])             # Получаем количество питомцев из инфо пользователя
   images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   anymal_type = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
   age = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

   assert len(my_pets) == num_pets  #количество карточек питомца равно количество питомцев всего в левой части инфо
   assert len(my_pets) > 0          # проверяем, что питомцы присутствуют

   all_names = []        #список имён всех питомцев
   info_all_pets = []    #список информации по каждому питомцу
   for i in range(num_pets):
      assert len(images[i].get_attribute('src')) > (num_pets // 2)  # Проверяем, что фото есть как минимум у половины питомцев
      assert names[i].text != ''                       # Проверяем наличие заполннего имени у питомцев
      assert anymal_type[i].text != ''                 # Проверяем наличие заполннего Порода
      assert age[i].text != ''                         # Проверяем наличие заполннего возраста
      all_names.append(names[i].text)                # Преобразуем в текст список имён
      info_all_pets.append(my_pets[i].text)          # Преобразцем инфо о питомце в список

   duplicates_pets = []
   for n in info_all_pets:
      if info_all_pets.count(n) > 1 and n not in duplicates_pets:
         duplicates_pets.append(n)
   print("Повторяющееся инфо питомца:", duplicates_pets)
   assert len(duplicates_pets) == 0                # Проверяем задвоение питомца (инфо )

   duplicates_name = []
   for item in all_names:
      if all_names.count(item) > 1 and item not in duplicates_name:
         duplicates_name.append(item)
   print("Повторяющиеся имена:", duplicates_name)
   assert len(duplicates_name) == 0                # Проверяем совпадение имён


