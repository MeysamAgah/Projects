# installs
!pip install selenium
!apt-get install chromium-driver

# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import pandas as pd

def web_driver(user_agent_string):
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

def scrape_metacritic(platform, 
                      reviewer="user", 
                      num_comments=50,
                      user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'):
  """
  arguments:
    platform: specify platform of game, for example "playstation-5" default will use default platform of website
    reviewer: type of reviewer e.g. user or critic
    num_comments: integer indicating number of comments to evaluate
    user_agent_string: string indicating user agent of browser
    ...
  output: will be a dataframe:
    df: represents dataframe of desired reviews
      columns are: reviewer, review_text, score, review_date, platform
  """
  driver = web_driver(user_agent_string) #initializing webscrapping

  url = f"https://www.metacritic.com/game/elden-ring/{reviewer}-reviews/?platform={platform}" # forming up url according to inputs
  driver.get(url) # loading html of url
  time.sleep(5) # Wait for initial page load

  max_num_comments = int(driver.find_elements(By.CLASS_NAME, "c-pageProductReviews_text")[0].text.split(" ")[1].replace(",", ""))
  if num_comments > max_num_comments:
    num_comments = max_num_comments
  
  review_texts = []
  reviewers = []
  review_dates = []
  ratings = []
  platforms = []

  prev_height = driver.execute_script("return document.body.scrollHeight")
  scroll_pause_time = 10
  no_more_scroll_count = 0

  
  
  while len(review_texts) < num_comments:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)  # Allow time for content to load

    # Check for new height after scrolling
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:  # Stop if no more content to load
      no_more_scroll_count += 1
      if no_more_scroll_count >= 2:  # Stop after two consecutive no-scroll detections
        break
    else:
      no_more_scroll_count = 0  # Reset counter if scroll happened
    prev_height = new_height

    # Extract data after scrolling (partial extraction each loop)
    full_review = driver.find_elements(By.CLASS_NAME, "c-siteReview")
    for e in full_review:
      if len(review_texts) >= num_comments:
        break  # Stop collecting if num_comments reached

      try:
        review_texts.append(e.find_element(By.CLASS_NAME, "c-siteReview_quote").text)
        if reviewer == "user":
          reviewers.append(e.find_element(By.CLASS_NAME, "c-siteReviewHeader_username").text)
        elif reviewer == "critic":
          reviewers.append(e.find_element(By.CLASS_NAME, "c-siteReviewHeader_publicationName").text)
        review_dates.append(datetime.strptime(e.find_element(By.CLASS_NAME, "c-siteReviewHeader_reviewDate").text, "%b %d, %Y").date()) 
        ratings.append(e.find_element(By.CLASS_NAME, "c-siteReviewHeader_reviewScore").text) 
        platforms.append(e.find_element(By.CLASS_NAME, "c-siteReview_platform").text)
      except Exception as ex:
        print(f"Error extracting review data: {ex}")

  # Close the browser
  driver.quit()

  #forming up a dataframe for output
  df = pd.DataFrame(
      {
          'reviewer': reviewers,
          'review_text': review_texts,
          'rating': ratings,
          'review_date': review_dates,
          'platform': platforms,
          'reviewer_type': [reviewer for i in range(len(reviewers))]
      }
  )

  return df

# initializing with an empty dataframe
df = pd.DataFrame(
    columns=['reviewer', 'review_text', 'rating', 'review_date', 'platform', 'reviewer_type']
)

# specifying required versions
elden_ring_platforms = ['pc', 'xbox-one', 'playstation-4', 'xbox-series-x', 'playstation-5'] # desired platforms
elden_ring_reviewers = ['user', 'critic'] # desired reviewers

# update and filling dataframe
for p in elden_ring_platforms:
  for r in elden_ring_reviewers:
    try:
      df_temp = scrape_metacritic(p, r, num_comments=float('inf')) #all comments for each webpage will be scraped
      df = pd.concat([df, df_temp])
      print(f"data for {r}s of {p} collected")
    except Exception as ex:
      print(f"Error extracting review data: {ex}")
# save dataframe as a .csv file
df.to_csv('Elden_Ring_metacritic_reviews.csv', index=False)
