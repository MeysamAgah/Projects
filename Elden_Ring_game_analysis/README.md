# Problem Statment
In the highly competitive video game industry, understanding user feedback and player behavior is critical for improving game design, optimizing marketing strategies, and maximizing sales. Sentiment analysis of player reviews provides insights into how users perceive different aspects of a game, including gameplay, graphics, storyline, and overall user experience. By detecting specific sentiments and opinions, developers can prioritize improvements and tailor future releases to better meet player expectations.
<br>
Additionally, player engagement and purchasing behavior vary significantly across different seasons and events. Understanding these patterns helps companies align marketing campaigns and game launches for peak impact. Analyzing the relationship between player behavior, sentiment trends, and sales performance offers a holistic view of a game's success and informs better strategic decisions.
<br>
This project aims to perform sentiment analysis on game reviews using pre-trained models and evaluate how sentiment trends influence sales across various seasonalities. By integrating these insights into a comprehensive Power BI dashboard, we provide actionable intelligence for stakeholders to drive business growth and enhance player satisfaction.
<br>
# Data Collection
For this project, data was collected from multiple sources to provide a comprehensive analysis. User and critic reviews were obtained from Metacritic, a popular website known for aggregating reviews of games, movies, and other media, providing scores from both professional critics and general users. This platform serves as a key resource for evaluating public sentiment and critical reception.
<br>
Furthermore, some data about details on how much elden ring was played gathered from [howlongtobeat.com](https://howlongtobeat.com). this data contains some tabular playtime data and some comments from players who dropped the game early.
<br>
Additionally, supplementary statistics such as playtime and game difficulty were gathered from Metacritics sourced by GameFAQs, a well-known repository for game guides, FAQs, and user-submitted content. These data points were extracted using Selenium, a powerful web scraping library that automates browser interactions for dynamic content extraction.
<br>
Last but not least, important metrics related to player activity, including the number of concurrent players and real-time viewer counts, were manually downloaded from SteamDB, a platform that tracks game statistics on Steam. Together, these data sources offer a rich foundation for analyzing game performance, user engagement, and sentiment trends. <br>
Further information about data used in this survey follow this [link](https://github.com/MeysamAgah/Projects/blob/main/Elden_Ring_game_analysis/Data/README.md) to data folder readme
<br>
# Data Cleaning
This step consist of cleaning two dataframes of reviews
1. **Metacritic comments:** <br>
1.1 for this dataset missing values removed<br>
   1.2 duplicated rows removed<br>
   1.3 rows containing spoiler (in other word "[SPOILER ALERT: This review contains spoilers.]") were removed<br>
   1.4 and last but not least data filtered to only english comments<br>
2. **Retirement reasons:** <br>
2.1 values representing Linux in platforms column replaced by PC<br>
   2.2 all values in playtimes column cleaned up<br>
   2.3 missing values and duplicated rows were removed

# Aspect Extraction
To extract all aspects from the reviews, I utilized the pre-trained model [InstructABSA](https://github.com/kevinscaria/InstructABSA) , which is a state-of-the-art model for Aspect-Based Sentiment Analysis tasks. The implemented function identifies aspects in each review and stores them in a new column.<br>
then I gathered all aspects whether positive or negative in a list for further steps.

# Aspect Categorization
In this step we first fine tune a Modern BERT model by training on video gaming paragraphs extracted from gamespot reviews.<br>
then I vectorize every aspectleveraging fine tuned Modern BERT.<br>
then I use Kmeans to cluster these aspects and find categories. most frequent aspect in each cluster will be cluster representative and will be category name<br>
finally by counting number of positives and negatives in each category we can analyze game by category
