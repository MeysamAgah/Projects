from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def related_games(game):
  """
  input:
    - game name
  output:
    - list of related games according to metacritic
  """
  driver = web_driver()
  url = f"https://www.metacritic.com/game/{game}/"
  driver.get(url)

  related_games = []
  for e in driver.find_elements(By.CLASS_NAME, "c-globalProductCard_container"):
    try:
      related_games.append(e.get_attribute('href').split('/')[-2])
    except:
      print('failed to get a related game name')
  
  driver.quit()
  
  return related_games
