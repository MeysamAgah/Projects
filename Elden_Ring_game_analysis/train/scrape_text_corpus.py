# imports
from selenium import webdriver
from selenium.webdriver.common.by import By

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

def extract_game_reviews_url(num_pages=1):
  """
  This function will crawl into pages to extract urls of game reviews on gamespot.com website!
  
  args:
    - num_pages: specify how many number of pages you decide to crawl (each page contains 21 game reviews).
  
  output:
    - list of urls of game reviews.
  """
  #initializing webscraping
  driver = web_driver()

  urls = [] #to store urls
  
  # creating a loop to crawl desired pages and extract urls
  for i in range(num_pages):
    page_url = f"https://www.gamespot.com/games/reviews/?page={i+1}"
    driver.get(page_url)
    time.sleep(5)

    for e in driver.find_elements(By.CLASS_NAME, "card-item__link"):
      try:
        urls.append(e.get_attribute("href"))
      except:
        pass
  
  driver.quit()

  return urls

def extract_game_review_document(game_url):
  """
  This function will scrape webpage of game review to provide a document

  args:
    - game_url: url of game review (string)
  
  output:
    - document of game review (string)
  """
  # initializing web scraping
  driver = web_driver()

  # loading html of url
  driver.get(game_url)

  # specifying elements
  elements = driver.find_elements(By.CSS_SELECTOR, '[dir="ltr"]')
  
  # storing paragraphs in a list
  doc = [] 
  
  # creating a loop to find elements
  for e in elements:
    try:
      doc.append(e.text)
    except:
      pass

  # quiting driver
  driver.quit()

  return doc
