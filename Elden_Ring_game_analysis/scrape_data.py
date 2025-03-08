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
                      game = "elden-ring"
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

  url = f"https://www.metacritic.com/game/{game}/{reviewer}-reviews/?platform={platform}" # forming up url according to inputs
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

def scrape_gamefaq(game='elden-ring',
                   user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'):
  url = f"https://www.metacritic.com/game/{game}/"
  driver = web_driver(user_agent_string)
  driver.get(url)
  time.sleep(5)

  # ratings dataframe
  total_ratings = [e.split(',')[0] for e in str(driver.page_source).split(";k.footer")[0].split("ratings:")[1].split(',play_time:')[0].split('total:')[1:]]
  game_rating_ids1 = [e.split(',')[0] for e in str(driver.page_source).split(";k.footer")[0].split("ratings:")[1].split(',play_time:')[0].split('game_rating_id:')[1:]]
  game_rating_labels = [e.split(',')[0][1:-2] for e in str(driver.page_source).split(";k.footer")[0].split("ratings:")[1].split(',play_time:')[0].split('label:')[1:]]

  df_ratings_stats = pd.DataFrame(
      {
          'total_ratings': total_ratings,
          'game_rating_ids': game_rating_ids1,
          'game_rating_labels': game_rating_labels
      }
  )

  # play time dataframe
  total_playtime = [e.split(',')[0] for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split(',difficulty:')[0].split('total:')[1:]]
  playtime_hour = [e.split('label:"')[1].replace("\\u003C ", '<').replace("\\u003E= ", '>') for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split(',difficulty:')[0].split(" Hour")[:-1]]
  playtime_id = [e.split('}')[0] for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split(',difficulty:')[0].split("play_time:")[1:]]

  df_playtime_stats = pd.DataFrame(
      {
          'total_playtime': total_playtime,
          'playtime_hour': playtime_hour,
          'playtime_id': playtime_id
      }
  )

  # difficulty dataframe
  total_difficulty = [e.split(',')[0] for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split(',difficulty:[')[1].split("play_status:[")[0].split('total:')[1:]]
  label_difficulty = [e.split(',')[0][1:-1] for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split(',difficulty:[')[1].split("play_status:[")[0].split('label:')[1:]]
  difficulty_id = [e.split('}')[0] for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split(',difficulty:[')[1].split("play_status:[")[0].split('difficulty_id:')[1:]]

  df_difficulty = pd.DataFrame(
      {
          'total_difficulty': total_difficulty,
          'label_difficulty': label_difficulty,
          'difficulty_id': difficulty_id
      }
  )

  # play_status dataframe
  total_play_status = [e.split(',')[0] for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split("play_status:[")[1].split('label:')[1:]]
  label_play_status = [e.split(',')[0] for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split("play_status:[")[1].split('total:')[1:]]
  play_status_id = [e.split('}')[0] for e in str(driver.page_source).split(";k.footer")[0].split("play_time:[")[1].split("play_status:[")[1].split('play_status_id:')[1:]]

  df_play_status = pd.DataFrame(
      {
          'total_play_status': total_play_status,
          'label_play_status': label_play_status,
          'play_status_id': play_status_id
      }
  )
  driver.quit()
  return df_ratings_stats, df_playtime_stats, df_difficulty, df_play_status

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

desired_data = ['df_ratings_stats', 'df_playtime_stats', 'df_difficulty', 'df_play_status']
faq_data = scrape_gamefaq()
for i in range(len(desired_data)):
  faq_data[i].to_csv(f'faq_{desired_data[i][3:]}.csv', index=False)

def scrape_howlongtobeat(game_id,
                         user_agent_string='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'):
  base_url = f'https://howlongtobeat.com/game/{game_id}' #base url
  driver = web_driver(user_agent_string) #initialize webscraping
  driver.get(base_url) #load html of webpage
  time.sleep(5)

  def extract_table(num_last_div): #by entering last div number can extract desired table 
    columns1 = []
    for i in range(10000):
      try:
        columns1.append(driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[2]/div/div[2]/div[{str(num_last_div)}]/table/thead/tr/td[{str(i+1)}]").text)
      except:
        break
    table_full1 = []
    for i in range(10000):
      try:
        table_full1.append(driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[2]/div/div[2]/div[{str(num_last_div)}]/table/tbody/tr[{str(i+1)}]").text)
      except:
        break
    num_rows1 = len(table_full1)

    data1 = {c: [] for c in columns1}
    for j in range(num_rows1):
      for i in range(len(columns1)):
        try:
          data1[columns1[i]].append(driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[2]/div/div[2]/div[{str(num_last_div)}]/table/tbody/tr[{str(j+1)}]/td[{str(i+1)}]").text)
        except:
          data1[columns1[i]].append(None)

    return data1
  table1 = extract_table(7)
  table2 = extract_table(8)
  table3 = extract_table(9)

  #retirements report data
  retirements_url = base_url + "/lists#retirement"
  driver.get(retirements_url)
  time.sleep(5)

  usernames = []
  platforms = []
  playtimes = []
  retirement_reasons = []
  for i in range(1, 141):
    try:
      usernames.append(driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[2]/div/div[2]/div[5]/div/article[{str(i)}]/div[2]/h4/a").text)
    except:
      usernames.append(None)
    try:
      platforms.append(driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[2]/div/div[2]/div[5]/div/article[{str(i)}]/div[2]/span[1]").text)
    except:
      platforms.append(None)
    try:
      playtimes.append(driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[2]/div/div[2]/div[5]/div/article[{str(i)}]/div[2]/span[2]").text)
    except:
      playtimes.append(None)
    try:
      retirement_reasons.append(driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div[2]/div/div[2]/div[5]/div/article[{str(i)}]/div[2]/div").text)
    except:
      retirement_reasons.append(None)

  driver.quit()
  
  table4 = {
          'usernames': usernames,
          'platforms': platforms,
          'playtimes': playtimes,
          'retirement_reasons': retirement_reasons
  }

  return table1, table2, table3, table4
