# Opinion analysis in Twitter

This `README.md` contains a short description of the project and some required instructions for configuring and running the application in the deployment phase.

## Objective

The objective of this mini application is to develop a system to analyze opinions about a person, an event, a brand in tweets. The example given in this project is an application of opinions on a political personality. Through this project, you will discover the python ecosystem to work with Twitter and do text data analysis.

![ALT](images/sentiment_analysis_example.png)

The MVP (Minimum Viable Product) of this project will consist in delivering a first version of the end-to-end analysis tool, i.e. from data collection to sentiment prediction and its visualization with simple solutions.

In particular, the MVP :
* Will allow to connect to the Twitter API to collect a set of tweets related to an entity.
* Will be based solely on the analysis of the textual content of the tweets and will neglect information about the author of the tweet, its type (retweet, reply, ...) and its multimedia content.
* Will allow simple processing and analysis of tweets.
* Display the results of the analysis in the form of a time graph as above.

## App configuration

This project is based on version 3 of python.

### Create a virtual environment

In the root folder `/`, create a vritual environment runnning the command:
```
python -m venv env
```

To activate the virtual environement:
```
source env/bin/activate
```

Then install your pip dependencies:
```
pip install -r requirements.txt
```

To exit the virtual environement, `CTRL+d` or run:
```
deactivate
```

## Run the app

