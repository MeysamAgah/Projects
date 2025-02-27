from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def find_urls(city, country, type_='apartment'):
  driver = web_driver()
  driver.get(f"https://www.airbnb.com/{city}-{country}/stays")
  time.sleep(5)
  if type_ == 'apartment':
    driver.find_elements(By.CLASS_NAME, "b120n5ee")[0].click()
    time.sleep(5)
  elif type_ == 'home':
    driver.find_elements(By.CLASS_NAME, "b120n5ee")[1].click()
    time.sleep(5)
  elif type_ == 'other':
    driver.find_elements(By.CLASS_NAME, "b120n5ee")[2].click()
    time.sleep(5)    
  else:
    raise ValueError('type is not writen correctly')
  
  links = []
  last_page = int(driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[1]/main/div[2]/div/div[3]/div/div/div/nav/div/a[4]").text)

  while int(driver.find_element(By.CSS_SELECTOR, 'button[aria-current="page"][disabled][role="link"]').text) < last_page:
    for e in driver.find_elements(By.CSS_SELECTOR, 'a.rfexzly'):
      links.append(e.get_attribute('href'))

    driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]').click()
    time.sleep(5)

  for e in driver.find_elements(By.CSS_SELECTOR, 'a.rfexzly'):
    links.append(e.get_attribute('href'))

  driver.quit()
  links = list(set(links))
  return links
