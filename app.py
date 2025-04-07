from flask import Flask,render_template,jsonify
import http.client
import json
from datetime import datetime
from models import db, CovidStats

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/covid_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db with the app
db.init_app(app)

@app.route('/get-covid-data')
def get_covid_data():
    try:
        conn = http.client.HTTPSConnection("covid-193.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': "5fafa80fbbmsh2a1f576e6ce1b1dp18adcdjsnbd3633751711",
            'x-rapidapi-host': "covid-193.p.rapidapi.com"
        }
        
        conn.request("GET", "/statistics", headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        
        # Parse the response as a string
        data_str = data.decode('utf-8')
        
        # Replace NaN values with null before parsing as JSON
        data_str = data_str.replace('NaN', 'null')
        
        j = json.loads(data_str)
        
        # Get the response data directly
        covid_data = j['response']
        
        return jsonify({
            'status': 'success',
            'data': covid_data,
            'count': len(covid_data)
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/')
def home():
    return render_template('index.html', title='COVID-19 Data')

@app.route('/visualize')
def visualize():
    return render_template('visualization.html', title='COVID-19 Data Visualization')

# Add new route to save data
@app.route('/save-covid-data', methods=['POST'])
def save_covid_data():
    try:
        # Get the current COVID data
        conn = http.client.HTTPSConnection("covid-193.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': "5fafa80fbbmsh2a1f576e6ce1b1dp18adcdjsnbd3633751711",
            'x-rapidapi-host': "covid-193.p.rapidapi.com"
        }
        
        conn.request("GET", "/statistics", headers=headers)
        res = conn.getresponse()
        data = res.read()
        data_str = data.decode('utf-8')
        data_str = data_str.replace('NaN', 'null')
        covid_data = json.loads(data_str)['response']

        saved_count = 0
        for entry in covid_data:
            try:
                # Parse the date from the time string
                day = datetime.strptime(entry['day'], '%Y-%m-%d').date()
                
                # Check if record already exists
                exists = CovidStats.query.filter_by(
                    country=entry['country'],
                    day=day,
                    continent=entry['continent']
                ).first()

                if not exists:
                    new_stat = CovidStats(
                        continent=entry['continent'],
                        country=entry['country'],
                        day=day,
                        active_cases=entry['cases'].get('active', 0),
                        critical_cases=entry['cases'].get('critical'),
                        new_cases=int(entry['cases']['new'].strip('+')) if entry['cases'].get('new') else None,
                        recovered_cases=entry['cases'].get('recovered', 0),
                        total_cases=entry['cases'].get('total', 0),
                        deaths_1M_pop=float(entry['deaths'].get('1M_pop')) if entry['deaths'].get('1M_pop') else None,
                        new_deaths=int(entry['deaths']['new'].strip('+')) if entry['deaths'].get('new') else None,
                        total_deaths=entry['deaths'].get('total', 0),
                        population=entry['population'],
                        tests_1M_pop=float(entry['tests'].get('1M_pop')) if entry['tests'].get('1M_pop') else None,
                        total_tests=entry['tests'].get('total'),
                        timestamp=datetime.strptime(entry['time'], '%Y-%m-%dT%H:%M:%S%z')
                    )
                    db.session.add(new_stat)
                    saved_count += 1

            except Exception as e:
                print(f"Error processing entry: {str(e)}")
                continue

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Successfully saved {saved_count} new records',
            'saved_count': saved_count
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/get-saved-covid-data')
def get_saved_covid_data():
    try:
        # Query all records from the database
        covid_stats = CovidStats.query.all()
        
        # Convert the records to a list of dictionaries
        data = []
        for stat in covid_stats:
            data.append({
                'continent': stat.continent,
                'country': stat.country,
                'population': stat.population,
                'cases': {
                    'new': f"+{stat.new_cases}" if stat.new_cases else None,
                    'active': stat.active_cases,
                    'critical': stat.critical_cases,
                    'recovered': stat.recovered_cases,
                    'total': stat.total_cases
                },
                'deaths': {
                    'total': stat.total_deaths
                },
                'time': stat.timestamp.strftime('%Y-%m-%dT%H:%M:%S+00:00')
            })
        
        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 