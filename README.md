# COVID Stats Dashboard

A web app that shows COVID-19 data from around the world. Built with Flask and Chart.js.

## What It Does

This app:
1. Shows COVID-19 numbers
2. Creates charts from the data
3. Saves data in a database
4. Lets you filter by region

Live site: https://python-for-data-analytics.onrender.com/

Presentation: https://docs.google.com/presentation/d/1ncvpkDDNRaSmFMZPjToHh4Os6xMtSnOS3ixt3T98Yi8/edit?slide=id.p1#slide=id.p1

## Setup Guide

### You'll Need
1. Python 3.8+
2. PostgreSQL 
3. pip
4. Git

### How to Install

1. Get the code:
   ```
   git clone https://github.com/muhammad342/Python_for_data_analytics
   ```

2. Set up Python:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your .env file:
   ```
   SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost:5432/covid_db
   RAPIDAPI_KEY="API KEY"
   ```

5. Set up the database:
   ```
   python init_db.py
   ```

6. Start the app:
   ```
   python app.py
   ```

The app runs at: http://localhost:5001

## Features

The dashboard has:

**Data**
- Gets COVID data from RapidAPI

**Charts**
1. Charts that update 
2. Compare regions
3. Filter options

**Database**
- Stores data in PostgreSQL

**Look and Feel**
1. Clean design
2. Pages of data
3. Charts you can interact with

## API Guide

The app has these data endpoints:

### Getting Data

`GET /get-covid-data`
- Gets fresh COVID stats
- Needs a RapidAPI key
- Gives data in JSON format

`GET /get-saved-covid-data`
- Gets saved data from the database
- Shows past stats

### Saving Data

`POST /save-covid-data`
- Saves COVID stats to database
- Prevents duplicate entries
- Reports if save worked

## Database Setup

We use PostgreSQL with this table:

**covid_stats**
- id (main key)
- continent
- country
- day
- active_cases
- critical_cases
- new_cases
- recovered_cases
- total_cases
- deaths_1M_pop
- new_deaths
- total_deaths
- population
- tests_1M_pop
- total_tests
- timestamp

## Main Packages

Flask==2.3.3
Flask-SQLAlchemy==3.1.1
gunicorn==21.2.0
psycopg2-binary==2.9.10
SQLAlchemy==2.0.40
pandas==2.2.3

Full list in `requirements.txt`.

## Acknowledgments && References

This project uses:
1. [Flask web app tutorial](https://medium.com/@AlexanderObregon/building-a-web-application-from-scratch-with-flask-and-python-f25f1f638aec)
2. GPT for HTML and CSS help
3. [RapidAPI](https://rapidapi.com)
4. [Chart.js](https://www.chartjs.org)
5. [SQLAlchemy](https://www.sqlalchemy.org)
6. [Flask](https://flask.palletsprojects.com)