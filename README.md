# Pipeline
The goal of this project is to create a pipeline:
* Intercept tweets
* Store them in a Mongo database
* Transform them and apply sentiment analysis
* Send the result to a Postgres database


![Pipeline](pipeline.svg)


Each point is hosted in a docker container, for postgres and mongodb I used already available images and I create my own in the case of ETL (transform and sentiment analysis) and the tweet collector.

To set it up:
* Clone the repository
* Ammend the docker-compose file with your port preferences and postgres credentials
* In the etl_job folder change put also your credentials in the .py file
* Tweet_colllector folder:
  * The config file should include your Twitter API credentials
  * There is a filter (track) in the code itself that you can change to target one specific topic and language in the twitter stream

To use it:
* Install Docker and Docker-compose in your local machine
* Run docker-compose build from the main folder
* Run docker-compose up

