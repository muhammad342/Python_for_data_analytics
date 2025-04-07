from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class CovidStats(db.Model):
    __tablename__ = 'covid_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    continent = db.Column(db.String(100))
    country = db.Column(db.String(100))
    day = db.Column(db.Date)
    active_cases = db.Column(db.Integer)
    critical_cases = db.Column(db.Integer, nullable=True)
    new_cases = db.Column(db.Integer, nullable=True)
    recovered_cases = db.Column(db.Integer)
    total_cases = db.Column(db.Integer)
    deaths_1M_pop = db.Column(db.Float, nullable=True)
    new_deaths = db.Column(db.Integer, nullable=True)
    total_deaths = db.Column(db.Integer)
    population = db.Column(db.Integer)
    tests_1M_pop = db.Column(db.Float, nullable=True)
    total_tests = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime)

    # Add unique constraint
    __table_args__ = (UniqueConstraint('country', 'day', 'continent', name='unique_country_day_continent'),) 