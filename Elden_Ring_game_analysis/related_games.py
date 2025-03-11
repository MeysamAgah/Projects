from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def web_driver(user_agent_string='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'):
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920, 1200")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"user-agent={user_agent_string}")
    driver = webdriver.Chrome(options=options)
    return driver

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

def game_platforms(game):
  """
  input:
    - game name
  output:
    - list of game platforms
  """
  driver = web_driver()
  url = f"https://www.metacritic.com/game/{game}/user-reviews/"
  driver.get(url)

  time.sleep(5)
  
  platforms = driver.find_element(By.CLASS_NAME, "c-siteDropdown_choice").text.split('\n')
  
  corrected_platforms = []
  for p in platforms:
    p = p.lower()
    p = p.replace(' ', '-')
    corrected_platforms.append(p)

  driver.quit()

  return corrected_platforms
