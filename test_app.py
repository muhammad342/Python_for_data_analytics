import unittest
from datetime import datetime, date
from app import app
from models import CovidStats, db

class TestCovidApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/covid_tracker'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_get_saved_covid_data(self):
        test_stats = CovidStats(
            continent='Europe',
            country='Germany',
            day=date(2023, 5, 15),
            active_cases=5000,
            critical_cases=200,
            new_cases=300,
            recovered_cases=10000,
            total_cases=15000,
            deaths_1M_pop=50.5,
            new_deaths=20,
            total_deaths=1000,
            population=83000000,
            tests_1M_pop=200.5,
            total_tests=5000000,
            timestamp=datetime(2023, 5, 15, 12, 0, 0)
        )
        db.session.add(test_stats)
        db.session.commit()
        
        response = self.app.get('/get-saved-covid-data')
        
        self.assertEqual(response.status_code, 200)
        
        response_data = response.get_json()
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['count'], 1)
        
        data = response_data['data'][0]
        self.assertEqual(data['continent'], 'Europe')
        self.assertEqual(data['country'], 'Germany')
        self.assertEqual(data['population'], 83000000)
        self.assertEqual(data['cases']['active'], 5000)
        self.assertEqual(data['cases']['critical'], 200)
        self.assertEqual(data['cases']['new'], '+300')
        self.assertEqual(data['cases']['recovered'], 10000)
        self.assertEqual(data['cases']['total'], 15000)
        self.assertEqual(data['deaths']['total'], 1000)
        
if __name__ == '__main__':
    unittest.main() 