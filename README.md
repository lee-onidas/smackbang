![image](https://user-images.githubusercontent.com/27832889/158303927-93f1aeae-f216-4e87-8f40-bb23969b55b5.png)

SmackBang is a travel app that finds the middle ground between two origin locations so family, friends, and colleagues can meet up in the middle.  Users enter the two origins, their travel dates, their preferred continent to meet up, and the default currency to use.  

The app uses API's to collect data which is then run through several models to predict the destination airfare, evaluate the prediction against the quoted price, and give an assessment of the current sentiment (aka "The Vibe") of the destination based on recent Tweets.

Users are able to click on live booking links with <a href="https://www.kiwi.com">kiwi.com</a> to book or explore the destinations with the interactive map.

App home: https://smackbang.herokuapp.com/

![image](https://user-images.githubusercontent.com/27832889/158303379-9702b5ea-3443-48f1-b7fe-f30ee896ab14.png)

![image](https://user-images.githubusercontent.com/27832889/158303402-4cf4292b-8292-4182-8835-0b9d6a06198f.png)



# Tech Stack
### Front End
- <a href="https://streamlit.io/">Streamlit</a>
- <a href="https://www.heroku.com/">Heroku</a>
- <a href="https://deckgl.readthedocs.io//">pydeck</a>

### Back End
- <a href="https://fastapi.tiangolo.com/">FastAPI</a>
- <a href="https://www.docker.com/">Docker</a>
- <a href="https://cloud.google.com/">Google Cloud Platform</a>

### Data Sources
- <a href="https://tequila.kiwi.com/portal/login">kiwi.com Tequila API</a>
- <a href="https://developer.twitter.com/en">Twitter API</a>
- <a href="https://www.kaggle.com/c/air-ticket-fare-prediction/data">Kaggle: Air Ticket Fare Dataset</a>

### Machine Learning Tools
- <a href="https://xgboost.readthedocs.io/">XGBoost</a>
- <a href="https://www.nltk.org/index.html">nltk </a>


# Team Members
- <a href="https://github.com/lee-onidas">Lee Steven </a>
- <a href="https://github.com/emadam">Emad Aminmoghadam </a>
- <a href="https://github.com/yourpandaboy">Norty Nakagawa</a>
- <a href="https://github.com/padofreo">Paul Adolphson</a>
